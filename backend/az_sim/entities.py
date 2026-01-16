"""
Entity definitions for the Azerbaijan Simplified Tax Engine.

These Pydantic models represent the input data, eligibility results,
and tax calculation outputs with full legal traceability.
"""

from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TaxRoute(str, Enum):
    """
    Simplified tax route types based on Tax Code Article 218.4 and 218.1.

    Legal basis: Tax Code Article 218
    Source: https://taxes.gov.az/az/page/vergi-mecellesi
    """
    GENERAL = "general"  # Standard simplified tax (218.1.1)
    TRADE_CATERING_OVER_200K = "trade_catering_over_200k"  # 218.1.2
    AUTO_TRANSPORT = "auto_transport"  # 218.4.1 - Passenger transport/taxi
    AUTO_BETTING_LOTTERY = "auto_betting_lottery"  # 218.4.2
    AUTO_PROPERTY = "auto_property"  # 218.4.3 - Own real estate sale
    AUTO_LAND = "auto_land"  # 218.4.5 - Own land sale
    AUTO_FIXED_220_10 = "auto_fixed_220_10"  # 218.4.4 - Fixed activity without employees


class PropertyType(str, Enum):
    """Property type for real estate transfers (218.4.3)."""
    RESIDENTIAL = "residential"
    NON_RESIDENTIAL = "non_residential"


class LocationZone(str, Enum):
    """
    Location zones for property tax calculation.

    Legal basis: Tax Code Article 220.8.1-220.8.4
    """
    BAKU_CENTER = "baku_center"  # Zone 1
    BAKU_OTHER = "baku_other"  # Zone 2
    SUMGAIT_GANJA_LANKARAN = "sumgait_ganja_lankaran"
    OTHER_CITIES = "other_cities"
    RURAL = "rural"


class LicensedActivityCode(str, Enum):
    """
    Licensed activity codes from the License Law Annex 1.

    Legal basis: "Lisenziyalar və icazələr haqqında" Law, Annex 1
    Source: https://president.az/az/documents/licenses
    """
    PRIVATE_MEDICAL = "private_medical"  # Özəl tibb fəaliyyəti
    EDUCATION = "education"  # Təhsil fəaliyyəti
    COMMUNICATIONS = "communications"  # Rabitə xidmətləri
    FIRE_PROTECTION = "fire_protection"  # Yanğından mühafizə fəaliyyəti
    CONSTRUCTION_SURVEY = "construction_survey"  # Engineering surveys
    CONSTRUCTION_INSTALL = "construction_install"  # Construction-installation
    CONSTRUCTION_DESIGN = "construction_design"  # Design work
    PHARMACEUTICAL = "pharmaceutical"  # Əczaçılıq fəaliyyəti
    VETERINARY = "veterinary"  # Baytarlıq fəaliyyəti
    AUDITING = "auditing"  # Audit xidməti
    NOTARY = "notary"  # Notariat fəaliyyəti
    LEGAL_SERVICES = "legal_services"  # Vəkillik fəaliyyəti
    SECURITY_SERVICES = "security_services"  # Mühafizə fəaliyyəti
    GAMBLING = "gambling"  # Qumar oyunları
    ALCOHOL_PRODUCTION = "alcohol_production"  # Spirtli içkilər istehsalı
    TOBACCO_PRODUCTION = "tobacco_production"  # Tütün məmulatları istehsalı
    BANKING = "banking"  # Bank fəaliyyəti
    INSURANCE = "insurance"  # Sığorta fəaliyyəti
    SECURITIES = "securities"  # Qiymətli kağızlar bazarı
    OTHER = "other"


class VATExemptCategory(str, Enum):
    """
    VAT-exempt categories under Tax Code Article 164.

    Legal basis: Tax Code Article 164
    """
    FINANCIAL_SERVICES = "financial_services"  # 164.1.2
    TEXTBOOK_PUBLISHING = "textbook_publishing"  # 164.1.8
    MEDICAL_SERVICES = "medical_services"  # 164.1.3
    EDUCATION_SERVICES = "education_services"  # 164.1.4
    INSURANCE_SERVICES = "insurance_services"  # 164.1.5
    OTHER = "other"


