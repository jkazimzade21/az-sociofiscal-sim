"""
Licensed activities list from the License Law Annex 1.

PATCH 3 implementation: Licensed activity knowledge gap

Legal basis:
- Tax Code Article 218.5.13: Licensed activities are disqualified
- License Law Annex 1: https://president.az/az/documents/licenses

This module provides the comprehensive list of licensed activities
that users can select from, resolving the knowledge gap about what
constitutes a "licensed activity" in Azerbaijan.
"""

from typing import Dict, List, TypedDict


class LicensedActivity(TypedDict):
    """Licensed activity definition with bilingual names."""
    code: str
    name_az: str
    name_en: str
    category: str
    disqualifies: bool  # Whether it disqualifies from simplified tax


# =============================================================================
# LICENSED ACTIVITY CATEGORIES
# From "Lisenziyalar və icazələr haqqında" Law, Annex 1
# =============================================================================
LICENSED_ACTIVITY_CATEGORIES: Dict[str, str] = {
    "healthcare": "Səhiyyə sahəsi / Healthcare",
    "education": "Təhsil sahəsi / Education",
    "communications": "Rabitə sahəsi / Communications",
    "construction": "Tikinti sahəsi / Construction",
    "financial": "Maliyyə sahəsi / Financial",
    "security": "Təhlükəsizlik sahəsi / Security",
    "professional": "Peşəkar xidmətlər / Professional Services",
    "manufacturing": "İstehsal sahəsi / Manufacturing",
    "transport": "Nəqliyyat sahəsi / Transport",
    "other": "Digər / Other",
}


