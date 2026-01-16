"""
Simplified Tax API Routes.

Endpoints for tax eligibility evaluation and server-driven interview.
"""

from typing import List
from fastapi import APIRouter, Query

from ..schemas.requests import EvaluateRequest
from ..schemas.responses import (
    EvaluateResponse,
    QuestionResponse,
    LicensedActivityResponse,
    LicensedActivitiesListResponse,
)
from ..services.evaluation import EvaluationService
from ..services.interview import InterviewService
from az_sim.parameters.licensed_activities import (
    LICENSED_ACTIVITIES,
    LICENSED_ACTIVITY_CATEGORIES,
)

router = APIRouter(prefix="/api/v1/simplified-tax", tags=["Simplified Tax"])


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_simplified_tax(
    request: EvaluateRequest,
    debug: bool = Query(default=False, description="Enable debug trace in response"),
) -> EvaluateResponse:
    """
    Evaluate simplified tax eligibility and calculate tax amount.

    This endpoint accepts full input and returns:
    - If eligible: tax amount, route, and calculation breakdown
    - If not eligible: reason code and description

    Use `?debug=1` to include the full rule evaluation trace.
    """
    service = EvaluationService(debug=debug)
    return service.evaluate(request)


@router.get("/questions", response_model=List[QuestionResponse])
async def get_interview_questions() -> List[QuestionResponse]:
    """
    Get all interview questions for the simplified tax assessment.

    Questions are ordered by the interview flow, with early exit
    questions first. Each question includes:
    - Bilingual text (English and Azerbaijani)
    - Tooltip with legal context
    - Legal basis reference
    - Conditional display rules
    """
    service = InterviewService()
    return service.get_questions()


@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str) -> QuestionResponse:
    """
    Get a specific interview question by ID.
    """
    service = InterviewService()
    question = service.get_question_by_id(question_id)
    if not question:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")
    return question


@router.get("/licensed-activities", response_model=LicensedActivitiesListResponse)
async def get_licensed_activities(
    search: str = Query(default=None, description="Search query for activities"),
    category: str = Query(default=None, description="Filter by category"),
) -> LicensedActivitiesListResponse:
    """
    Get the list of licensed activities for Q11 (PATCH 3).

    This endpoint provides the comprehensive list of licensed activities
    from the License Law Annex 1, which users need to identify whether
    their activity requires a license.
    """
    activities = LICENSED_ACTIVITIES

    # Apply search filter
    if search:
        search_lower = search.lower()
        activities = [
            a for a in activities
            if search_lower in a["name_az"].lower() or search_lower in a["name_en"].lower()
        ]

    # Apply category filter
    if category:
        activities = [a for a in activities if a["category"] == category]

    return LicensedActivitiesListResponse(
        activities=[
            LicensedActivityResponse(
                code=a["code"],
                name_az=a["name_az"],
                name_en=a["name_en"],
                category=a["category"],
                disqualifies=a["disqualifies"],
            )
            for a in activities
        ],
        categories=LICENSED_ACTIVITY_CATEGORIES,
    )
