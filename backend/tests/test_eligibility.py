"""
Tests for simplified tax eligibility rules.

Each test case maps to a specific article in the Tax Code
for full legal traceability.
"""

import pytest
from decimal import Decimal

from az_sim import SimplifiedTaxEngine, TaxpayerInput
from az_sim.entities import (
    TurnoverInput,
    PropertyTransferInput,
    PropertyType,
    LocationZone,
    LicensedActivityCode,
)


class TestVATRegistration:
    """
    Test VAT registration gate (218.1.1).

    VAT-registered taxpayers cannot use simplified tax regime.
    """

    def test_vat_registered_not_eligible(self):
        """VAT registered -> not eligible (218.1.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(is_vat_registered=True)
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "VAT_REGISTERED"
        assert any(lb.article == "218.1.1" for lb in result.legal_basis)

    def test_not_vat_registered_can_proceed(self):
        """Not VAT registered -> can proceed (218.1.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        # Should be eligible (no other disqualifiers)
        assert result.eligible is True


class TestTurnoverThreshold:
    """
    Test turnover threshold rules (218.1.1, 218.1.2, 218.1-1).
    """

    def test_turnover_under_threshold_eligible(self):
        """Turnover <= 200k -> eligible (218.1.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("150000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "general"

    def test_turnover_over_threshold_not_trade_not_eligible(self):
        """Turnover > 200k, not trade/catering -> not eligible (218.1.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=False,
            does_catering=False,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("250000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "TURNOVER_EXCEEDED"

    def test_turnover_over_threshold_trade_eligible(self):
        """Turnover > 200k, trade -> eligible with different route (218.1.2)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("250000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "trade_catering_over_200k"

    def test_pos_coefficient_reduces_turnover(self):
        """POS turnover counted at 0.5 coefficient (218.1-1)."""
        engine = SimplifiedTaxEngine(debug=True)

        # Without POS: 220k gross, would exceed 200k
        # With POS: 220k - 100k + 50k = 170k (under threshold)
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(
                gross_turnover_12m=Decimal("220000"),
                pos_retail_nonregistered_12m=Decimal("100000"),
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True

    def test_vat_exempt_excluded_from_turnover(self):
        """VAT-exempt turnover excluded from threshold test (218.1.1)."""
        engine = SimplifiedTaxEngine()

        # 250k gross, but 100k is VAT-exempt -> 150k taxable
        input_data = TaxpayerInput(
            is_vat_registered=False,
            turnover=TurnoverInput(
                gross_turnover_12m=Decimal("250000"),
                vat_exempt_turnover_12m=Decimal("100000"),
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True


class TestAutomaticRoutes:
    """
    Test automatic simplified tax categories (218.4).
    """

    def test_auto_transport_eligible(self):
        """Passenger transport/taxi -> automatic eligible (218.4.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_transport=True,
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "auto_transport"

    def test_auto_property_eligible(self):
        """Own real estate transfer -> automatic eligible (218.4.3)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("100"),
                location_zone=LocationZone.BAKU_OTHER,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.route == "auto_property"


class TestDisqualifiers:
    """
    Test disqualifying conditions (218.5.*).
    """

    def test_excise_producer_not_eligible(self):
        """Excise goods producer -> not eligible (218.5.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            produces_excise_goods=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "EXCISE_PRODUCER"
        assert any(lb.article == "218.5.1" for lb in result.legal_basis)

    def test_credit_org_not_eligible(self):
        """Credit organization -> not eligible (218.5.2)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            is_credit_org=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "FINANCIAL_SECTOR"

    def test_insurance_participant_not_eligible(self):
        """Insurance market participant -> not eligible (218.5.2)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            is_insurance_market_participant=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "FINANCIAL_SECTOR"

    def test_pawnshop_not_eligible(self):
        """Pawnshop -> not eligible (218.5.2)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            is_pawnshop=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "FINANCIAL_SECTOR"

    def test_pension_fund_not_eligible(self):
        """Non-state pension fund -> not eligible (218.5.3)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            is_non_state_pension_fund=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "PENSION_FUND"

    def test_rental_income_not_eligible(self):
        """Rental income -> not eligible (218.5.4)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            has_rental_income=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "RENTAL_ROYALTY"

    def test_royalty_income_not_eligible(self):
        """Royalty income -> not eligible (218.5.4)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            has_royalty_income=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "RENTAL_ROYALTY"

    def test_natural_monopoly_not_eligible(self):
        """Natural monopoly -> not eligible (218.5.5)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            is_natural_monopoly=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "NATURAL_MONOPOLY"

    def test_fixed_assets_over_threshold_not_eligible(self):
        """Fixed assets > 1M AZN -> not eligible (218.5.6)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            fixed_assets_residual_value=Decimal("1500000"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "FIXED_ASSETS_EXCEEDED"

    def test_fixed_assets_under_threshold_eligible(self):
        """Fixed assets <= 1M AZN -> eligible (218.5.6)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            fixed_assets_residual_value=Decimal("500000"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True

    def test_gold_seller_not_eligible(self):
        """Gold/jewelry/diamond seller -> not eligible (218.5.11)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            sells_gold_jewelry_diamonds=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "PRECIOUS_GOODS"

    def test_fur_seller_not_eligible(self):
        """Fur/leather seller -> not eligible (218.5.12)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            sells_fur_leather=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "FUR_LEATHER"


class TestWholesaleException:
    """
    Test wholesale trade exception (218.5.9 + 218.6.1).
    """

    def test_wholesale_over_30_percent_not_eligible(self):
        """Wholesale e-invoice ratio > 30% -> not eligible (218.5.9)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=True,
            does_wholesale=True,
            wholesale_einvoice_ratio=Decimal("0.35"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "WHOLESALE_EXCEEDED"

    def test_wholesale_under_30_percent_eligible(self):
        """Wholesale e-invoice ratio <= 30% -> eligible (218.6.1 exception)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=True,
            does_wholesale=True,
            wholesale_einvoice_ratio=Decimal("0.25"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True

    def test_wholesale_exactly_30_percent_eligible(self):
        """Wholesale e-invoice ratio = 30% -> eligible (218.6.1 exception)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_trade=True,
            does_wholesale=True,
            wholesale_einvoice_ratio=Decimal("0.30"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True


class TestB2BException:
    """
    Test B2B works/services exception (218.5.10 + 218.6.2).
    """

    def test_b2b_over_30_percent_not_eligible(self):
        """B2B e-invoice ratio > 30% -> not eligible (218.5.10)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_b2b_works_services=True,
            b2b_einvoice_ratio=Decimal("0.40"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "B2B_EXCEEDED"

    def test_b2b_under_30_percent_eligible(self):
        """B2B e-invoice ratio <= 30% -> eligible (218.6.2 exception)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_b2b_works_services=True,
            b2b_einvoice_ratio=Decimal("0.20"),
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True


class TestLicensedActivities:
    """
    Test licensed activities rules (218.5.13) - PATCH 3.
    """

    def test_licensed_medical_not_eligible(self):
        """Private medical activity -> not eligible (218.5.13)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            licensed_activity_codes=[LicensedActivityCode.PRIVATE_MEDICAL],
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "LICENSED_ACTIVITY"

    def test_licensed_education_not_eligible(self):
        """Education activity -> not eligible (218.5.13)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            licensed_activity_codes=[LicensedActivityCode.EDUCATION],
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "LICENSED_ACTIVITY"

    def test_licensed_construction_not_eligible(self):
        """Construction-related licensed activity -> not eligible (218.5.13)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            licensed_activity_codes=[LicensedActivityCode.CONSTRUCTION_INSTALL],
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "LICENSED_ACTIVITY"

    def test_compulsory_insurance_carveout_eligible(self):
        """Licensed activity with compulsory insurance carve-out -> eligible."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            licensed_activity_codes=[LicensedActivityCode.PRIVATE_MEDICAL],
            has_compulsory_insurance_carveout=True,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True

    def test_no_licensed_activity_eligible(self):
        """No licensed activities -> eligible."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            licensed_activity_codes=[],
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True


class TestProductionEmployees:
    """
    Test production + employees rule (218.5.8).
    """

    def test_production_with_many_employees_not_eligible(self):
        """Production with >10 avg quarterly employees -> not eligible (218.5.8)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_production=True,
            avg_quarterly_employees=15,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is False
        assert result.reason_code == "PRODUCTION_EMPLOYEES"

    def test_production_with_few_employees_eligible(self):
        """Production with <=10 avg quarterly employees -> eligible (218.5.8)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_production=True,
            avg_quarterly_employees=8,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True

    def test_non_production_with_many_employees_eligible(self):
        """Non-production with many employees -> eligible."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            does_production=False,
            avg_quarterly_employees=50,
            turnover=TurnoverInput(gross_turnover_12m=Decimal("100000")),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
