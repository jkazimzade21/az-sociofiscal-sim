'use client';

import { useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Button, Input, Checkbox, Select, Tooltip } from '@/components/ui';
import { QuestionCard, ResultCard } from '@/components/questionnaire';
import { evaluateSimplifiedTax } from '@/lib/api';
import { cn, getZoneName } from '@/lib/utils';
import type { EvaluateRequest, EvaluateResponse, LocationZone, PropertyType } from '@/lib/types';

import { dictionary } from '@/lib/dictionary';

// Step definitions
const STEPS = [
  { id: 'vat', label: dictionary.calculator.steps.vat },
  { id: 'route', label: dictionary.calculator.steps.route },
  { id: 'turnover', label: dictionary.calculator.steps.turnover },
  { id: 'disqualifiers', label: dictionary.calculator.steps.disqualifiers },
  { id: 'result', label: dictionary.calculator.steps.result },
];

const LOCATION_ZONES: { value: LocationZone; label: string }[] = [
  { value: 'baku_center', label: dictionary.calculator.activities.propertyExemption.details.zones.baku_center },
  { value: 'baku_other', label: dictionary.calculator.activities.propertyExemption.details.zones.baku_other },
  { value: 'sumgait_ganja_lankaran', label: dictionary.calculator.activities.propertyExemption.details.zones.sumgait_ganja_lankaran },
  { value: 'other_cities', label: dictionary.calculator.activities.propertyExemption.details.zones.other_cities },
  { value: 'rural', label: dictionary.calculator.activities.propertyExemption.details.zones.rural },
];

const LICENSED_ACTIVITIES = [
  { value: 'private_medical', label: dictionary.calculator.disqualifiers.license.items.medical, label_az: dictionary.calculator.disqualifiers.license.items.medical }, // Using same key as desc wasn't separate for az
  { value: 'education', label: dictionary.calculator.disqualifiers.license.items.education, label_az: dictionary.calculator.disqualifiers.license.items.education },
  { value: 'communications', label: dictionary.calculator.disqualifiers.license.items.comm, label_az: dictionary.calculator.disqualifiers.license.items.comm },
  { value: 'fire_protection', label: dictionary.calculator.disqualifiers.license.items.fire, label_az: dictionary.calculator.disqualifiers.license.items.fire },
  { value: 'construction_survey', label: dictionary.calculator.disqualifiers.license.items.survey, label_az: dictionary.calculator.disqualifiers.license.items.survey },
  { value: 'construction_install', label: dictionary.calculator.disqualifiers.license.items.construction, label_az: dictionary.calculator.disqualifiers.license.items.construction },
  { value: 'construction_design', label: dictionary.calculator.disqualifiers.license.items.design, label_az: dictionary.calculator.disqualifiers.license.items.design },
  { value: 'other', label: dictionary.calculator.disqualifiers.license.items.other, label_az: dictionary.calculator.disqualifiers.license.items.other },
];