# =============================================================================
# LICENSED ACTIVITIES - FULL LIST
# Source: https://president.az/az/documents/licenses (Annex 1)
#
# Note: This is a representative subset. The full Annex 1 contains
# additional specialized activities.
# =============================================================================
LICENSED_ACTIVITIES: List[LicensedActivity] = [
    # Healthcare
    {
        "code": "private_medical",
        "name_az": "Özəl tibb fəaliyyəti",
        "name_en": "Private medical activity",
        "category": "healthcare",
        "disqualifies": True,
    },
    {
        "code": "pharmaceutical",
        "name_az": "Əczaçılıq fəaliyyəti",
        "name_en": "Pharmaceutical activity",
        "category": "healthcare",
        "disqualifies": True,
    },
    {
        "code": "veterinary",
        "name_az": "Baytarlıq fəaliyyəti",
        "name_en": "Veterinary activity",
        "category": "healthcare",
        "disqualifies": True,
    },
    {
        "code": "medical_equipment",
        "name_az": "Tibbi avadanlıqların istehsalı və satışı",
        "name_en": "Medical equipment production and sales",
        "category": "healthcare",
        "disqualifies": True,
    },

    # Education
    {
        "code": "education",
        "name_az": "Təhsil fəaliyyəti (ali, orta ixtisas, peşə)",
        "name_en": "Education activity (higher, secondary, vocational)",
        "category": "education",
        "disqualifies": True,
    },
    {
        "code": "driving_school",
        "name_az": "Sürücülük kursları",
        "name_en": "Driving schools",
        "category": "education",
        "disqualifies": True,
    },

    # Communications
    {
        "code": "telecom",
        "name_az": "Telekommunikasiya xidmətləri",
        "name_en": "Telecommunication services",
        "category": "communications",
        "disqualifies": True,
    },
    {
        "code": "postal",
        "name_az": "Poçt rabitəsi xidmətləri",
        "name_en": "Postal communication services",
        "category": "communications",
        "disqualifies": True,
    },
    {
        "code": "broadcasting",
        "name_az": "Televiziya və radio yayımı",
        "name_en": "Television and radio broadcasting",
        "category": "communications",
        "disqualifies": True,
    },

    # Construction (permit-required buildings)
    {
        "code": "construction_survey",
        "name_az": "Tikintisinə icazə tələb olunan bina və qurğuların mühəndis axtarışları",
        "name_en": "Engineering surveys for permit-required buildings",
        "category": "construction",
        "disqualifies": True,
    },
    {
        "code": "construction_install",
        "name_az": "Tikintisinə icazə tələb olunan bina və qurğuların tikinti-quraşdırma işləri",
        "name_en": "Construction-installation works for permit-required buildings",
        "category": "construction",
        "disqualifies": True,
    },
    {
        "code": "construction_design",
        "name_az": "Tikintisinə icazə tələb olunan bina və qurğuların layihələndirilməsi",
        "name_en": "Design of permit-required buildings",
        "category": "construction",
        "disqualifies": True,
    },

    # Financial Services
    {
        "code": "banking",
        "name_az": "Bank fəaliyyəti",
        "name_en": "Banking activity",
        "category": "financial",
        "disqualifies": True,
    },
    {
        "code": "insurance",
        "name_az": "Sığorta fəaliyyəti",
        "name_en": "Insurance activity",
        "category": "financial",
        "disqualifies": True,
    },
    {
        "code": "securities",
        "name_az": "Qiymətli kağızlar bazarında peşəkar fəaliyyət",
        "name_en": "Professional activity in securities market",
        "category": "financial",
        "disqualifies": True,
    },
    {
        "code": "auditing",
        "name_az": "Audit xidməti",
        "name_en": "Auditing services",
        "category": "financial",
        "disqualifies": True,
    },

    # Security
    {
        "code": "fire_protection",
        "name_az": "Yanğından mühafizə fəaliyyəti",
        "name_en": "Fire protection activity",
        "category": "security",
        "disqualifies": True,
    },
    {
        "code": "security_services",
        "name_az": "Özəl mühafizə fəaliyyəti",
        "name_en": "Private security services",
        "category": "security",
        "disqualifies": True,
    },
    {
        "code": "detective",
        "name_az": "Özəl detektiv fəaliyyəti",
        "name_en": "Private detective activity",
        "category": "security",
        "disqualifies": True,
    },

    # Professional Services
    {
        "code": "notary",
        "name_az": "Notariat fəaliyyəti",
        "name_en": "Notary activity",
        "category": "professional",
        "disqualifies": True,
    },
    {
        "code": "legal_services",
        "name_az": "Vəkillik fəaliyyəti",
        "name_en": "Legal services / Advocacy",
        "category": "professional",
        "disqualifies": True,
    },
    {
        "code": "customs_broker",
        "name_az": "Gömrük brokeri fəaliyyəti",
        "name_en": "Customs broker activity",
        "category": "professional",
        "disqualifies": True,
    },
    {
        "code": "appraisal",
        "name_az": "Qiymətləndirmə fəaliyyəti",
        "name_en": "Appraisal/Valuation activity",
        "category": "professional",
        "disqualifies": True,
    },

    # Manufacturing (excise-related often)
    {
        "code": "alcohol_production",
        "name_az": "Spirtli içkilərin istehsalı",
        "name_en": "Alcoholic beverages production",
        "category": "manufacturing",
        "disqualifies": True,
    },
    {
        "code": "tobacco_production",
        "name_az": "Tütün məmulatlarının istehsalı",
        "name_en": "Tobacco products production",
        "category": "manufacturing",
        "disqualifies": True,
    },
    {
        "code": "weapons",
        "name_az": "Silah və döyüş sursatının istehsalı və satışı",
        "name_en": "Weapons and ammunition production/sales",
        "category": "manufacturing",
        "disqualifies": True,
    },
    {
        "code": "explosives",
        "name_az": "Partlayıcı maddələrin istehsalı və satışı",
        "name_en": "Explosives production and sales",
        "category": "manufacturing",
        "disqualifies": True,
    },

    # Transport
    {
        "code": "aviation",
        "name_az": "Aviasiya fəaliyyəti",
        "name_en": "Aviation activity",
        "category": "transport",
        "disqualifies": True,
    },
    {
        "code": "maritime",
        "name_az": "Dəniz nəqliyyatı fəaliyyəti",
        "name_en": "Maritime transport activity",
        "category": "transport",
        "disqualifies": True,
    },
    {
        "code": "dangerous_goods",
        "name_az": "Təhlükəli yüklərin daşınması",
        "name_en": "Dangerous goods transportation",
        "category": "transport",
        "disqualifies": True,
    },

    # Gambling (separate regime)
    {
        "code": "gambling",
        "name_az": "Qumar oyunlarının təşkili",
        "name_en": "Gambling organization",
        "category": "other",
        "disqualifies": True,
    },
    {
        "code": "lottery",
        "name_az": "Lotereya fəaliyyəti",
        "name_en": "Lottery activity",
        "category": "other",
        "disqualifies": True,
    },

    # Other
    {
        "code": "tourism",
        "name_az": "Turizm fəaliyyəti",
        "name_en": "Tourism activity",
        "category": "other",
        "disqualifies": True,
    },
    {
        "code": "employment_agency",
        "name_az": "Məşğulluq agentliyi fəaliyyəti",
        "name_en": "Employment agency activity",
        "category": "other",
        "disqualifies": True,
    },
    {
        "code": "geological",
        "name_az": "Geoloji fəaliyyət",
        "name_en": "Geological activity",
        "category": "other",
        "disqualifies": True,
    },
]


def get_licensed_activities_by_category(category: str) -> List[LicensedActivity]:
    """Get licensed activities filtered by category."""
    return [
        activity for activity in LICENSED_ACTIVITIES
        if activity["category"] == category
    ]


def get_disqualifying_activities() -> List[LicensedActivity]:
    """Get only activities that disqualify from simplified tax."""
    return [
        activity for activity in LICENSED_ACTIVITIES
        if activity["disqualifies"]
    ]


def search_licensed_activities(query: str) -> List[LicensedActivity]:
    """
    Search licensed activities by name (Azerbaijani or English).

    Args:
        query: Search string (case-insensitive)

    Returns:
        List of matching activities
    """
    query_lower = query.lower()
    return [
        activity for activity in LICENSED_ACTIVITIES
        if (query_lower in activity["name_az"].lower() or
            query_lower in activity["name_en"].lower())
    ]


# Compulsory insurance carve-out activities
# These activities can still use simplified tax if they ONLY provide
# services under compulsory insurance contracts (icbari sığorta müqavilələri)
COMPULSORY_INSURANCE_CARVEOUT_ELIGIBLE = [
    "private_medical",  # Medical services under mandatory health insurance
    "veterinary",  # Veterinary services under mandatory insurance
]