class TurnoverInput(BaseModel):
    """
    Turnover input for the 200,000 AZN threshold test.

    Legal basis: Tax Code Articles 218.1.1, 218.1-1
    - The test uses VAT-taxable operations ("vergi tutulan əməliyyatlar həcmi")
    - POS non-cash turnover from retail/services to unregistered persons
      is counted with coefficient 0.5 (218.1-1)
    """
    gross_turnover_12m: Decimal = Field(
        ...,
        ge=0,
        description="Total gross turnover for last 12 consecutive months (AZN)"
    )
    vat_exempt_turnover_12m: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        description="VAT-exempt turnover under Article 164 (AZN)"
    )
    vat_exempt_categories: list[VATExemptCategory] = Field(
        default_factory=list,
        description="Categories of VAT-exempt operations"
    )
    pos_retail_nonregistered_12m: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        description="POS non-cash retail turnover to unregistered persons (AZN)"
    )
    pos_services_nonregistered_12m: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        description="POS non-cash services turnover to unregistered persons (AZN)"
    )


class PropertyTransferInput(BaseModel):
    """
    Property transfer details for 218.4.3 route.

    Legal basis: Tax Code Articles 218.4.3, 218-1.1.5, 220.8
    """
    property_type: PropertyType
    area_m2: Decimal = Field(..., gt=0, description="Property area in square meters")
    location_zone: LocationZone

    # Exemption conditions (PATCH 1)
    # 218-1.1.5.1: Registered at address for ≥3 calendar years
    is_registered_3yr: bool = Field(
        default=False,
        description="Was registered at the property address for at least 3 calendar years"
    )
    # 218-1.1.5.1-1: Proof of residence ≥3 years AND owns only one residential property
    has_proof_3yr_one_home: bool = Field(
        default=False,
        description="Has proof of 3-year residence AND owns only one residential property"
    )
    # 218-1.1.5.2 references 102.1.3.2: Family gift/inheritance
    is_family_gift_inheritance: bool = Field(
        default=False,
        description="Property received as gift/inheritance from family member (102.1.3.2)"
    )


