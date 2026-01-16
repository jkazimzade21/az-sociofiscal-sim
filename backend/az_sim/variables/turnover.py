"""
Turnover calculation variables.

Legal basis:
- Tax Code Article 218.1.1: 200,000 AZN threshold uses VAT-taxable operations
- Tax Code Article 218.1-1: POS coefficient of 0.5 for non-cash retail/services

PATCH 2 implementation: Turnover definition with VAT-exempt exclusion
and POS coefficient application.
"""

from decimal import Decimal


# Tax Code Article 218.1-1
# "nağdsız qaydada aparılan əməliyyatların həcmi 0,5 əmsalı ilə nəzərə alınır"
POS_COEFFICIENT = Decimal("0.5")


def calculate_vat_taxable_turnover(
    gross_turnover: Decimal,
    vat_exempt_turnover: Decimal
) -> Decimal:
    """
    Calculate VAT-taxable turnover by excluding VAT-exempt operations.

    Legal basis: Tax Code Article 218.1.1
    "vergi tutulan əməliyyatlar həcmi" - VAT-taxable operations

    VAT-exempt categories (Article 164) should be excluded:
    - 164.1.2: Financial services
    - 164.1.8: Textbook production-related publishing/printing
    - etc.

    Args:
        gross_turnover: Total gross turnover for the period
        vat_exempt_turnover: Turnover from VAT-exempt categories

    Returns:
        VAT-taxable turnover amount
    """
    return gross_turnover - vat_exempt_turnover


def calculate_pos_adjusted_turnover(
    vat_taxable_turnover: Decimal,
    pos_retail_turnover: Decimal,
    pos_services_turnover: Decimal
) -> Decimal:
    """
    Apply POS coefficient to calculate adjusted turnover for 200k test.

    Legal basis: Tax Code Article 218.1-1
    "sadələşdirilmiş vergi ödəyicisinin pərakəndə ticarət və əhaliyə
    xidmət göstərilməsi üzrə nağdsız qaydada aparılan əməliyyatların
    həcmi 0,5 əmsalı ilə nəzərə alınır"

    Translation: For simplified taxpayers, non-cash POS operations
    in retail trade and services to the population are counted
    with a coefficient of 0.5.

    Args:
        vat_taxable_turnover: Already VAT-exempt-adjusted turnover
        pos_retail_turnover: POS non-cash retail turnover to unregistered persons
        pos_services_turnover: POS non-cash services turnover to unregistered persons

    Returns:
        Adjusted turnover for the 200,000 AZN threshold test

    Formula:
        pos_eligible = pos_retail + pos_services
        adjusted = vat_taxable - pos_eligible + (pos_eligible × 0.5)
                 = vat_taxable - (pos_eligible × 0.5)
    """
    pos_eligible = pos_retail_turnover + pos_services_turnover

    # Effectively: full turnover minus half of POS eligible amount
    # This is equivalent to counting POS at 0.5 coefficient
    adjusted = vat_taxable_turnover - (pos_eligible * (1 - POS_COEFFICIENT))

    return adjusted
