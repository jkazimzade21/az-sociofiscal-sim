"""
Tests for simplified tax calculation.

Legal basis:
- Tax Code 219: Simplified tax base
- Tax Code 220: Simplified tax rates
"""

import pytest
from decimal import Decimal

from az_sim import SimplifiedTaxEngine, TaxpayerInput
from az_sim.entities import TurnoverInput


class TestGeneralSimplifiedTax:
    """
    Test general simplified tax calculation (220.1).
    """

    def test_general_2_percent_rate(self):
        """
        General simplified tax = 2% of turnover (220.1).
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("150000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "general"
        # Tax = 150000 × 0.02 = 3000 AZN
        assert result.tax_amount == Decimal("3000")
        assert result.tax_rate == Decimal("0.02")

    def test_small_turnover_calculation(self):
        """Small turnover still gets 2% rate."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("50000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 50000 × 0.02 = 1000 AZN
        assert result.tax_amount == Decimal("1000")


class TestTradeCateringTax:
    """
    Test trade/catering tax calculation for turnover > 200k (220.1-1).
    """

    def test_trade_over_200k_8_percent(self):
        """
        Trade/catering > 200k: 8% general rate (220.1-1).
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("300000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "trade_catering_over_200k"
        # Tax = 300000 × 0.08 = 24000 AZN
        assert result.tax_amount == Decimal("24000")

    def test_trade_pos_6_percent(self):
        """
        Trade/catering: POS turnover gets 6% rate (220.1-1).
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=True,
            turnover=TurnoverInput(
                gross_turnover_12m=Decimal("300000"),
                pos_retail_nonregistered_12m=Decimal("100000"),
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "trade_catering_over_200k"
        # POS tax = 100000 × 0.06 = 6000 AZN
        # Other tax = 200000 × 0.08 = 16000 AZN
        # Total = 22000 AZN
        assert result.tax_amount == Decimal("22000")
        assert "POS turnover" in result.exemptions_applied[0]

    def test_catering_same_rates(self):
        """Catering gets same rates as trade."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_catering=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("250000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "trade_catering_over_200k"


class TestTurnoverCalculation:
    """
    Test turnover calculation with VAT-exempt exclusion and POS coefficient.
    """

    def test_adjusted_turnover_with_pos_coefficient(self):
        """
        POS coefficient of 0.5 reduces effective turnover (218.1-1).
        """
        engine = SimplifiedTaxEngine(debug=True)

        # Gross: 240k, POS: 100k
        # Adjusted = 240k - 100k + 50k = 190k (under 200k threshold)
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(
                gross_turnover_12m=Decimal("240000"),
                pos_retail_nonregistered_12m=Decimal("100000"),
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "general"  # Under 200k adjusted

    def test_vat_exempt_reduces_taxable_turnover(self):
        """
        VAT-exempt turnover excluded from threshold test (218.1.1).
        """
        engine = SimplifiedTaxEngine()

        # Gross: 300k, VAT-exempt: 150k
        # Taxable = 300k - 150k = 150k (under 200k)
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(
                gross_turnover_12m=Decimal("300000"),
                vat_exempt_turnover_12m=Decimal("150000"),
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "general"

    def test_combined_adjustments(self):
        """
        Both VAT-exempt exclusion and POS coefficient applied together.
        """
        engine = SimplifiedTaxEngine()

        # Gross: 350k, VAT-exempt: 100k, POS: 100k
        # Taxable = 350k - 100k = 250k
        # Adjusted = 250k - 100k + 50k = 200k (exactly at threshold)
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(
                gross_turnover_12m=Decimal("350000"),
                vat_exempt_turnover_12m=Decimal("100000"),
                pos_retail_nonregistered_12m=Decimal("100000"),
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True


class TestDebugTrace:
    """
    Test debug trace functionality.
    """

    def test_debug_trace_included_when_enabled(self):
        """Debug trace included when debug=True."""
        engine = SimplifiedTaxEngine(debug=True)
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.debug_trace is not None
        assert len(result.debug_trace) > 0
        assert "rule" in result.debug_trace[0]
        assert "result" in result.debug_trace[0]
        assert "article" in result.debug_trace[0]

    def test_debug_trace_not_included_when_disabled(self):
        """Debug trace not included when debug=False."""
        engine = SimplifiedTaxEngine(debug=False)
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.debug_trace is None

    def test_debug_trace_shows_failing_rule(self):
        """Debug trace shows which rule failed."""
        engine = SimplifiedTaxEngine(debug=True)
        input_data = TaxpayerInput(
            is_vat_registered=True,  # This will fail
        )
        result = engine.evaluate(input_data)

        assert result.debug_trace is not None
        failing_rules = [t for t in result.debug_trace if not t["result"]]
        assert len(failing_rules) > 0
        assert failing_rules[0]["rule"] == "vat_registration"
