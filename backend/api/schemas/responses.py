"""
Response schemas for the Simplified Tax Calculator API.
"""

from decimal import Decimal
from typing import Optional, List, Literal, Any
from pydantic import BaseModel, Field

from az_sim.entities import TaxRoute


class LegalBasisResponse(BaseModel):
    """Legal reference for traceability."""
    article: str
    description: str
    source_url: str = "https://taxes.gov.az/az/page/vergi-mecellesi"


class QuestionOption(BaseModel):
    """Option for a question with multiple choices."""
    value: str
    label: str
    label_az: Optional[str] = None
    description: Optional[str] = None
    description_az: Optional[str] = None


class QuestionResponse(BaseModel):
    """
    A single question in the interview flow.

    Questions are designed to minimize user burden while gathering
    all required information for tax determination.
    """
    id: str
    type: Literal["boolean", "select", "multi_select", "number", "decimal", "object"]
    question: str
    question_az: str
    tooltip: Optional[str] = None
    tooltip_az: Optional[str] = None
    legal_basis: Optional[str] = None
    options: Optional[List[QuestionOption]] = None
    required: bool = True
    subquestions: Optional[List["QuestionResponse"]] = None
    condition: Optional[str] = None  # When this question should be shown


class InterviewStateResponse(BaseModel):
    """
    Current state of the server-driven interview.

    Either returns the next question or the final result.
    """
    status: Literal["need_more_info", "done"]
    next_question: Optional[QuestionResponse] = None
    progress: Optional[float] = None  # 0-1 progress through interview
    result: Optional["EvaluateResponse"] = None


class EvaluateResponse(BaseModel):
    """
    Complete evaluation response.

    If not eligible: shows only eligibility status and reason code.
    If eligible: shows tax calculation with optional breakdown.
    """
    eligible: bool
    tax_amount: Optional[Decimal] = None
    currency: str = "AZN"
    route: Optional[TaxRoute] = None

    # Tax calculation breakdown
    tax_base: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    exemptions_applied: List[str] = Field(default_factory=list)

    # For not eligible results
    reason_code: Optional[str] = None
    reason_description: Optional[str] = None

    # Legal traceability
    legal_basis: List[LegalBasisResponse] = Field(default_factory=list)

    # Debug trace (only when ?debug=1)
    debug_trace: Optional[List[dict]] = None

    model_config = {"json_schema_extra": {
        "examples": [
            {
                "eligible": True,
                "tax_amount": "3000.00",
                "currency": "AZN",
                "route": "general",
                "tax_base": "150000.00",
                "tax_rate": "0.02",
                "exemptions_applied": [],
                "legal_basis": [
                    {
                        "article": "220.1",
                        "description": "General simplified tax rate of 2%",
                        "source_url": "https://taxes.gov.az/az/page/vergi-mecellesi",
                    }
                ],
            },
            {
                "eligible": False,
                "reason_code": "VAT_REGISTERED",
                "reason_description": "VAT-registered taxpayers cannot use simplified tax regime",
                "legal_basis": [
                    {
                        "article": "218.1.1",
                        "description": "VAT registration disqualifies from simplified tax",
                        "source_url": "https://taxes.gov.az/az/page/vergi-mecellesi",
                    }
                ],
            },
        ]
    }}


class LicensedActivityResponse(BaseModel):
    """Licensed activity for PATCH 3 dropdown."""
    code: str
    name_az: str
    name_en: str
    category: str
    disqualifies: bool


class LicensedActivitiesListResponse(BaseModel):
    """Response with all licensed activities for Q11."""
    activities: List[LicensedActivityResponse]
    categories: dict


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
