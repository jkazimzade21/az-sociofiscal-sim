"""
Azerbaijan Simplified Tax Simulation Engine (Pilot)

This module implements the rules-as-code for simplified tax eligibility
and calculation based on the Azerbaijan Tax Code.

Legal Sources:
- Tax Code: https://taxes.gov.az/az/page/vergi-mecellesi
- License Law Annex 1: https://president.az/az/documents/licenses

All rules are traceable to specific article numbers.
"""

__version__ = "0.1.0"

from .entities import TaxpayerInput, EligibilityResult, TaxCalculationResult
from .engine import SimplifiedTaxEngine

__all__ = [
    "TaxpayerInput",
    "EligibilityResult",
    "TaxCalculationResult",
    "SimplifiedTaxEngine",
]
