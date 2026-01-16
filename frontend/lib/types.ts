/**
 * Type definitions for the Simplified Tax Calculator frontend.
 */

export type TaxRoute =
  | 'general'
  | 'trade_catering_over_200k'
  | 'auto_transport'
  | 'auto_betting_lottery'
  | 'auto_property'
  | 'auto_land'
  | 'auto_fixed_220_10';

export type PropertyType = 'residential' | 'non_residential';

export type LocationZone =
  | 'baku_center'
  | 'baku_other'
  | 'sumgait_ganja_lankaran'
  | 'other_cities'
  | 'rural';

export type VATExemptCategory =
  | 'financial_services'
  | 'textbook_publishing'
  | 'medical_services'
  | 'education_services'
  | 'insurance_services'
  | 'other';

export type LicensedActivityCode =
  | 'private_medical'
  | 'education'
  | 'communications'
  | 'fire_protection'
  | 'construction_survey'
  | 'construction_install'
  | 'construction_design'
  | 'pharmaceutical'
  | 'veterinary'
  | 'auditing'
  | 'notary'
  | 'legal_services'
  | 'security_services'
  | 'gambling'
  | 'alcohol_production'
  | 'tobacco_production'
  | 'banking'
  | 'insurance'
  | 'securities'
  | 'other';

export interface TurnoverInput {
  gross_turnover_12m: number;
  vat_exempt_turnover_12m: number;
  vat_exempt_categories: VATExemptCategory[];
  pos_retail_nonregistered_12m: number;
  pos_services_nonregistered_12m: number;
}

export interface PropertyTransferInput {
  property_type: PropertyType;
  area_m2: number;
  location_zone: LocationZone;
  is_registered_3yr: boolean;
  has_proof_3yr_one_home: boolean;
  is_family_gift_inheritance: boolean;
}

export interface EvaluateRequest {
  is_vat_registered?: boolean;
  route_auto_transport?: boolean;
  route_auto_betting_lottery?: boolean;
  route_auto_property?: boolean;
  route_auto_fixed_220_10?: boolean;
  route_auto_land?: boolean;
  property_transfer?: PropertyTransferInput;
  does_trade?: boolean;
  does_catering?: boolean;
  turnover?: TurnoverInput;
  produces_excise_goods?: boolean;
  is_credit_org?: boolean;
  is_insurance_market_participant?: boolean;
  is_investment_fund?: boolean;
  is_securities_licensed?: boolean;
  is_pawnshop?: boolean;
  is_non_state_pension_fund?: boolean;
  has_rental_income?: boolean;
  has_royalty_income?: boolean;
  is_natural_monopoly?: boolean;
  fixed_assets_residual_value?: number;
  licensed_activity_codes?: LicensedActivityCode[];
  has_compulsory_insurance_carveout?: boolean;
  does_production?: boolean;
  avg_quarterly_employees?: number;
  does_wholesale?: boolean;
  wholesale_einvoice_ratio?: number;
  does_b2b_works_services?: boolean;
  b2b_einvoice_ratio?: number;
  sells_gold_jewelry_diamonds?: boolean;
  sells_fur_leather?: boolean;
  is_public_legal_entity?: boolean;
}

export interface LegalBasis {
  article: string;
  description: string;
  source_url: string;
}

export interface EvaluateResponse {
  eligible: boolean;
  tax_amount?: number;
  currency: string;
  route?: TaxRoute;
  tax_base?: number;
  tax_rate?: number;
  exemptions_applied: string[];
  reason_code?: string;
  reason_description?: string;
  legal_basis: LegalBasis[];
  debug_trace?: Array<{
    rule: string;
    result: boolean;
    details: string;
    article: string;
  }>;
}

export interface QuestionOption {
  value: string;
  label: string;
  label_az?: string;
  description?: string;
  description_az?: string;
}

export interface Question {
  id: string;
  type: 'boolean' | 'select' | 'multi_select' | 'number' | 'decimal' | 'object';
  question: string;
  question_az: string;
  tooltip?: string;
  tooltip_az?: string;
  legal_basis?: string;
  options?: QuestionOption[];
  required: boolean;
  subquestions?: Question[];
  condition?: string;
}

export interface LicensedActivity {
  code: string;
  name_az: string;
  name_en: string;
  category: string;
  disqualifies: boolean;
}

// Form state for the questionnaire
export interface FormState extends EvaluateRequest {
  // Track which questions have been answered
  _answered: Set<string>;
  // Current step in the wizard
  _currentStep: number;
}