class TaxpayerInput(BaseModel):
    """
    Complete taxpayer input for simplified tax evaluation.

    This model supports both the full input mode and the
    server-driven interview mode (partial input).
    """
    # Q1: VAT registration (hard stop)
    # Legal basis: Tax Code 218.1.1 references Chapter XI
    is_vat_registered: Optional[bool] = Field(
        default=None,
        description="Is the taxpayer registered for VAT?"
    )

    # Q2: Route selection (fast pass - 218.4)
    route_auto_transport: bool = Field(
        default=False,
        description="Passenger transport/taxi activity (218.4.1)"
    )
    route_auto_betting_lottery: bool = Field(
        default=False,
        description="Betting/lottery activity (218.4.2)"
    )
    route_auto_property: bool = Field(
        default=False,
        description="Transfer/sale of own real estate (218.4.3)"
    )
    route_auto_fixed_220_10: bool = Field(
        default=False,
        description="Fixed activity under 220.10 without employees (218.4.4)"
    )
    route_auto_land: bool = Field(
        default=False,
        description="Sale/transfer of own land (218.4.5)"
    )

    # Property transfer details (if route_auto_property)
    property_transfer: Optional[PropertyTransferInput] = None

    # Q3: Trade/catering activity
    does_trade: bool = Field(
        default=False,
        description="Engaged in trade activity"
    )
    does_catering: bool = Field(
        default=False,
        description="Engaged in public catering activity"
    )

    # Q4: Turnover (PATCH 2)
    turnover: Optional[TurnoverInput] = None

    # Q5: Excise/mandatory marking production (218.5.1)
    produces_excise_goods: bool = Field(
        default=False,
        description="Produces excise or mandatory-label goods"
    )

    # Q6: Financial sector (218.5.2)
    is_credit_org: bool = Field(
        default=False,
        description="Is a credit organization"
    )
    is_insurance_market_participant: bool = Field(
        default=False,
        description="Is an insurance market professional participant"
    )
    is_investment_fund: bool = Field(
        default=False,
        description="Is an investment fund or manager"
    )
    is_securities_licensed: bool = Field(
        default=False,
        description="Is licensed for securities market activities"
    )
    is_pawnshop: bool = Field(
        default=False,
        description="Is a pawnshop"
    )

    # Q7: Pension fund (218.5.3)
    is_non_state_pension_fund: bool = Field(
        default=False,
        description="Is a non-state pension fund"
    )

    # Q8: Rental/royalty income (218.5.4)
    has_rental_income: bool = Field(
        default=False,
        description="Has rental income"
    )
    has_royalty_income: bool = Field(
        default=False,
        description="Has royalty income"
    )

    # Q9: Natural monopoly (218.5.5)
    is_natural_monopoly: bool = Field(
        default=False,
        description="Is a designated natural monopoly"
    )

    # Q10: Fixed assets (218.5.6)
    fixed_assets_residual_value: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Fixed assets residual value at start of year (AZN)"
    )

    # Q11: Licensed activities (PATCH 3 - 218.5.13)
    licensed_activity_codes: list[LicensedActivityCode] = Field(
        default_factory=list,
        description="Licensed activities from Annex 1 list"
    )
    has_compulsory_insurance_carveout: bool = Field(
        default=False,
        description="Only provides services under compulsory insurance contracts (icbari sığorta)"
    )

    # Q12: Production + employees (218.5.8)
    does_production: bool = Field(
        default=False,
        description="Conducts production activity"
    )
    avg_quarterly_employees: Optional[int] = Field(
        default=None,
        ge=0,
        description="Average quarterly employee count"
    )

    # Q13: Wholesale (218.5.9 + 218.6.1)
    does_wholesale: bool = Field(
        default=False,
        description="Conducts wholesale trade"
    )
    wholesale_einvoice_ratio: Optional[Decimal] = Field(
        default=None,
        ge=0,
        le=1,
        description="Ratio of e-invoiced wholesale ops to total quarterly trade ops"
    )

    # Q14: B2B works/services (218.5.10 + 218.6.2)
    does_b2b_works_services: bool = Field(
        default=False,
        description="Performs works/services for legal entities or registered individuals"
    )
    b2b_einvoice_ratio: Optional[Decimal] = Field(
        default=None,
        ge=0,
        le=1,
        description="Ratio of e-invoiced B2B ops to total quarterly works/services ops"
    )

    # Q15: Precious goods / fur (218.5.11, 218.5.12)
    sells_gold_jewelry_diamonds: bool = Field(
        default=False,
        description="Sells gold, jewelry, or diamonds"
    )
    sells_fur_leather: bool = Field(
        default=False,
        description="Sells fur or leather products"
    )

    # Additional disqualifiers
    is_public_legal_entity: bool = Field(
        default=False,
        description="Is a public legal entity (218.5.7)"
    )


class LegalBasis(BaseModel):
    """Reference to legal source for traceability."""
    article: str
    description: str
    source_url: str = "https://taxes.gov.az/az/page/vergi-mecellesi"


class EligibilityResult(BaseModel):
    """
    Result of simplified tax eligibility evaluation.

    If not eligible, reason_code and legal_basis explain why.
    """
    eligible: bool
    reason_code: Optional[str] = None
    reason_description: Optional[str] = None
    legal_basis: list[LegalBasis] = Field(default_factory=list)
    route: Optional[TaxRoute] = None

    # For debug mode
    evaluation_trace: list[dict] = Field(default_factory=list)


class TaxCalculationResult(BaseModel):
    """
    Complete result including eligibility and tax calculation.
    """
    eligible: bool
    tax_amount: Optional[Decimal] = None
    currency: str = "AZN"
    route: Optional[TaxRoute] = None

    # Breakdown for eligible results
    tax_base: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    exemptions_applied: list[str] = Field(default_factory=list)

    # For not eligible results
    reason_code: Optional[str] = None
    reason_description: Optional[str] = None

    # Legal traceability
    legal_basis: list[LegalBasis] = Field(default_factory=list)

    # Debug trace (only populated when debug=True)
    debug_trace: Optional[list[dict]] = None
