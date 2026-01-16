"""
Variable definitions for the Azerbaijan Simplified Tax Engine.

Variables represent the inputs and intermediate values used in
tax calculations, with full legal traceability.
"""

from .turnover import (
    calculate_vat_taxable_turnover,
    calculate_pos_adjusted_turnover,
)
from .thresholds import (
    TURNOVER_THRESHOLD,
    FIXED_ASSETS_THRESHOLD,
    EMPLOYEE_THRESHOLD,
    EXCEPTION_RATIO_THRESHOLD,
)

__all__ = [
    "calculate_vat_taxable_turnover",
    "calculate_pos_adjusted_turnover",
    "TURNOVER_THRESHOLD",
    "FIXED_ASSETS_THRESHOLD",
    "EMPLOYEE_THRESHOLD",
    "EXCEPTION_RATIO_THRESHOLD",
]
