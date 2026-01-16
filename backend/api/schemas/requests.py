"""
Request schemas for the Simplified Tax Calculator API.
"""

from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field

from az_sim.entities import (
    PropertyType,
    LocationZone,
    LicensedActivityCode,
    VATExemptCategory,
)


class TurnoverInputSchema(BaseModel):
    """
    Turnover input for the 200,000 AZN threshold test.

    PATCH 2: Includes structured input for VAT-exempt exclusion
    and POS coefficient calculation.
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
    vat_exempt_categories: List[VATExemptCategory] = Field(
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

    model_config = {"json_schema_extra": {
        "example": {
            "gross_turnover_12m": 150000,
            "vat_exempt_turnover_12m": 10000,
            "vat_exempt_categories": ["financial_services"],
            "pos_retail_nonregistered_12m": 50000,
            "pos_services_nonregistered_12m": 20000,
        }
    }}


class PropertyTransferInputSchema(BaseModel):
    """
    Property transfer details for 218.4.3 route.

    PATCH 1: Includes exemption condition questions.
    """
    property_type: PropertyType
    area_m2: Decimal = Field(..., gt=0, description="Property area in square meters")
    location_zone: LocationZone

    # Exemption conditions (PATCH 1)
    is_registered_3yr: bool = Field(
        default=False,
        description="Was registered at the property address for at least 3 calendar years (218-1.1.5.1)"
    )
    has_proof_3yr_one_home: bool = Field(
        default=False,
        description="Has proof of 3-year residence AND owns only one residential property (218-1.1.5.1-1)"
    )
    is_family_gift_inheritance: bool = Field(
        default=False,
        description="Property received as gift/inheritance from family member (102.1.3.2)"
    )

    model_config = {"json_schema_extra": {
        "example": {
            "property_type": "residential",
            "area_m2": 85,
            "location_zone": "baku_other",
            "is_registered_3yr": False,
            "has_proof_3yr_one_home": False,
            "is_family_gift_inheritance": False,
        }
    }}


class EvaluateRequest(BaseModel):
    """
    Full evaluation request for simplified tax eligibility and calculation.

    This schema supports both complete input and partial input
    for the server-driven interview mode.
    """
    # Q1: VAT registration
    is_vat_registered: Optional[bool] = None

    # Q2: Automatic routes (218.4)
    route_auto_transport: bool = False
    route_auto_betting_lottery: bool = False
    route_auto_property: bool = False
    route_auto_fixed_220_10: bool = False
    route_auto_land: bool = False

    # Property transfer details (if route_auto_property)
    property_transfer: Optional[PropertyTransferInputSchema] = None

    # Q3: Trade/catering activity
    does_trade: bool = False
    does_catering: bool = False

    # Q4: Turnover (PATCH 2)
    turnover: Optional[TurnoverInputSchema] = None

    # Q5: Excise/mandatory marking production
    produces_excise_goods: bool = False

    # Q6: Financial sector
    is_credit_org: bool = False
    is_insurance_market_participant: bool = False
    is_investment_fund: bool = False
    is_securities_licensed: bool = False
    is_pawnshop: bool = False

    # Q7: Pension fund
    is_non_state_pension_fund: bool = False

    # Q8: Rental/royalty income
    has_rental_income: bool = False
    has_royalty_income: bool = False

    # Q9: Natural monopoly
    is_natural_monopoly: bool = False

    # Q10: Fixed assets
    fixed_assets_residual_value: Optional[Decimal] = None

    # Q11: Licensed activities (PATCH 3)
    licensed_activity_codes: List[LicensedActivityCode] = Field(default_factory=list)
    has_compulsory_insurance_carveout: bool = False

    # Q12: Production + employees
    does_production: bool = False
    avg_quarterly_employees: Optional[int] = None

    # Q13: Wholesale
    does_wholesale: bool = False
    wholesale_einvoice_ratio: Optional[Decimal] = None

    # Q14: B2B works/services
    does_b2b_works_services: bool = False
    b2b_einvoice_ratio: Optional[Decimal] = None

    # Q15: Precious goods / fur
    sells_gold_jewelry_diamonds: bool = False
    sells_fur_leather: bool = False

    # Additional
    is_public_legal_entity: bool = False

    model_config = {"json_schema_extra": {
        "example": {
            "is_vat_registered": False,
            "does_trade": True,
            "turnover": {
                "gross_turnover_12m": 150000,
                "vat_exempt_turnover_12m": 0,
                "pos_retail_nonregistered_12m": 50000,
                "pos_services_nonregistered_12m": 0,
            },
        }
    }}


class InterviewAnswerRequest(BaseModel):
    """
    Request for answering a single interview question.

    Used in the server-driven interview mode.
    """
    question_id: str
    answer: dict = Field(
        ...,
        description="Answer data specific to the question type"
    )

    model_config = {"json_schema_extra": {
        "example": {
            "question_id": "vat_registration",
            "answer": {"is_vat_registered": False},
        }
    }}
