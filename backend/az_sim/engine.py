"""
Simplified Tax Engine - Core Rules Implementation

This module implements the rules-as-code for Azerbaijan simplified tax.
Every rule is linked to its legal citation for full traceability.

Legal Sources:
- Tax Code: https://taxes.gov.az/az/page/vergi-mecellesi
- License Law: https://president.az/az/documents/licenses
"""

from decimal import Decimal
from typing import Optional
from .entities import (
    TaxpayerInput,
    EligibilityResult,
    TaxCalculationResult,
    TaxRoute,
    LegalBasis,
    PropertyType,
    LocationZone,
    LicensedActivityCode,
)


# =============================================================================
# LEGAL CONSTANTS
# =============================================================================

# Tax Code Article 218.1.1 - Turnover threshold
TURNOVER_THRESHOLD_AZN = Decimal("200000")

# Tax Code Article 218.1-1 - POS coefficient
POS_COEFFICIENT = Decimal("0.5")

# Tax Code Article 218.5.6 - Fixed assets threshold
FIXED_ASSETS_THRESHOLD_AZN = Decimal("1000000")

# Tax Code Article 218.5.8 - Production employee threshold
PRODUCTION_EMPLOYEE_THRESHOLD = 10

# Tax Code Articles 218.6.1, 218.6.2 - Exception ratio threshold
EXCEPTION_RATIO_THRESHOLD = Decimal("0.30")

# Tax Code Article 220.1 - General simplified tax rate
GENERAL_SIMPLIFIED_RATE = Decimal("0.02")  # 2%

# Tax Code Article 220.1-1 - Trade/catering over 200k rates
TRADE_CATERING_GENERAL_RATE = Decimal("0.08")  # 8%
TRADE_CATERING_POS_RATE = Decimal("0.06")  # 6% (effective 2026-01-01 for 3 years)

# Tax Code Article 220.8 - Property transfer base rate per m²
PROPERTY_TAX_BASE_RATE_PER_M2 = Decimal("15")  # 15 AZN per m²

# Tax Code Article 218-1.1.5.3 - Property exemption area
PROPERTY_EXEMPT_AREA_M2 = Decimal("30")

# Zone coefficients for property tax (220.8.1-220.8.4)
ZONE_COEFFICIENTS = {
    LocationZone.BAKU_CENTER: Decimal("2.5"),
    LocationZone.BAKU_OTHER: Decimal("2.0"),
    LocationZone.SUMGAIT_GANJA_LANKARAN: Decimal("1.5"),
    LocationZone.OTHER_CITIES: Decimal("1.2"),
    LocationZone.RURAL: Decimal("1.0"),
}

# Licensed activities that disqualify (218.5.13)
# Unless compulsory insurance carve-out applies
DISQUALIFYING_LICENSED_ACTIVITIES = {
    LicensedActivityCode.PRIVATE_MEDICAL,
    LicensedActivityCode.EDUCATION,
    LicensedActivityCode.COMMUNICATIONS,
    LicensedActivityCode.FIRE_PROTECTION,
    LicensedActivityCode.CONSTRUCTION_SURVEY,
    LicensedActivityCode.CONSTRUCTION_INSTALL,
    LicensedActivityCode.CONSTRUCTION_DESIGN,
    LicensedActivityCode.PHARMACEUTICAL,
    LicensedActivityCode.VETERINARY,
    LicensedActivityCode.AUDITING,
    LicensedActivityCode.NOTARY,
    LicensedActivityCode.LEGAL_SERVICES,
    LicensedActivityCode.SECURITY_SERVICES,
    LicensedActivityCode.GAMBLING,
    LicensedActivityCode.ALCOHOL_PRODUCTION,
    LicensedActivityCode.TOBACCO_PRODUCTION,
    LicensedActivityCode.BANKING,
    LicensedActivityCode.INSURANCE,
    LicensedActivityCode.SECURITIES,
    LicensedActivityCode.OTHER,
}


