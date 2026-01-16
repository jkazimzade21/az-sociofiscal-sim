"""
Parameter definitions for the Azerbaijan Simplified Tax Engine.

Parameters are configurable values that may change with legal updates,
including rate tables, zone coefficients, and licensed activity lists.
"""

from .rates import TAX_RATES, ZONE_COEFFICIENTS
from .licensed_activities import LICENSED_ACTIVITIES, LICENSED_ACTIVITY_CATEGORIES

__all__ = [
    "TAX_RATES",
    "ZONE_COEFFICIENTS",
    "LICENSED_ACTIVITIES",
    "LICENSED_ACTIVITY_CATEGORIES",
]
