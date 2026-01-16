"""
Evaluation service for simplified tax calculation.

This service bridges the API layer with the core rules engine.
"""

from typing import Optional
from decimal import Decimal

from az_sim import SimplifiedTaxEngine, TaxpayerInput
from az_sim.entities import (
    TaxCalculationResult,
    TurnoverInput,
    PropertyTransferInput,
    PropertyType,
    LocationZone,
    LicensedActivityCode,
    VATExemptCategory,
)
from ..schemas.requests import EvaluateRequest
from ..schemas.responses import EvaluateResponse, LegalBasisResponse


class EvaluationService:
    """
    Service for evaluating simplified tax eligibility and calculating tax.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug

    def evaluate(self, request: EvaluateRequest) -> EvaluateResponse:
        """
        Evaluate simplified tax eligibility and calculate tax amount.

        Args:
            request: Full evaluation request with all taxpayer data

        Returns:
            EvaluateResponse with eligibility status and tax calculation
        """
        # Convert API schema to engine input
        taxpayer_input = self._convert_request_to_input(request)

        # Run evaluation engine
        engine = SimplifiedTaxEngine(debug=self.debug)
        result = engine.evaluate(taxpayer_input)

        # Convert result to API response
        return self._convert_result_to_response(result)

    def _convert_request_to_input(self, request: EvaluateRequest) -> TaxpayerInput:
        """Convert API request schema to engine input model."""
        # Convert turnover if provided
        turnover = None
        if request.turnover:
            turnover = TurnoverInput(
                gross_turnover_12m=request.turnover.gross_turnover_12m,
                vat_exempt_turnover_12m=request.turnover.vat_exempt_turnover_12m,
                vat_exempt_categories=[
                    VATExemptCategory(cat) for cat in request.turnover.vat_exempt_categories
                ],
                pos_retail_nonregistered_12m=request.turnover.pos_retail_nonregistered_12m,
                pos_services_nonregistered_12m=request.turnover.pos_services_nonregistered_12m,
            )

        # Convert property transfer if provided
        property_transfer = None
        if request.property_transfer:
            property_transfer = PropertyTransferInput(
                property_type=PropertyType(request.property_transfer.property_type),
                area_m2=request.property_transfer.area_m2,
                location_zone=LocationZone(request.property_transfer.location_zone),
                is_registered_3yr=request.property_transfer.is_registered_3yr,
                has_proof_3yr_one_home=request.property_transfer.has_proof_3yr_one_home,
                is_family_gift_inheritance=request.property_transfer.is_family_gift_inheritance,
            )

        # Convert licensed activity codes
        licensed_codes = [
            LicensedActivityCode(code) for code in request.licensed_activity_codes
        ]

        return TaxpayerInput(
            is_vat_registered=request.is_vat_registered,
            route_auto_transport=request.route_auto_transport,
            route_auto_betting_lottery=request.route_auto_betting_lottery,
            route_auto_property=request.route_auto_property,
            route_auto_fixed_220_10=request.route_auto_fixed_220_10,
            route_auto_land=request.route_auto_land,
            property_transfer=property_transfer,
            does_trade=request.does_trade,
            does_catering=request.does_catering,
            turnover=turnover,
            produces_excise_goods=request.produces_excise_goods,
            is_credit_org=request.is_credit_org,
            is_insurance_market_participant=request.is_insurance_market_participant,
            is_investment_fund=request.is_investment_fund,
            is_securities_licensed=request.is_securities_licensed,
            is_pawnshop=request.is_pawnshop,
            is_non_state_pension_fund=request.is_non_state_pension_fund,
            has_rental_income=request.has_rental_income,
            has_royalty_income=request.has_royalty_income,
            is_natural_monopoly=request.is_natural_monopoly,
            fixed_assets_residual_value=request.fixed_assets_residual_value,
            licensed_activity_codes=licensed_codes,
            has_compulsory_insurance_carveout=request.has_compulsory_insurance_carveout,
            does_production=request.does_production,
            avg_quarterly_employees=request.avg_quarterly_employees,
            does_wholesale=request.does_wholesale,
            wholesale_einvoice_ratio=request.wholesale_einvoice_ratio,
            does_b2b_works_services=request.does_b2b_works_services,
            b2b_einvoice_ratio=request.b2b_einvoice_ratio,
            sells_gold_jewelry_diamonds=request.sells_gold_jewelry_diamonds,
            sells_fur_leather=request.sells_fur_leather,
            is_public_legal_entity=request.is_public_legal_entity,
        )

    def _convert_result_to_response(
        self,
        result: TaxCalculationResult
    ) -> EvaluateResponse:
        """Convert engine result to API response."""
        legal_basis = [
            LegalBasisResponse(
                article=lb.article,
                description=lb.description,
                source_url=lb.source_url,
            )
            for lb in result.legal_basis
        ]

        return EvaluateResponse(
            eligible=result.eligible,
            tax_amount=result.tax_amount,
            currency=result.currency,
            route=result.route,
            tax_base=result.tax_base,
            tax_rate=result.tax_rate,
            exemptions_applied=result.exemptions_applied,
            reason_code=result.reason_code,
            reason_description=result.reason_description,
            legal_basis=legal_basis,
            debug_trace=result.debug_trace,
        )