class SimplifiedTaxEngine:
    """
    Core engine for simplified tax eligibility and calculation.

    All methods include legal basis references for traceability.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self._trace: list[dict] = []

    def _log_trace(self, rule: str, result: bool, details: str, article: str) -> None:
        """Log evaluation trace for debugging."""
        if self.debug:
            self._trace.append({
                "rule": rule,
                "result": result,
                "details": details,
                "article": article,
            })

    def evaluate(self, input_data: TaxpayerInput) -> TaxCalculationResult:
        """
        Main entry point: evaluate eligibility and calculate tax.

        Returns complete result with legal traceability.
        """
        self._trace = []

        # Step 1: Check eligibility
        eligibility = self._check_eligibility(input_data)

        if not eligibility.eligible:
            return TaxCalculationResult(
                eligible=False,
                reason_code=eligibility.reason_code,
                reason_description=eligibility.reason_description,
                legal_basis=eligibility.legal_basis,
                debug_trace=self._trace if self.debug else None,
            )

        # Step 2: Calculate tax based on route
        tax_result = self._calculate_tax(input_data, eligibility.route)
        tax_result.debug_trace = self._trace if self.debug else None

        return tax_result

    def _check_eligibility(self, input_data: TaxpayerInput) -> EligibilityResult:
        """
        Check all eligibility conditions in order.

        The order follows the interview flow for early exit optimization.
        """
        legal_basis: list[LegalBasis] = []

        # =================================================================
        # Q1: VAT REGISTRATION CHECK (HARD STOP)
        # Legal basis: Tax Code 218.1.1 - references Chapter XI
        # "sadələşdirilmiş vergi ödəyicisi kimi qeydiyyata alınmış vergi
        # ödəyicilərinin əməliyyatları VAT-a cəlb edilmir" (218.1.1)
        # =================================================================
        if input_data.is_vat_registered:
            self._log_trace(
                "vat_registration",
                False,
                "Taxpayer is VAT registered - not eligible for simplified tax",
                "218.1.1"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="VAT_REGISTERED",
                reason_description="VAT-registered taxpayers cannot use simplified tax regime",
                legal_basis=[LegalBasis(
                    article="218.1.1",
                    description="Sadələşdirilmiş vergi ödəyicisi kimi qeydiyyata alınmış vergi ödəyicilərinin əməliyyatları ƏDV-yə cəlb edilmir"
                )],
            )
        self._log_trace("vat_registration", True, "Not VAT registered", "218.1.1")

        # =================================================================
        # Q2: AUTOMATIC ROUTES (218.4) - Early fast pass
        # These categories are "simplified taxpayers regardless of 218.1"
        # =================================================================
        route = self._determine_route(input_data)

        if route in [
            TaxRoute.AUTO_TRANSPORT,
            TaxRoute.AUTO_BETTING_LOTTERY,
            TaxRoute.AUTO_PROPERTY,
            TaxRoute.AUTO_LAND,
            TaxRoute.AUTO_FIXED_220_10,
        ]:
            self._log_trace(
                "automatic_route",
                True,
                f"Automatic simplified tax route: {route.value}",
                "218.4"
            )
            # For automatic routes, skip some eligibility checks
            # but still check the universal disqualifiers
            if not self._check_universal_disqualifiers(input_data, legal_basis):
                return EligibilityResult(
                    eligible=False,
                    reason_code="DISQUALIFIER",
                    reason_description="Disqualifying condition found",
                    legal_basis=legal_basis,
                )

            return EligibilityResult(
                eligible=True,
                route=route,
                legal_basis=[LegalBasis(
                    article="218.4",
                    description="Automatic simplified tax categories"
                )],
            )

        # =================================================================
        # Q4: TURNOVER THRESHOLD CHECK (218.1.1 / 218.1.2)
        # Uses adjusted turnover with VAT-exempt exclusion + POS coefficient
        # =================================================================
        if input_data.turnover:
            adjusted_turnover = self._calculate_adjusted_turnover(input_data.turnover)

            if adjusted_turnover > TURNOVER_THRESHOLD_AZN:
                # Check if trade/catering (218.1.2) which has higher threshold allowance
                if input_data.does_trade or input_data.does_catering:
                    self._log_trace(
                        "turnover_threshold",
                        True,
                        f"Trade/catering: turnover {adjusted_turnover} > 200k, eligible under 218.1.2",
                        "218.1.2"
                    )
                    route = TaxRoute.TRADE_CATERING_OVER_200K
                else:
                    self._log_trace(
                        "turnover_threshold",
                        False,
                        f"Adjusted turnover {adjusted_turnover} > {TURNOVER_THRESHOLD_AZN}",
                        "218.1.1"
                    )
                    return EligibilityResult(
                        eligible=False,
                        reason_code="TURNOVER_EXCEEDED",
                        reason_description=f"Adjusted turnover ({adjusted_turnover} AZN) exceeds 200,000 AZN threshold",
                        legal_basis=[LegalBasis(
                            article="218.1.1",
                            description="Vergi tutulan əməliyyatlar həcmi ardıcıl 12 ayda 200000 manatdan çox olmamalıdır"
                        )],
                    )
            else:
                self._log_trace(
                    "turnover_threshold",
                    True,
                    f"Adjusted turnover {adjusted_turnover} <= {TURNOVER_THRESHOLD_AZN}",
                    "218.1.1"
                )
                route = TaxRoute.GENERAL

        # =================================================================
        # DISQUALIFIER CHECKS (218.5.*)
        # =================================================================

        # Q5: Excise/mandatory marking production (218.5.1)
        if input_data.produces_excise_goods:
            self._log_trace(
                "excise_goods",
                False,
                "Produces excise or mandatory-label goods",
                "218.5.1"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="EXCISE_PRODUCER",
                reason_description="Excise or mandatory-label goods producers are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.1",
                    description="Aksizli malların və mütləq markalanan malların istehsalçıları"
                )],
            )
        self._log_trace("excise_goods", True, "Does not produce excise goods", "218.5.1")

        # Q6: Financial sector (218.5.2)
        financial_disqualifiers = [
            (input_data.is_credit_org, "credit organization"),
            (input_data.is_insurance_market_participant, "insurance market professional participant"),
            (input_data.is_investment_fund, "investment fund or manager"),
            (input_data.is_securities_licensed, "securities market licensed person"),
            (input_data.is_pawnshop, "pawnshop"),
        ]

        for is_disqualified, desc in financial_disqualifiers:
            if is_disqualified:
                self._log_trace(
                    "financial_sector",
                    False,
                    f"Is a {desc}",
                    "218.5.2"
                )
                return EligibilityResult(
                    eligible=False,
                    reason_code="FINANCIAL_SECTOR",
                    reason_description=f"Financial sector entities ({desc}) are not eligible",
                    legal_basis=[LegalBasis(
                        article="218.5.2",
                        description="Kredit təşkilatları, sığorta bazarının peşəkar iştirakçıları, investisiya fondları, qiymətli kağızlar bazarının lisenziyalı iştirakçıları, lombardlar"
                    )],
                )
        self._log_trace("financial_sector", True, "Not in financial sector", "218.5.2")

        # Q7: Non-state pension fund (218.5.3)
        if input_data.is_non_state_pension_fund:
            self._log_trace(
                "pension_fund",
                False,
                "Is a non-state pension fund",
                "218.5.3"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="PENSION_FUND",
                reason_description="Non-state pension funds are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.3",
                    description="Qeyri-dövlət pensiya fondları"
                )],
            )
        self._log_trace("pension_fund", True, "Not a pension fund", "218.5.3")

        # Q8: Rental/royalty income (218.5.4)
        if input_data.has_rental_income or input_data.has_royalty_income:
            income_type = "rental" if input_data.has_rental_income else "royalty"
            self._log_trace(
                "rental_royalty",
                False,
                f"Has {income_type} income",
                "218.5.4"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="RENTAL_ROYALTY",
                reason_description=f"Taxpayers with {income_type} income are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.4",
                    description="İcarə və royalti gəliri əldə edən vergi ödəyiciləri"
                )],
            )
        self._log_trace("rental_royalty", True, "No rental/royalty income", "218.5.4")

        # Q9: Natural monopoly (218.5.5)
        if input_data.is_natural_monopoly:
            self._log_trace(
                "natural_monopoly",
                False,
                "Is a designated natural monopoly",
                "218.5.5"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="NATURAL_MONOPOLY",
                reason_description="Natural monopolies are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.5",
                    description="Təbii inhisarçılar"
                )],
            )
        self._log_trace("natural_monopoly", True, "Not a natural monopoly", "218.5.5")

        # Q10: Fixed assets threshold (218.5.6)
        if input_data.fixed_assets_residual_value is not None:
            if input_data.fixed_assets_residual_value > FIXED_ASSETS_THRESHOLD_AZN:
                self._log_trace(
                    "fixed_assets",
                    False,
                    f"Fixed assets {input_data.fixed_assets_residual_value} > {FIXED_ASSETS_THRESHOLD_AZN}",
                    "218.5.6"
                )
                return EligibilityResult(
                    eligible=False,
                    reason_code="FIXED_ASSETS_EXCEEDED",
                    reason_description=f"Fixed assets residual value exceeds 1,000,000 AZN threshold",
                    legal_basis=[LegalBasis(
                        article="218.5.6",
                        description="İlin əvvəlinə əsas vəsaitlərinin qalıq dəyəri 1 000 000 manatdan artıq olan vergi ödəyiciləri"
                    )],
                )
        self._log_trace("fixed_assets", True, "Fixed assets within threshold", "218.5.6")

        # Public legal entity (218.5.7)
        if input_data.is_public_legal_entity:
            self._log_trace(
                "public_entity",
                False,
                "Is a public legal entity",
                "218.5.7"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="PUBLIC_ENTITY",
                reason_description="Public legal entities are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.7",
                    description="Publik hüquqi şəxslər"
                )],
            )
        self._log_trace("public_entity", True, "Not a public entity", "218.5.7")

        # Q12: Production + employees > 10 (218.5.8)
        if input_data.does_production:
            if (input_data.avg_quarterly_employees is not None and
                    input_data.avg_quarterly_employees > PRODUCTION_EMPLOYEE_THRESHOLD):
                self._log_trace(
                    "production_employees",
                    False,
                    f"Production with {input_data.avg_quarterly_employees} employees > {PRODUCTION_EMPLOYEE_THRESHOLD}",
                    "218.5.8"
                )
                return EligibilityResult(
                    eligible=False,
                    reason_code="PRODUCTION_EMPLOYEES",
                    reason_description=f"Production activity with more than {PRODUCTION_EMPLOYEE_THRESHOLD} average quarterly employees is not eligible",
                    legal_basis=[LegalBasis(
                        article="218.5.8",
                        description="İstehsal fəaliyyəti göstərən və rüblük orta işçi sayı 10 nəfərdən çox olan vergi ödəyiciləri"
                    )],
                )
        self._log_trace("production_employees", True, "Production employee threshold OK", "218.5.8")

        # Q13: Wholesale trade (218.5.9 + 218.6.1 exception)
        if input_data.does_wholesale:
            if input_data.wholesale_einvoice_ratio is not None:
                if input_data.wholesale_einvoice_ratio > EXCEPTION_RATIO_THRESHOLD:
                    self._log_trace(
                        "wholesale",
                        False,
                        f"Wholesale e-invoice ratio {input_data.wholesale_einvoice_ratio} > {EXCEPTION_RATIO_THRESHOLD}",
                        "218.5.9"
                    )
                    return EligibilityResult(
                        eligible=False,
                        reason_code="WHOLESALE_EXCEEDED",
                        reason_description="Wholesale e-invoiced operations exceed 30% of quarterly trade operations",
                        legal_basis=[LegalBasis(
                            article="218.5.9",
                            description="Topdan ticarət fəaliyyəti göstərən vergi ödəyiciləri"
                        ), LegalBasis(
                            article="218.6.1",
                            description="Elektron qaimə-faktura ilə topdan satış əməliyyatları rüblük ticarət əməliyyatlarının 30%-dən çox olmamalıdır"
                        )],
                    )
                else:
                    self._log_trace(
                        "wholesale",
                        True,
                        f"Wholesale e-invoice ratio {input_data.wholesale_einvoice_ratio} <= {EXCEPTION_RATIO_THRESHOLD} - exception applies",
                        "218.6.1"
                    )
            else:
                # Wholesale without ratio specified - assume disqualified
                self._log_trace(
                    "wholesale",
                    False,
                    "Wholesale trade without e-invoice ratio - assumed disqualified",
                    "218.5.9"
                )
                return EligibilityResult(
                    eligible=False,
                    reason_code="WHOLESALE",
                    reason_description="Wholesale trade activity without 30% exception verification",
                    legal_basis=[LegalBasis(
                        article="218.5.9",
                        description="Topdan ticarət fəaliyyəti göstərən vergi ödəyiciləri"
                    )],
                )

        # Q14: B2B works/services (218.5.10 + 218.6.2 exception)
        if input_data.does_b2b_works_services:
            if input_data.b2b_einvoice_ratio is not None:
                if input_data.b2b_einvoice_ratio > EXCEPTION_RATIO_THRESHOLD:
                    self._log_trace(
                        "b2b_works_services",
                        False,
                        f"B2B e-invoice ratio {input_data.b2b_einvoice_ratio} > {EXCEPTION_RATIO_THRESHOLD}",
                        "218.5.10"
                    )
                    return EligibilityResult(
                        eligible=False,
                        reason_code="B2B_EXCEEDED",
                        reason_description="B2B e-invoiced operations exceed 30% of quarterly works/services operations",
                        legal_basis=[LegalBasis(
                            article="218.5.10",
                            description="Hüquqi şəxslərə və ya qeydiyyatda olan sahibkarlara iş görən və ya xidmət göstərən vergi ödəyiciləri"
                        ), LegalBasis(
                            article="218.6.2",
                            description="Elektron qaimə-faktura ilə B2B əməliyyatları rüblük iş/xidmət əməliyyatlarının 30%-dən çox olmamalıdır"
                        )],
                    )
                else:
                    self._log_trace(
                        "b2b_works_services",
                        True,
                        f"B2B e-invoice ratio {input_data.b2b_einvoice_ratio} <= {EXCEPTION_RATIO_THRESHOLD} - exception applies",
                        "218.6.2"
                    )
            else:
                self._log_trace(
                    "b2b_works_services",
                    False,
                    "B2B works/services without e-invoice ratio - assumed disqualified",
                    "218.5.10"
                )
                return EligibilityResult(
                    eligible=False,
                    reason_code="B2B_WORKS_SERVICES",
                    reason_description="B2B works/services activity without 30% exception verification",
                    legal_basis=[LegalBasis(
                        article="218.5.10",
                        description="Hüquqi şəxslərə və ya qeydiyyatda olan sahibkarlara iş görən və ya xidmət göstərən vergi ödəyiciləri"
                    )],
                )

        # Q15: Precious goods / fur (218.5.11, 218.5.12)
        if input_data.sells_gold_jewelry_diamonds:
            self._log_trace(
                "precious_goods",
                False,
                "Sells gold, jewelry, or diamonds",
                "218.5.11"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="PRECIOUS_GOODS",
                reason_description="Gold, jewelry, and diamond sellers are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.11",
                    description="Qızıl, zərgərlik məmulatları və almaz satan vergi ödəyiciləri"
                )],
            )

        if input_data.sells_fur_leather:
            self._log_trace(
                "fur_leather",
                False,
                "Sells fur or leather products",
                "218.5.12"
            )
            return EligibilityResult(
                eligible=False,
                reason_code="FUR_LEATHER",
                reason_description="Fur and leather product sellers are not eligible",
                legal_basis=[LegalBasis(
                    article="218.5.12",
                    description="Xəz və dəri məmulatları satan vergi ödəyiciləri"
                )],
            )
        self._log_trace("precious_fur", True, "No precious goods or fur/leather sales", "218.5.11-12")

        # Q11: Licensed activities (PATCH 3 - 218.5.13)
        if input_data.licensed_activity_codes:
            # Check for compulsory insurance carve-out
            if not input_data.has_compulsory_insurance_carveout:
                disqualifying = [
                    code for code in input_data.licensed_activity_codes
                    if code in DISQUALIFYING_LICENSED_ACTIVITIES
                ]
                if disqualifying:
                    self._log_trace(
                        "licensed_activities",
                        False,
                        f"Has licensed activities without carve-out: {disqualifying}",
                        "218.5.13"
                    )
                    return EligibilityResult(
                        eligible=False,
                        reason_code="LICENSED_ACTIVITY",
                        reason_description=f"Licensed activities ({', '.join(c.value for c in disqualifying)}) are not eligible without compulsory insurance carve-out",
                        legal_basis=[LegalBasis(
                            article="218.5.13",
                            description="Lisenziya tələb olunan fəaliyyət növləri ilə məşğul olan vergi ödəyiciləri (icbari sığorta müqavilələri üzrə xidmət istisna olmaqla)"
                        )],
                    )
            else:
                self._log_trace(
                    "licensed_activities",
                    True,
                    "Has licensed activities but compulsory insurance carve-out applies",
                    "218.5.13"
                )
        else:
            self._log_trace("licensed_activities", True, "No licensed activities", "218.5.13")

        # All checks passed
        return EligibilityResult(
            eligible=True,
            route=route or TaxRoute.GENERAL,
            legal_basis=[LegalBasis(
                article="218",
                description="Simplified tax eligibility conditions met"
            )],
        )

    def _check_universal_disqualifiers(
        self,
        input_data: TaxpayerInput,
        legal_basis: list[LegalBasis]
    ) -> bool:
        """
        Check disqualifiers that apply even to automatic routes.

        Returns True if all checks pass, False if disqualified.
        """
        # Financial sector check
        if any([
            input_data.is_credit_org,
            input_data.is_insurance_market_participant,
            input_data.is_investment_fund,
            input_data.is_securities_licensed,
            input_data.is_pawnshop,
        ]):
            legal_basis.append(LegalBasis(
                article="218.5.2",
                description="Financial sector disqualification"
            ))
            return False

        return True

    def _determine_route(self, input_data: TaxpayerInput) -> Optional[TaxRoute]:
        """
        Determine the tax route based on activity type.

        Legal basis: Tax Code Article 218.4
        """
        if input_data.route_auto_transport:
            return TaxRoute.AUTO_TRANSPORT
        if input_data.route_auto_betting_lottery:
            return TaxRoute.AUTO_BETTING_LOTTERY
        if input_data.route_auto_property:
            return TaxRoute.AUTO_PROPERTY
        if input_data.route_auto_land:
            return TaxRoute.AUTO_LAND
        if input_data.route_auto_fixed_220_10:
            return TaxRoute.AUTO_FIXED_220_10

        if input_data.does_trade or input_data.does_catering:
            if input_data.turnover:
                adjusted = self._calculate_adjusted_turnover(input_data.turnover)
                if adjusted > TURNOVER_THRESHOLD_AZN:
                    return TaxRoute.TRADE_CATERING_OVER_200K

        return TaxRoute.GENERAL

    def _calculate_adjusted_turnover(self, turnover: "TurnoverInput") -> Decimal:
        """
        Calculate adjusted turnover for the 200,000 AZN threshold test.

        Legal basis:
        - Tax Code 218.1.1: Uses "vergi tutulan əməliyyatlar həcmi"
        - Tax Code 218.1-1: POS coefficient of 0.5 for retail/services to unregistered

        Formula:
        vat_taxable = gross - vat_exempt
        pos_eligible = pos_retail + pos_services
        adjusted = vat_taxable - pos_eligible + (pos_eligible * 0.5)
                 = vat_taxable - (pos_eligible * 0.5)
        """
        from .entities import TurnoverInput

        vat_taxable = turnover.gross_turnover_12m - turnover.vat_exempt_turnover_12m
        pos_eligible = (
            turnover.pos_retail_nonregistered_12m +
            turnover.pos_services_nonregistered_12m
        )

        # Apply 0.5 coefficient: subtract full amount, add back at 0.5
        adjusted = vat_taxable - pos_eligible + (pos_eligible * POS_COEFFICIENT)

        self._log_trace(
            "turnover_calculation",
            True,
            f"Gross: {turnover.gross_turnover_12m}, VAT-exempt: {turnover.vat_exempt_turnover_12m}, "
            f"POS eligible: {pos_eligible}, Adjusted: {adjusted}",
            "218.1-1"
        )

        return adjusted

    def _calculate_tax(
        self,
        input_data: TaxpayerInput,
        route: Optional[TaxRoute]
    ) -> TaxCalculationResult:
        """
        Calculate simplified tax amount based on route.

        Legal basis: Tax Code Articles 219, 220
        """
        if route == TaxRoute.AUTO_PROPERTY:
            return self._calculate_property_tax(input_data)

        if route == TaxRoute.AUTO_LAND:
            return self._calculate_land_tax(input_data)

        if route == TaxRoute.TRADE_CATERING_OVER_200K:
            return self._calculate_trade_catering_tax(input_data)

        # General simplified tax (220.1)
        if input_data.turnover:
            tax_base = input_data.turnover.gross_turnover_12m
            tax_amount = tax_base * GENERAL_SIMPLIFIED_RATE

            return TaxCalculationResult(
                eligible=True,
                tax_amount=tax_amount,
                tax_base=tax_base,
                tax_rate=GENERAL_SIMPLIFIED_RATE,
                route=route,
                legal_basis=[LegalBasis(
                    article="220.1",
                    description="Sadələşdirilmiş verginin dərəcəsi vergi tutulan əməliyyatların həcminin 2 faizi"
                )],
            )

        return TaxCalculationResult(
            eligible=True,
            route=route,
            legal_basis=[LegalBasis(
                article="220",
                description="Tax calculation requires additional input"
            )],
        )

    def _calculate_property_tax(self, input_data: TaxpayerInput) -> TaxCalculationResult:
        """
        Calculate property transfer simplified tax.

        PATCH 1 implementation: Property sale exemptions

        Legal basis:
        - Tax Code 218.4.3: Property transfer route
        - Tax Code 218-1.1.5: Property exemptions
        - Tax Code 220.8: Property tax calculation
        - Tax Code 102.1.3.2: Family gift/inheritance exemption
        """
        if not input_data.property_transfer:
            return TaxCalculationResult(
                eligible=True,
                route=TaxRoute.AUTO_PROPERTY,
                legal_basis=[LegalBasis(
                    article="218.4.3",
                    description="Property details required for calculation"
                )],
            )

        prop = input_data.property_transfer
        exemptions_applied: list[str] = []

        # Check exemptions (PATCH 1)
        # 218-1.1.5.1: Registered at address for ≥3 years
        if prop.is_registered_3yr:
            self._log_trace(
                "property_exemption",
                True,
                "Exempt: registered at address for ≥3 calendar years",
                "218-1.1.5.1"
            )
            return TaxCalculationResult(
                eligible=True,
                tax_amount=Decimal("0"),
                route=TaxRoute.AUTO_PROPERTY,
                exemptions_applied=["3-year registration exemption (218-1.1.5.1)"],
                legal_basis=[LegalBasis(
                    article="218-1.1.5.1",
                    description="Həmin yaşayış sahəsinin ünvanında azı 3 təqvim ili qeydiyyatda olduqda vergidən azaddır"
                )],
            )

        # 218-1.1.5.1-1: Proof of 3-year residence + one home
        if prop.has_proof_3yr_one_home:
            self._log_trace(
                "property_exemption",
                True,
                "Exempt: 3-year proof with one home ownership",
                "218-1.1.5.1-1"
            )
            return TaxCalculationResult(
                eligible=True,
                tax_amount=Decimal("0"),
                route=TaxRoute.AUTO_PROPERTY,
                exemptions_applied=["3-year residence proof + one home exemption (218-1.1.5.1-1)"],
                legal_basis=[LegalBasis(
                    article="218-1.1.5.1-1",
                    description="3 il ərzində yaşadığını sübut edən və yalnız bir yaşayış sahəsinə malik olan şəxs vergidən azaddır"
                )],
            )

        # 218-1.1.5.2 references 102.1.3.2: Family gift/inheritance
        if prop.is_family_gift_inheritance:
            self._log_trace(
                "property_exemption",
                True,
                "Exempt: family gift/inheritance",
                "102.1.3.2"
            )
            return TaxCalculationResult(
                eligible=True,
                tax_amount=Decimal("0"),
                route=TaxRoute.AUTO_PROPERTY,
                exemptions_applied=["Family gift/inheritance exemption (102.1.3.2)"],
                legal_basis=[LegalBasis(
                    article="218-1.1.5.2",
                    description="Ailə üzvündən bağışlama və ya vərəsəlik yolu ilə əldə edilmiş əmlak"
                ), LegalBasis(
                    article="102.1.3.2",
                    description="Ailə üzvləri arasında əmlakın bağışlanması vergidən azaddır"
                )],
            )

        # No full exemption - calculate tax with 30 m² exemption (218-1.1.5.3)
        taxable_area = prop.area_m2

        if prop.property_type == PropertyType.RESIDENTIAL:
            # Apply 30 m² exemption for residential
            taxable_area = max(Decimal("0"), prop.area_m2 - PROPERTY_EXEMPT_AREA_M2)
            if taxable_area < prop.area_m2:
                exemptions_applied.append(f"30 m² exemption applied (218-1.1.5.3)")
                self._log_trace(
                    "property_30m2_exemption",
                    True,
                    f"Applied 30 m² exemption: {prop.area_m2} - 30 = {taxable_area} taxable",
                    "218-1.1.5.3"
                )

        # Calculate tax: 15 AZN × area × zone coefficient
        zone_coef = ZONE_COEFFICIENTS.get(prop.location_zone, Decimal("1.0"))
        tax_base = taxable_area * PROPERTY_TAX_BASE_RATE_PER_M2
        tax_amount = tax_base * zone_coef

        self._log_trace(
            "property_tax_calc",
            True,
            f"Area: {taxable_area} m², Base rate: {PROPERTY_TAX_BASE_RATE_PER_M2}, "
            f"Zone coef: {zone_coef}, Tax: {tax_amount}",
            "220.8"
        )

        return TaxCalculationResult(
            eligible=True,
            tax_amount=tax_amount,
            tax_base=tax_base,
            tax_rate=zone_coef,  # Zone coefficient acts as rate modifier
            route=TaxRoute.AUTO_PROPERTY,
            exemptions_applied=exemptions_applied,
            legal_basis=[LegalBasis(
                article="220.8",
                description="Yaşayış sahəsinin özgəninkiləşdirilməsindən sadələşdirilmiş vergi 1 kv.m üçün 15 manat × zona əmsalı"
            ), LegalBasis(
                article="218-1.1.5.3",
                description="Mülkiyyətində olan yaşayış sahəsinin ilk 30 kv.m-i vergidən azaddır"
            )],
        )

    def _calculate_land_tax(self, input_data: TaxpayerInput) -> TaxCalculationResult:
        """
        Calculate land transfer simplified tax.

        Legal basis:
        - Tax Code 218.4.5: Land transfer route
        - Tax Code 220.8: Land tax = 2× land tax under 206.1-1
        """
        # For agricultural land, tax = 2× the land tax under 206.1-1
        return TaxCalculationResult(
            eligible=True,
            route=TaxRoute.AUTO_LAND,
            legal_basis=[LegalBasis(
                article="220.8",
                description="Torpaq sahəsinin özgəninkiləşdirilməsindən sadələşdirilmiş vergi 206.1-1-ci maddəyə əsasən torpaq vergisinin 2 misli"
            ), LegalBasis(
                article="206.1-1",
                description="Kənd təsərrüfatı torpaqlarının vergisi"
            )],
        )

    def _calculate_trade_catering_tax(
        self,
        input_data: TaxpayerInput
    ) -> TaxCalculationResult:
        """
        Calculate trade/catering tax for turnover > 200k.

        Legal basis:
        - Tax Code 220.1-1: 8% general, 6% for POS (effective 2026-01-01)

        Note: The 6% POS rate is effective from 2026-01-01 for 3 years
        for turnover through KKM integrated with unified system.
        """
        if not input_data.turnover:
            return TaxCalculationResult(
                eligible=True,
                route=TaxRoute.TRADE_CATERING_OVER_200K,
                legal_basis=[LegalBasis(
                    article="220.1-1",
                    description="Turnover details required for calculation"
                )],
            )

        # Calculate POS eligible portion for lower rate
        pos_eligible = (
            input_data.turnover.pos_retail_nonregistered_12m +
            input_data.turnover.pos_services_nonregistered_12m
        )
        other_turnover = input_data.turnover.gross_turnover_12m - pos_eligible

        # Tax on POS portion at 6% (effective 2026-01-01)
        pos_tax = pos_eligible * TRADE_CATERING_POS_RATE

        # Tax on other portion at 8%
        other_tax = other_turnover * TRADE_CATERING_GENERAL_RATE

        total_tax = pos_tax + other_tax

        exemptions_applied = []
        if pos_eligible > 0:
            exemptions_applied.append(
                f"POS turnover ({pos_eligible} AZN) taxed at 6% rate"
            )

        self._log_trace(
            "trade_catering_tax",
            True,
            f"POS: {pos_eligible} × 6% = {pos_tax}, Other: {other_turnover} × 8% = {other_tax}, Total: {total_tax}",
            "220.1-1"
        )

        return TaxCalculationResult(
            eligible=True,
            tax_amount=total_tax,
            tax_base=input_data.turnover.gross_turnover_12m,
            route=TaxRoute.TRADE_CATERING_OVER_200K,
            exemptions_applied=exemptions_applied,
            legal_basis=[LegalBasis(
                article="220.1-1",
                description="Ticarət və ictimai iaşə üçün 8% (ümumi) və 6% (POS əməliyyatları, 01.01.2026-dan 3 il müddətinə)"
            )],
        )
