"""
Tax rates and zone coefficients.

Legal basis:
- Tax Code Article 220: Simplified tax rates
- Tax Code Article 220.8.1-220.8.4: Zone coefficients for property
"""

from decimal import Decimal
from typing import Dict
from ..entities import TaxRoute, LocationZone


# =============================================================================
# TAX RATES BY ROUTE
# Legal basis: Tax Code Articles 220.1, 220.1-1, 220.8
# =============================================================================
TAX_RATES: Dict[TaxRoute, Dict[str, Decimal]] = {
    # Article 220.1: General simplified tax = 2%
    TaxRoute.GENERAL: {
        "base_rate": Decimal("0.02"),
        "description": "General simplified tax rate (220.1)",
    },

    # Article 220.1-1: Trade/catering over 200k
    TaxRoute.TRADE_CATERING_OVER_200K: {
        "general_rate": Decimal("0.08"),  # 8% general
        "pos_rate": Decimal("0.06"),  # 6% for POS (from 2026-01-01)
        "description": "Trade/catering simplified tax rates (220.1-1)",
    },

    # Article 218.4.1 + 220.4: Passenger transport
    TaxRoute.AUTO_TRANSPORT: {
        "base_rate": Decimal("0.02"),
        "description": "Passenger transport/taxi rate (220.4)",
    },

    # Article 218.4.2 + 220.6: Betting/lottery
    TaxRoute.AUTO_BETTING_LOTTERY: {
        "base_rate": Decimal("0.02"),
        "description": "Betting/lottery rate (220.6)",
    },

    # Article 218.4.3 + 220.8: Property transfer
    TaxRoute.AUTO_PROPERTY: {
        "base_per_m2": Decimal("15"),  # 15 AZN per m²
        "description": "Property transfer rate per m² (220.8)",
    },

    # Article 218.4.5 + 220.8: Land transfer
    TaxRoute.AUTO_LAND: {
        "multiplier": Decimal("2"),  # 2× land tax under 206.1-1
        "description": "Land transfer = 2× land tax (220.8)",
    },

    # Article 218.4.4 + 220.10: Fixed activities
    TaxRoute.AUTO_FIXED_220_10: {
        "fixed_amount": True,  # Uses fixed amounts per activity type
        "description": "Fixed activity amounts (220.10)",
    },
}


# =============================================================================
# ZONE COEFFICIENTS FOR PROPERTY TAX
# Legal basis: Tax Code Article 220.8.1-220.8.4
# =============================================================================
ZONE_COEFFICIENTS: Dict[LocationZone, Decimal] = {
    # Article 220.8.1: Baku center (high-value zones)
    LocationZone.BAKU_CENTER: Decimal("2.5"),

    # Article 220.8.2: Baku other areas
    LocationZone.BAKU_OTHER: Decimal("2.0"),

    # Article 220.8.3: Major cities (Sumgait, Ganja, Lankaran)
    LocationZone.SUMGAIT_GANJA_LANKARAN: Decimal("1.5"),

    # Article 220.8.3: Other cities
    LocationZone.OTHER_CITIES: Decimal("1.2"),

    # Article 220.8.4: Rural areas
    LocationZone.RURAL: Decimal("1.0"),
}


# City classification for zone determination
BAKU_CENTER_DISTRICTS = [
    "Sabail",
    "Yasamal",
    "Nasimi",
    "Nəsimi",
    "Səbail",
]

MAJOR_CITIES = [
    "Sumqayıt",
    "Sumgayit",
    "Gəncə",
    "Ganja",
    "Lənkəran",
    "Lankaran",
]
