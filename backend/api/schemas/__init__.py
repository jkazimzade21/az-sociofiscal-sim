"""
API Schemas for the Simplified Tax Calculator.
"""

from .requests import (
    EvaluateRequest,
    TurnoverInputSchema,
    PropertyTransferInputSchema,
    InterviewAnswerRequest,
)
from .responses import (
    EvaluateResponse,
    QuestionResponse,
    QuestionOption,
    InterviewStateResponse,
    LegalBasisResponse,
)

__all__ = [
    "EvaluateRequest",
    "TurnoverInputSchema",
    "PropertyTransferInputSchema",
    "InterviewAnswerRequest",
    "EvaluateResponse",
    "QuestionResponse",
    "QuestionOption",
    "InterviewStateResponse",
    "LegalBasisResponse",
]
