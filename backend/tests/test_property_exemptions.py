"""
Tests for property transfer exemptions - PATCH 1.

Legal basis:
- Tax Code 218-1.1.5: Property exemptions
- Tax Code 102.1.3.2: Family gift/inheritance exemption
- Tax Code 220.8: Property tax calculation
"""

import pytest
from decimal import Decimal

from az_sim import SimplifiedTaxEngine, TaxpayerInput
from az_sim.entities import (
    PropertyTransferInput,
    PropertyType,
    LocationZone,
)


class TestPropertyExemptions:
    """
    Test property exemption rules (218-1.1.5) - PATCH 1.
    """

    def test_registered_3yr_exempt(self):
        """
        Registered at address for ≥3 years -> exempt (218-1.1.5.1).

        Zero tax should be returned.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("100"),
                location_zone=LocationZone.BAKU_CENTER,
                is_registered_3yr=True,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.tax_amount == Decimal("0")
        assert "3-year registration exemption" in result.exemptions_applied[0]
        assert any(lb.article == "218-1.1.5.1" for lb in result.legal_basis)

    def test_proof_3yr_one_home_exempt(self):
        """
        Proof of 3-year residence + one home -> exempt (218-1.1.5.1-1).

        Zero tax should be returned.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("150"),
                location_zone=LocationZone.BAKU_OTHER,
                has_proof_3yr_one_home=True,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.tax_amount == Decimal("0")
        assert "3-year residence proof" in result.exemptions_applied[0]
        assert any(lb.article == "218-1.1.5.1-1" for lb in result.legal_basis)

    def test_family_gift_inheritance_exempt(self):
        """
        Family gift/inheritance -> exempt (102.1.3.2 via 218-1.1.5.2).

        Zero tax should be returned.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("200"),
                location_zone=LocationZone.SUMGAIT_GANJA_LANKARAN,
                is_family_gift_inheritance=True,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.tax_amount == Decimal("0")
        assert "Family gift/inheritance" in result.exemptions_applied[0]
        assert any(lb.article == "102.1.3.2" for lb in result.legal_basis)


class TestProperty30m2Exemption:
    """
    Test 30 m² exemption for residential property (218-1.1.5.3).
    """

    def test_30m2_exemption_applied(self):
        """
        First 30 m² exempt for residential property (218-1.1.5.3).

        For 100 m² property: only 70 m² taxed.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("100"),
                location_zone=LocationZone.RURAL,  # Coefficient 1.0
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = (100 - 30) m² × 15 AZN × 1.0 = 70 × 15 = 1050 AZN
        assert result.tax_amount == Decimal("1050")
        assert "30 m² exemption" in result.exemptions_applied[0]

    def test_small_property_fully_exempt(self):
        """
        Property ≤30 m² is fully exempt (218-1.1.5.3).
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("25"),
                location_zone=LocationZone.BAKU_CENTER,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = max(0, 25 - 30) × 15 × coef = 0
        assert result.tax_amount == Decimal("0")

    def test_30m2_exemption_not_applied_to_non_residential(self):
        """
        30 m² exemption does NOT apply to non-residential property.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.NON_RESIDENTIAL,
                area_m2=Decimal("100"),
                location_zone=LocationZone.RURAL,  # Coefficient 1.0
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 100 m² × 15 AZN × 1.0 = 1500 AZN (no exemption)
        assert result.tax_amount == Decimal("1500")
        assert len(result.exemptions_applied) == 0


class TestPropertyZoneCoefficients:
    """
    Test zone coefficients for property tax (220.8.1-220.8.4).
    """

    def test_baku_center_coefficient(self):
        """Baku center zone coefficient = 2.5 (220.8.1)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("130"),  # 130 - 30 = 100 taxable
                location_zone=LocationZone.BAKU_CENTER,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 100 m² × 15 AZN × 2.5 = 3750 AZN
        assert result.tax_amount == Decimal("3750")

    def test_baku_other_coefficient(self):
        """Baku other areas coefficient = 2.0 (220.8.2)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("130"),  # 130 - 30 = 100 taxable
                location_zone=LocationZone.BAKU_OTHER,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 100 m² × 15 AZN × 2.0 = 3000 AZN
        assert result.tax_amount == Decimal("3000")

    def test_major_cities_coefficient(self):
        """Sumgait/Ganja/Lankaran coefficient = 1.5 (220.8.3)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("130"),  # 130 - 30 = 100 taxable
                location_zone=LocationZone.SUMGAIT_GANJA_LANKARAN,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 100 m² × 15 AZN × 1.5 = 2250 AZN
        assert result.tax_amount == Decimal("2250")

    def test_other_cities_coefficient(self):
        """Other cities coefficient = 1.2 (220.8.3)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("130"),  # 130 - 30 = 100 taxable
                location_zone=LocationZone.OTHER_CITIES,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 100 m² × 15 AZN × 1.2 = 1800 AZN
        assert result.tax_amount == Decimal("1800")

    def test_rural_coefficient(self):
        """Rural areas coefficient = 1.0 (220.8.4)."""
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("130"),  # 130 - 30 = 100 taxable
                location_zone=LocationZone.RURAL,
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        # Tax = 100 m² × 15 AZN × 1.0 = 1500 AZN
        assert result.tax_amount == Decimal("1500")


class TestPropertyExemptionPriority:
    """
    Test that exemption conditions take priority over calculation.
    """

    def test_exemption_overrides_zone(self):
        """
        Even in high-value Baku center, 3-year registration gives 0 tax.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("500"),  # Large property
                location_zone=LocationZone.BAKU_CENTER,  # Highest coefficient
                is_registered_3yr=True,  # But exempt!
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.tax_amount == Decimal("0")

    def test_multiple_exemptions_first_wins(self):
        """
        If multiple exemption conditions are true, first one applies.
        """
        engine = SimplifiedTaxEngine()
        input_data = TaxpayerInput(
            is_vat_registered=False,
            route_auto_property=True,
            property_transfer=PropertyTransferInput(
                property_type=PropertyType.RESIDENTIAL,
                area_m2=Decimal("100"),
                location_zone=LocationZone.BAKU_OTHER,
                is_registered_3yr=True,
                has_proof_3yr_one_home=True,  # Also true, but first condition wins
            ),
        )
        result = engine.evaluate(input_data)

        assert result.eligible is True
        assert result.tax_amount == Decimal("0")
        # First condition (registered_3yr) should be in exemptions
        assert "218-1.1.5.1" in result.exemptions_applied[0]
