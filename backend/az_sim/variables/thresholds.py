"""
Threshold constants for simplified tax eligibility.

All thresholds are defined with their legal basis from the Tax Code.
"""

from decimal import Decimal


# =============================================================================
# Tax Code Article 218.1.1 - Turnover Threshold
# =============================================================================
# "vergi tutulan əməliyyatlar həcmi ardıcıl 12 ayda 200000 manatdan çox olmayan"
TURNOVER_THRESHOLD = Decimal("200000")  # 200,000 AZN


# =============================================================================
# Tax Code Article 218.5.6 - Fixed Assets Threshold
# =============================================================================
# "İlin əvvəlinə əsas vəsaitlərinin qalıq dəyəri 1 000 000 manatdan artıq olan
# vergi ödəyiciləri sadələşdirilmiş vergi ödəyicisi ola bilməz"
FIXED_ASSETS_THRESHOLD = Decimal("1000000")  # 1,000,000 AZN


# =============================================================================
# Tax Code Article 218.5.8 - Production Employee Threshold
# =============================================================================
# "İstehsal fəaliyyəti göstərən və rüblük orta işçi sayı 10 nəfərdən çox olan"
EMPLOYEE_THRESHOLD = 10  # More than 10 employees


# =============================================================================
# Tax Code Articles 218.6.1, 218.6.2 - Exception Ratio Threshold
# =============================================================================
# "elektron qaimə-faktura ilə rəsmiləşdirilən əməliyyatları rüblük
# əməliyyatlarının 30 faizindən çox olmadıqda"
EXCEPTION_RATIO_THRESHOLD = Decimal("0.30")  # 30%


# =============================================================================
# Tax Code Article 220.8 - Property Tax Per Square Meter
# =============================================================================
# "Yaşayış sahəsinin özgəninkiləşdirilməsindən sadələşdirilmiş vergi
# hər 1 kvadratmetr üçün 15 manat"
PROPERTY_TAX_PER_M2 = Decimal("15")  # 15 AZN per m²


# =============================================================================
# Tax Code Article 218-1.1.5.3 - Property Exempt Area
# =============================================================================
# "mülkiyyətində olan yaşayış sahəsinin ilk 30 kvadratmetri vergidən azaddır"
PROPERTY_EXEMPT_AREA_M2 = Decimal("30")  # 30 m²


# =============================================================================
# Tax Code Article 220.1 - General Simplified Tax Rate
# =============================================================================
# "Sadələşdirilmiş verginin dərəcəsi vergi tutulan əməliyyatların həcminin
# 2 faizi"
GENERAL_TAX_RATE = Decimal("0.02")  # 2%


# =============================================================================
# Tax Code Article 220.1-1 - Trade/Catering Rates (>200k turnover)
# =============================================================================
# General rate: 8%
TRADE_CATERING_GENERAL_RATE = Decimal("0.08")  # 8%

# POS rate (effective 2026-01-01 for 3 years): 6%
# "nağdsız ödəmə terminalları ilə təchiz olunmuş vahid KKM-ə inteqrasiya
# edilmiş nəzarət-kassa aparatından istifadə etməklə aparılan əməliyyatlar
# üzrə 6 faiz"
TRADE_CATERING_POS_RATE = Decimal("0.06")  # 6%