function CalculatorContent() {
  const searchParams = useSearchParams();
  const debug = searchParams.get('debug') === '1';

  const [currentStep, setCurrentStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<EvaluateResponse | null>(null);

  // Form state
  const [formData, setFormData] = useState<EvaluateRequest>({
    is_vat_registered: undefined,
    route_auto_transport: false,
    route_auto_betting_lottery: false,
    route_auto_property: false,
    route_auto_fixed_220_10: false,
    route_auto_land: false,
    property_transfer: undefined,
    does_trade: false,
    does_catering: false,
    turnover: undefined,
    produces_excise_goods: false,
    is_credit_org: false,
    is_insurance_market_participant: false,
    is_investment_fund: false,
    is_securities_licensed: false,
    is_pawnshop: false,
    is_non_state_pension_fund: false,
    has_rental_income: false,
    has_royalty_income: false,
    is_natural_monopoly: false,
    fixed_assets_residual_value: undefined,
    licensed_activity_codes: [],
    has_compulsory_insurance_carveout: false,
    does_production: false,
    avg_quarterly_employees: undefined,
    does_wholesale: false,
    wholesale_einvoice_ratio: undefined,
    does_b2b_works_services: false,
    b2b_einvoice_ratio: undefined,
    sells_gold_jewelry_diamonds: false,
    sells_fur_leather: false,
    is_public_legal_entity: false,
  });

  // Property exemption state (PATCH 1)
  const [propertyExemption, setPropertyExemption] = useState<string>('');

  // Turnover state (PATCH 2)
  const [turnoverData, setTurnoverData] = useState({
    gross_turnover_12m: '',
    vat_exempt_turnover_12m: '',
    pos_retail_nonregistered_12m: '',
    pos_services_nonregistered_12m: '',
  });

  // Property transfer state
  const [propertyData, setPropertyData] = useState({
    property_type: 'residential' as PropertyType,
    area_m2: '',
    location_zone: 'baku_other' as LocationZone,
  });

  const updateFormData = (updates: Partial<EvaluateRequest>) => {
    setFormData((prev) => ({ ...prev, ...updates }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Build the request with turnover data
      const request: EvaluateRequest = {
        ...formData,
      };

      // Add turnover if provided
      if (turnoverData.gross_turnover_12m) {
        request.turnover = {
          gross_turnover_12m: parseFloat(turnoverData.gross_turnover_12m) || 0,
          vat_exempt_turnover_12m: parseFloat(turnoverData.vat_exempt_turnover_12m) || 0,
          vat_exempt_categories: [],
          pos_retail_nonregistered_12m: parseFloat(turnoverData.pos_retail_nonregistered_12m) || 0,
          pos_services_nonregistered_12m: parseFloat(turnoverData.pos_services_nonregistered_12m) || 0,
        };
      }

      // Add property transfer if route selected
      if (formData.route_auto_property && propertyData.area_m2) {
        request.property_transfer = {
          property_type: propertyData.property_type,
          area_m2: parseFloat(propertyData.area_m2) || 0,
          location_zone: propertyData.location_zone,
          is_registered_3yr: propertyExemption === 'registered_3yr',
          has_proof_3yr_one_home: propertyExemption === 'proof_3yr_one_home',
          is_family_gift_inheritance: propertyExemption === 'family_gift_inheritance',
        };
      }

      const response = await evaluateSimplifiedTax(request, debug);
      setResult(response);
      setCurrentStep(4); // Move to result step
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNext = () => {
    // Validate current step before moving
    if (currentStep === 0 && formData.is_vat_registered === undefined) {
      setError('Please answer the VAT registration question');
      return;
    }

    // If VAT registered, skip to result with early exit
    if (currentStep === 0 && formData.is_vat_registered) {
      handleSubmit();
      return;
    }

    setError(null);
    setCurrentStep((prev) => Math.min(prev + 1, STEPS.length - 1));
  };

  const handleBack = () => {
    setError(null);
    setCurrentStep((prev) => Math.max(prev - 1, 0));
  };

  const handleReset = () => {
    setCurrentStep(0);
    setResult(null);
    setError(null);
    setFormData({
      is_vat_registered: undefined,
      route_auto_transport: false,
      route_auto_betting_lottery: false,
      route_auto_property: false,
      route_auto_fixed_220_10: false,
      route_auto_land: false,
      property_transfer: undefined,
      does_trade: false,
      does_catering: false,
      turnover: undefined,
      produces_excise_goods: false,
      is_credit_org: false,
      is_insurance_market_participant: false,
      is_investment_fund: false,
      is_securities_licensed: false,
      is_pawnshop: false,
      is_non_state_pension_fund: false,
      has_rental_income: false,
      has_royalty_income: false,
      is_natural_monopoly: false,
      fixed_assets_residual_value: undefined,
      licensed_activity_codes: [],
      has_compulsory_insurance_carveout: false,
      does_production: false,
      avg_quarterly_employees: undefined,
      does_wholesale: false,
      wholesale_einvoice_ratio: undefined,
      does_b2b_works_services: false,
      b2b_einvoice_ratio: undefined,
      sells_gold_jewelry_diamonds: false,
      sells_fur_leather: false,
      is_public_legal_entity: false,
    });
    setPropertyExemption('');
    setTurnoverData({
      gross_turnover_12m: '',
      vat_exempt_turnover_12m: '',
      pos_retail_nonregistered_12m: '',
      pos_services_nonregistered_12m: '',
    });
    setPropertyData({
      property_type: 'residential',
      area_m2: '',
      location_zone: 'baku_other',
    });
  };

  // Render step content
  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return renderVATStep();
      case 1:
        return renderRouteStep();
      case 2:
        return renderTurnoverStep();
      case 3:
        return renderDisqualifiersStep();
      case 4:
        return result ? (
          <ResultCard result={result} onReset={handleReset} showDebug={debug} />
        ) : null;
      default:
        return null;
    }
  };

  // Step 1: VAT Registration
  // Step 1: VAT Registration
  const renderVATStep = () => (
    <QuestionCard
      question={dictionary.calculator.vat.question}
      tooltip={dictionary.calculator.vat.tooltip}
      legalBasis="Tax Code 218.1.1"
    >
      <div className="space-y-3">
        <label className="flex items-center gap-3 p-4 border border-green-200 bg-green-50/50 rounded-lg cursor-pointer hover:bg-green-50 transition-colors">
          <input
            type="radio"
            name="vat_registered"
            checked={formData.is_vat_registered === false}
            onChange={() => updateFormData({ is_vat_registered: false })}
            className="w-4 h-4 text-primary-600"
          />
          <div className="flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-medium">{dictionary.calculator.vat.no.label}</span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                {dictionary.calculator.vat.no.badge}
              </span>
            </div>
            <div className="text-sm text-gray-500">{dictionary.calculator.vat.no.subLabel}</div>
            <div className="text-xs text-green-600 mt-1">{dictionary.calculator.vat.no.subLabel}</div>
          </div>
        </label>
        <label className="flex items-center gap-3 p-4 border border-red-200 bg-red-50/50 rounded-lg cursor-pointer hover:bg-red-50 transition-colors">
          <input
            type="radio"
            name="vat_registered"
            checked={formData.is_vat_registered === true}
            onChange={() => updateFormData({ is_vat_registered: true })}
            className="w-4 h-4 text-primary-600"
          />
          <div className="flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-medium">{dictionary.calculator.vat.yes.label}</span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                {dictionary.calculator.vat.yes.badge}
              </span>
            </div>
            <div className="text-sm text-gray-500">{dictionary.calculator.vat.yes.subLabel}</div>
            <div className="text-xs text-red-600 mt-1">{dictionary.calculator.vat.yes.subLabel}</div>
          </div>
        </label>
      </div>
    </QuestionCard>
  );

  // Step 2: Route Selection
  const renderRouteStep = () => (
    <div className="space-y-6">
      <QuestionCard
        question={dictionary.calculator.activities.question}
        tooltip={dictionary.calculator.activities.tooltip}
        legalBasis="Tax Code 218.4"
      >
        <div className="space-y-3">
          <Checkbox
            label={dictionary.calculator.activities.items.transport.label}
            description={dictionary.calculator.activities.items.transport.desc}
            checked={formData.route_auto_transport}
            onChange={(e) => updateFormData({ route_auto_transport: e.target.checked })}
            qualifier
            qualifierReason={dictionary.calculator.activities.tooltip}
          />
          <Checkbox
            label={dictionary.calculator.activities.items.betting.label}
            description={dictionary.calculator.activities.items.betting.desc}
            checked={formData.route_auto_betting_lottery}
            onChange={(e) => updateFormData({ route_auto_betting_lottery: e.target.checked })}
            qualifier
            qualifierReason={dictionary.calculator.activities.tooltip}
          />
          <Checkbox
            label={dictionary.calculator.activities.items.property.label}
            description={dictionary.calculator.activities.items.property.desc}
            checked={formData.route_auto_property}
            onChange={(e) => updateFormData({ route_auto_property: e.target.checked })}
            qualifier
            qualifierReason={dictionary.calculator.activities.tooltip}
          />
          <Checkbox
            label={dictionary.calculator.activities.items.fixed.label}
            description={dictionary.calculator.activities.items.fixed.desc}
            checked={formData.route_auto_fixed_220_10}
            onChange={(e) => updateFormData({ route_auto_fixed_220_10: e.target.checked })}
            qualifier
            qualifierReason={dictionary.calculator.activities.tooltip}
          />
          <Checkbox
            label={dictionary.calculator.activities.items.land.label}
            description={dictionary.calculator.activities.items.land.desc}
            checked={formData.route_auto_land}
            onChange={(e) => updateFormData({ route_auto_land: e.target.checked })}
            qualifier
            qualifierReason={dictionary.calculator.activities.tooltip}
          />
          <div className="border-t pt-3 mt-3">
            <Checkbox
              label={dictionary.calculator.activities.none}
              description={dictionary.calculator.activities.noneDesc}
              checked={!formData.route_auto_transport && !formData.route_auto_betting_lottery && !formData.route_auto_property && !formData.route_auto_fixed_220_10 && !formData.route_auto_land}
              onChange={(e) => {
                if (e.target.checked) {
                  updateFormData({
                    route_auto_transport: false,
                    route_auto_betting_lottery: false,
                    route_auto_property: false,
                    route_auto_fixed_220_10: false,
                    route_auto_land: false,
                  });
                }
              }}
            />
          </div>
        </div>
      </QuestionCard>

      {/* PATCH 1: Property exemption subquestion */}
      {formData.route_auto_property && (
        <QuestionCard
          question={dictionary.calculator.activities.propertyExemption.question}
          tooltip={dictionary.calculator.activities.propertyExemption.tooltip}
          legalBasis="Tax Code 218-1.1.5"
        >
          <div className="space-y-3">
            <label className="flex items-start gap-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
              <input
                type="radio"
                name="property_exemption"
                value="registered_3yr"
                checked={propertyExemption === 'registered_3yr'}
                onChange={(e) => setPropertyExemption(e.target.value)}
                className="w-4 h-4 mt-1 text-primary-600"
              />
              <div>
                <div className="font-medium">{dictionary.calculator.activities.propertyExemption.options.registered.label}</div>
                <div className="text-sm text-gray-500">{dictionary.calculator.activities.propertyExemption.options.registered.desc}</div>
              </div>
            </label>
            <label className="flex items-start gap-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
              <input
                type="radio"
                name="property_exemption"
                value="proof_3yr_one_home"
                checked={propertyExemption === 'proof_3yr_one_home'}
                onChange={(e) => setPropertyExemption(e.target.value)}
                className="w-4 h-4 mt-1 text-primary-600"
              />
              <div>
                <div className="font-medium">{dictionary.calculator.activities.propertyExemption.options.proof.label}</div>
                <div className="text-sm text-gray-500">{dictionary.calculator.activities.propertyExemption.options.proof.desc}</div>
              </div>
            </label>
            <label className="flex items-start gap-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
              <input
                type="radio"
                name="property_exemption"
                value="family_gift_inheritance"
                checked={propertyExemption === 'family_gift_inheritance'}
                onChange={(e) => setPropertyExemption(e.target.value)}
                className="w-4 h-4 mt-1 text-primary-600"
              />
              <div>
                <div className="font-medium">{dictionary.calculator.activities.propertyExemption.options.gift.label}</div>
                <div className="text-sm text-gray-500">{dictionary.calculator.activities.propertyExemption.options.gift.desc}</div>
              </div>
            </label>
            <label className="flex items-start gap-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
              <input
                type="radio"
                name="property_exemption"
                value="none"
                checked={propertyExemption === 'none'}
                onChange={(e) => setPropertyExemption(e.target.value)}
                className="w-4 h-4 mt-1 text-primary-600"
              />
              <div>
                <div className="font-medium">{dictionary.calculator.activities.propertyExemption.options.none.label}</div>
                <div className="text-sm text-gray-500">{dictionary.calculator.activities.propertyExemption.options.none.desc}</div>
              </div>
            </label>
          </div>

          {propertyExemption === 'none' && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium mb-4">{dictionary.calculator.activities.propertyExemption.details.title}</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  label={dictionary.calculator.activities.propertyExemption.details.type}
                  options={[
                    { value: 'residential', label: dictionary.calculator.activities.propertyExemption.details.types.residential },
                    { value: 'non_residential', label: dictionary.calculator.activities.propertyExemption.details.types.non_residential },
                  ]}
                  value={propertyData.property_type}
                  onChange={(e) =>
                    setPropertyData({ ...propertyData, property_type: e.target.value as PropertyType })
                  }
                />
                <Input
                  label={dictionary.calculator.activities.propertyExemption.details.area}
                  type="number"
                  min="0"
                  value={propertyData.area_m2}
                  onChange={(e) => setPropertyData({ ...propertyData, area_m2: e.target.value })}
                />
                <Select
                  label={dictionary.calculator.activities.propertyExemption.details.zone}
                  options={LOCATION_ZONES}
                  value={propertyData.location_zone}
                  onChange={(e) =>
                    setPropertyData({ ...propertyData, location_zone: e.target.value as LocationZone })
                  }
                />
              </div>
            </div>
          )}
        </QuestionCard>
      )}

      {/* Trade/catering question */}
      <QuestionCard
        question={dictionary.calculator.activities.trade.question}
        tooltip={dictionary.calculator.activities.trade.tooltip}
        legalBasis="Tax Code 218.1.2, 220.1-1"
      >
        <div className="space-y-3">
          <Checkbox
            label={dictionary.calculator.activities.trade.retail.label}
            checked={formData.does_trade}
            onChange={(e) => updateFormData({ does_trade: e.target.checked })}
          />
          <Checkbox
            label={dictionary.calculator.activities.trade.catering.label}
            checked={formData.does_catering}
            onChange={(e) => updateFormData({ does_catering: e.target.checked })}
          />
        </div>
      </QuestionCard>
    </div>
  );

  // Step 3: Turnover (PATCH 2)
  // Step 3: Turnover (PATCH 2)
  const renderTurnoverStep = () => (
    <QuestionCard
      question={dictionary.calculator.turnover.question}
      tooltip={dictionary.calculator.turnover.tooltip}
      legalBasis="Tax Code 218.1.1, 218.1-1, 164"
    >
      <div className="space-y-6">
        {/* Threshold warning */}
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-start gap-3">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-red-100 text-red-600 flex-shrink-0 mt-0.5">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </span>
            <div>
              <h4 className="font-medium text-red-900 mb-1">{dictionary.calculator.turnover.warning.title}</h4>
              <p className="text-sm text-red-700">
                <span dangerouslySetInnerHTML={{ __html: dictionary.calculator.turnover.warning.desc }} />
              </p>
            </div>
          </div>
        </div>

        <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg">
          <h4 className="font-medium text-primary-900 mb-2">{dictionary.calculator.turnover.info.title}</h4>
          <p className="text-sm text-primary-700">
            <span dangerouslySetInnerHTML={{ __html: dictionary.calculator.turnover.info.desc }} />
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label={dictionary.calculator.turnover.inputs.gross.label}
            type="number"
            min="0"
            step="0.01"
            placeholder={`${dictionary.common.eg} 150000`}
            value={turnoverData.gross_turnover_12m}
            onChange={(e) =>
              setTurnoverData({ ...turnoverData, gross_turnover_12m: e.target.value })
            }
            helperText={dictionary.calculator.turnover.inputs.gross.desc}
          />
          <Input
            label={dictionary.calculator.turnover.inputs.exempt.label}
            type="number"
            min="0"
            step="0.01"
            placeholder={`${dictionary.common.eg} 0`}
            value={turnoverData.vat_exempt_turnover_12m}
            onChange={(e) =>
              setTurnoverData({ ...turnoverData, vat_exempt_turnover_12m: e.target.value })
            }
            helperText={dictionary.calculator.turnover.inputs.exempt.desc}
          />
        </div>

        <div className="border-t pt-6">
          <h4 className="font-medium mb-4">{dictionary.calculator.turnover.inputs.posRetail.sectionTitle}</h4>
          <p className="text-sm text-gray-500 mb-4">
            Non-cash POS turnover from retail/services to unregistered persons is counted at 50% for the threshold test.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label={dictionary.calculator.turnover.inputs.posRetail.label}
              type="number"
              min="0"
              step="0.01"
              placeholder={`${dictionary.common.eg} 50000`}
              value={turnoverData.pos_retail_nonregistered_12m}
              onChange={(e) =>
                setTurnoverData({ ...turnoverData, pos_retail_nonregistered_12m: e.target.value })
              }
              helperText={dictionary.calculator.turnover.inputs.posRetail.desc}
            />
            <Input
              label={dictionary.calculator.turnover.inputs.posServices.label}
              type="number"
              min="0"
              step="0.01"
              placeholder={`${dictionary.common.eg} 20000`}
              value={turnoverData.pos_services_nonregistered_12m}
              onChange={(e) =>
                setTurnoverData({ ...turnoverData, pos_services_nonregistered_12m: e.target.value })
              }
              helperText={dictionary.calculator.turnover.inputs.posServices.desc}
            />
          </div>
        </div>
      </div>
    </QuestionCard>
  );

  // Step 4: Disqualifiers
  const renderDisqualifiersStep = () => (
    <div className="space-y-6">
      {/* Info banner */}
      <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
        <div className="flex items-start gap-3">
          <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-100 text-amber-600 flex-shrink-0 mt-0.5">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </span>
          <div>
            <h4 className="font-medium text-amber-900 mb-1">{dictionary.calculator.disqualifiers.info.title}</h4>
            <p className="text-sm text-amber-700">
              {dictionary.calculator.disqualifiers.info.desc}
            </p>
          </div>
        </div>
      </div>

      {/* Excise goods */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.excise.question}
        legalBasis="Tax Code 218.5.1"
      >
        <div className="space-y-3">
          <label className="flex items-center gap-3 p-3 border border-green-200 bg-green-50/50 rounded-lg cursor-pointer hover:bg-green-50 transition-colors">
            <input
              type="radio"
              name="excise"
              checked={formData.produces_excise_goods === false}
              onChange={() => updateFormData({ produces_excise_goods: false })}
              className="w-4 h-4 text-primary-600"
            />
            <span className="font-medium">{dictionary.calculator.disqualifiers.excise.no}</span>
          </label>
          <label className="flex items-center gap-3 p-3 border border-red-200 bg-red-50/50 rounded-lg cursor-pointer hover:bg-red-50 transition-colors">
            <input
              type="radio"
              name="excise"
              checked={formData.produces_excise_goods === true}
              onChange={() => updateFormData({ produces_excise_goods: true })}
              className="w-4 h-4 text-primary-600"
            />
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="font-medium">{dictionary.calculator.disqualifiers.excise.yes}</span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  {dictionary.calculator.disqualifiers.excise.disqualify}
                </span>
              </div>
            </div>
          </label>
        </div>
      </QuestionCard>

      {/* Financial sector */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.financial.question}
        legalBasis="Tax Code 218.5.2"
      >
        <div className="space-y-3">
          <Checkbox
            label={dictionary.calculator.disqualifiers.financial.credit}
            checked={formData.is_credit_org}
            onChange={(e) => updateFormData({ is_credit_org: e.target.checked })}
            disqualifier
          />
          <Checkbox
            label={dictionary.calculator.disqualifiers.financial.insurance}
            checked={formData.is_insurance_market_participant}
            onChange={(e) => updateFormData({ is_insurance_market_participant: e.target.checked })}
            disqualifier
          />
          <Checkbox
            label={dictionary.calculator.disqualifiers.financial.investment}
            checked={formData.is_investment_fund}
            onChange={(e) => updateFormData({ is_investment_fund: e.target.checked })}
            disqualifier
          />
          <Checkbox
            label={dictionary.calculator.disqualifiers.financial.securities}
            checked={formData.is_securities_licensed}
            onChange={(e) => updateFormData({ is_securities_licensed: e.target.checked })}
            disqualifier
          />
          <Checkbox
            label={dictionary.calculator.disqualifiers.financial.pawnshop}
            checked={formData.is_pawnshop}
            onChange={(e) => updateFormData({ is_pawnshop: e.target.checked })}
            disqualifier
          />
        </div>
      </QuestionCard>

      {/* Rental/royalty */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.income.question}
        legalBasis="Tax Code 218.5.4"
      >
        <div className="space-y-3">
          <Checkbox
            label={dictionary.calculator.disqualifiers.income.rental}
            checked={formData.has_rental_income}
            onChange={(e) => updateFormData({ has_rental_income: e.target.checked })}
            disqualifier
          />
          <Checkbox
            label={dictionary.calculator.disqualifiers.income.royalty}
            checked={formData.has_royalty_income}
            onChange={(e) => updateFormData({ has_royalty_income: e.target.checked })}
            disqualifier
          />
        </div>
      </QuestionCard>

      {/* Licensed activities */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.license.question}
        tooltip={dictionary.calculator.disqualifiers.license.tooltip}
        legalBasis="Tax Code 218.5.13, License Law Annex 1"
      >
        <div className="space-y-3">
          {LICENSED_ACTIVITIES.map((activity) => (
            <Checkbox
              key={activity.value}
              label={activity.label}
              checked={formData.licensed_activity_codes?.includes(activity.value as any)}
              onChange={(e) => {
                const codes = formData.licensed_activity_codes || [];
                if (e.target.checked) {
                  updateFormData({ licensed_activity_codes: [...codes, activity.value as any] });
                } else {
                  updateFormData({
                    licensed_activity_codes: codes.filter((c) => c !== activity.value),
                  });
                }
              }}
              disqualifier
            />
          ))}
        </div>

        {(formData.licensed_activity_codes?.length || 0) > 0 && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <Checkbox
              label={dictionary.calculator.disqualifiers.license.exception}
              checked={formData.has_compulsory_insurance_carveout}
              onChange={(e) =>
                updateFormData({ has_compulsory_insurance_carveout: e.target.checked })
              }
              exception
            />
          </div>
        )}
      </QuestionCard>

      {/* Wholesale */}
      {formData.does_trade && (
        <QuestionCard
          question={dictionary.calculator.disqualifiers.wholesale.question}
          tooltip={dictionary.calculator.disqualifiers.wholesale.tooltip}
          legalBasis="Tax Code 218.5.9, 218.6.1"
        >
          <div className="space-y-4">
            <div className="space-y-3">
              <label className="flex items-center gap-3 p-3 border border-green-200 bg-green-50/50 rounded-lg cursor-pointer hover:bg-green-50 transition-colors">
                <input
                  type="radio"
                  name="wholesale"
                  checked={formData.does_wholesale === false}
                  onChange={() => updateFormData({ does_wholesale: false })}
                  className="w-4 h-4 text-primary-600"
                />
                <span className="font-medium">{dictionary.calculator.disqualifiers.wholesale.no}</span>
              </label>
              <label className="flex items-center gap-3 p-3 border border-amber-200 bg-amber-50/50 rounded-lg cursor-pointer hover:bg-amber-50 transition-colors">
                <input
                  type="radio"
                  name="wholesale"
                  checked={formData.does_wholesale === true}
                  onChange={() => updateFormData({ does_wholesale: true })}
                  className="w-4 h-4 text-primary-600"
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{dictionary.calculator.disqualifiers.wholesale.yes}</span>
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-700">
                      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      {dictionary.calculator.disqualifiers.wholesale.disqualify}
                    </span>
                  </div>
                </div>
              </label>
            </div>

            {formData.does_wholesale && (
              <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <Input
                  label={dictionary.calculator.disqualifiers.wholesale.ratio}
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  placeholder={`${dictionary.common.eg} 0.25`}
                  value={formData.wholesale_einvoice_ratio?.toString() || ''}
                  onChange={(e) =>
                    updateFormData({
                      wholesale_einvoice_ratio: e.target.value ? parseFloat(e.target.value) : undefined,
                    })
                  }
                />
              </div>
            )}
          </div>
        </QuestionCard>
      )}

      {/* Precious goods */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.goods.question}
        legalBasis="Tax Code 218.5.11-218.5.12"
      >
        <div className="space-y-3">
          <Checkbox
            label={dictionary.calculator.disqualifiers.goods.gold}
            checked={formData.sells_gold_jewelry_diamonds}
            onChange={(e) => updateFormData({ sells_gold_jewelry_diamonds: e.target.checked })}
            disqualifier
          />
          <Checkbox
            label={dictionary.calculator.disqualifiers.goods.leather}
            checked={formData.sells_fur_leather}
            onChange={(e) => updateFormData({ sells_fur_leather: e.target.checked })}
            disqualifier
          />
        </div>
      </QuestionCard>

      {/* Production */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.production.question}
        legalBasis="Tax Code 218.5.10"
      >
        <div className="space-y-4">
          <Checkbox
            label={dictionary.calculator.disqualifiers.production.label}
            checked={formData.does_production}
            onChange={(e) => updateFormData({ does_production: e.target.checked })}
          />

          {formData.does_production && (
            <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <Input
                label={dictionary.calculator.disqualifiers.production.employees}
                type="number"
                min="0"
                placeholder={`${dictionary.common.eg} 5`}
                value={formData.avg_quarterly_employees?.toString() || ''}
                onChange={(e) =>
                  updateFormData({
                    avg_quarterly_employees: e.target.value ? parseFloat(e.target.value) : undefined,
                  })
                }
                helperText={dictionary.calculator.disqualifiers.production.disqualify}
              />
            </div>
          )}
        </div>
      </QuestionCard>

      {/* B2B Services */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.b2b.question}
        legalBasis="Tax Code 218.6.2"
      >
        <div className="space-y-4">
          <div className="space-y-3">
            <label className="flex items-center gap-3 p-3 border border-green-200 bg-green-50/50 rounded-lg cursor-pointer hover:bg-green-50 transition-colors">
              <input
                type="radio"
                name="b2b"
                checked={formData.does_b2b_works_services === false}
                onChange={() => updateFormData({ does_b2b_works_services: false })}
                className="w-4 h-4 text-primary-600"
              />
              <span className="font-medium">{dictionary.calculator.disqualifiers.b2b.no}</span>
            </label>
            <label className="flex items-center gap-3 p-3 border border-amber-200 bg-amber-50/50 rounded-lg cursor-pointer hover:bg-amber-50 transition-colors">
              <input
                type="radio"
                name="b2b"
                checked={formData.does_b2b_works_services === true}
                onChange={() => updateFormData({ does_b2b_works_services: true })}
                className="w-4 h-4 text-primary-600"
              />
              <span className="font-medium">{dictionary.calculator.disqualifiers.b2b.yes}</span>
            </label>
          </div>

          {formData.does_b2b_works_services && (
            <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <Input
                label={dictionary.calculator.disqualifiers.b2b.ratio}
                type="number"
                min="0"
                max="1"
                step="0.01"
                placeholder={`${dictionary.common.eg} 0.25`}
                value={formData.b2b_einvoice_ratio?.toString() || ''}
                onChange={(e) =>
                  updateFormData({
                    b2b_einvoice_ratio: e.target.value ? parseFloat(e.target.value) : undefined,
                  })
                }
                helperText={dictionary.calculator.disqualifiers.b2b.disqualify}
              />
            </div>
          )}
        </div>
      </QuestionCard>

      {/* Public entity */}
      <QuestionCard
        question={dictionary.calculator.disqualifiers.entity.question}
        legalBasis="Tax Code 218.5.8"
      >
        <Checkbox
          label={dictionary.calculator.disqualifiers.entity.label}
          checked={formData.is_public_legal_entity}
          onChange={(e) => updateFormData({ is_public_legal_entity: e.target.checked })}
          disqualifier
          disqualifierReason={dictionary.calculator.disqualifiers.entity.disqualify}
        />
      </QuestionCard>
    </div>
  );

  return (
    <div className="max-w-3xl mx-auto">
      {/* Progress indicator */}
      {currentStep < 4 && (
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>
              {dictionary.common.step} {currentStep + 1} / {STEPS.length - 1}
            </span>
            <span>{STEPS[currentStep].label}</span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-primary-600 transition-all duration-300"
              style={{ width: `${((currentStep + 1) / (STEPS.length - 1)) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="mb-6 p-4 bg-error-50 border border-error-200 rounded-lg text-error-700">
          {error}
        </div>
      )}

      {/* Step content */}
      {renderStep()}

      {/* Navigation buttons */}
      {currentStep < 4 && (
        <div className="mt-8 flex justify-between">
          <Button
            variant="outline"
            onClick={handleBack}
            disabled={currentStep === 0}
          >
            {dictionary.common.back}
          </Button>
          <div className="flex gap-3">
            {currentStep < 3 && (
              <Button onClick={handleNext}>{dictionary.common.continue}</Button>
            )}
            {currentStep === 3 && (
              <Button onClick={handleSubmit} loading={isLoading}>
                {dictionary.common.calculate}
              </Button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default function CalculatorPage() {
  return (
    <Suspense fallback={<div className="max-w-3xl mx-auto p-4">{dictionary.common.loading}</div>}>
      <CalculatorContent />
    </Suspense>
  );
}
