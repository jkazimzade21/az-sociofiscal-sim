'use client';

import { useState } from 'react';
import { Button } from '@/components/ui';
import { cn, formatCurrency, formatPercent, getRouteName } from '@/lib/utils';
import type { EvaluateResponse } from '@/lib/types';
import { dictionary } from '@/lib/dictionary';

interface ResultCardProps {
  result: EvaluateResponse;
  onReset: () => void;
  showDebug?: boolean;
}

export function ResultCard({ result, onReset, showDebug }: ResultCardProps) {
  const [showDetails, setShowDetails] = useState(false);
  const t = dictionary.calculator.results;

  if (!result.eligible) {
    return (
      <div className="card result-not-eligible border-2">
        <div className="text-center py-8">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-error-100 flex items-center justify-center">
            <svg
              className="w-8 h-8 text-error-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-error-900 mb-2">
            {t.notEligible.title}
          </h2>
          <p className="text-error-700">
            {t.notEligible.desc}
          </p>
        </div>

        {showDebug && result.debug_trace && (
          <div className="mt-6 p-4 bg-white rounded-lg border border-error-200">
            <h3 className="text-sm font-semibold text-gray-900 mb-2">
              {t.notEligible.debug}
            </h3>
            <div className="space-y-2 text-sm">
              {result.debug_trace
                .filter((t) => !t.result)
                .slice(0, 1)
                .map((trace, i) => (
                  <div key={i} className="p-2 bg-error-50 rounded">
                    <div className="font-medium text-error-900">
                      {trace.rule}
                    </div>
                    <div className="text-error-700">{trace.details}</div>
                    <div className="text-xs text-error-500 mt-1">
                      {t.details.article}: {trace.article}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        <div className="mt-6 flex justify-center">
          <Button variant="outline" onClick={onReset}>
            {t.restart}
          </Button>
        </div>
      </div>
    );
  }

  // Eligible result
  return (
    <div className="card result-eligible border-2">
      <div className="text-center py-8">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-success-100 flex items-center justify-center">
          <svg
            className="w-8 h-8 text-success-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-success-900 mb-2">{t.eligible.title}</h2>
        <p className="text-success-700 mb-4">
          {t.eligible.desc}
        </p>

        {result.tax_amount !== null && result.tax_amount !== undefined && (
          <div className="mt-6">
            <div className="text-4xl font-bold text-success-900">
              {result.tax_amount === 0
                ? t.eligible.exempt
                : formatCurrency(result.tax_amount)}
            </div>
            {result.route && (
              <div className="text-sm text-success-700 mt-2">
                {t.eligible.route}: {getRouteName(result.route)}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Details Accordion */}
      <div className="mt-6 border-t border-success-200 pt-6">
        <button
          type="button"
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center justify-between w-full text-left"
        >
          <span className="text-sm font-medium text-success-900">
            {t.details.button}
          </span>
          <svg
            className={cn(
              'w-5 h-5 text-success-600 transition-transform',
              showDetails && 'rotate-180'
            )}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        {showDetails && (
          <div className="mt-4 space-y-4">
            {/* Calculation breakdown */}
            {result.tax_base && (
              <div className="p-4 bg-white rounded-lg border border-success-200">
                <h3 className="text-sm font-semibold text-gray-900 mb-3">
                  {t.details.breakdown}
                </h3>
                <dl className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <dt className="text-gray-600">{t.details.taxBase}:</dt>
                    <dd className="font-medium">
                      {formatCurrency(result.tax_base)}
                    </dd>
                  </div>
                  {result.tax_rate && (
                    <div className="flex justify-between">
                      <dt className="text-gray-600">{t.details.taxRate}:</dt>
                      <dd className="font-medium">
                        {formatPercent(result.tax_rate)}
                      </dd>
                    </div>
                  )}
                  <div className="flex justify-between pt-2 border-t">
                    <dt className="font-medium text-gray-900">{t.eligible.taxAmount}:</dt>
                    <dd className="font-bold text-success-700">
                      {result.tax_amount !== null && result.tax_amount !== undefined
                        ? formatCurrency(result.tax_amount)
                        : '-'}
                    </dd>
                  </div>
                </dl>
              </div>
            )}

            {/* Exemptions applied */}
            {result.exemptions_applied.length > 0 && (
              <div className="p-4 bg-white rounded-lg border border-success-200">
                <h3 className="text-sm font-semibold text-gray-900 mb-3">
                  {t.details.exemptions}
                </h3>
                <ul className="space-y-1">
                  {result.exemptions_applied.map((exemption, i) => (
                    <li key={i} className="text-sm text-gray-600 flex gap-2">
                      <span className="text-success-500">&#10003;</span>
                      {exemption}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Legal basis */}
            {result.legal_basis.length > 0 && (
              <div className="p-4 bg-white rounded-lg border border-success-200">
                <h3 className="text-sm font-semibold text-gray-900 mb-3">
                  {t.details.citations}
                </h3>
                <ul className="space-y-2">
                  {result.legal_basis.map((basis, i) => (
                    <li key={i} className="text-sm">
                      <span className="font-medium text-primary-700">
                        {t.details.article} {basis.article}
                      </span>
                      <p className="text-gray-600">{basis.description}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Debug trace */}
            {showDebug && result.debug_trace && (
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <h3 className="text-sm font-semibold text-gray-900 mb-3">
                  Full Debug Trace
                </h3>
                <div className="space-y-2 text-xs font-mono max-h-64 overflow-y-auto">
                  {result.debug_trace.map((trace, i) => (
                    <div
                      key={i}
                      className={cn(
                        'p-2 rounded',
                        trace.result ? 'bg-success-50' : 'bg-error-50'
                      )}
                    >
                      <div className="font-medium">{trace.rule}</div>
                      <div className="text-gray-600">{trace.details}</div>
                      <div className="text-gray-400">
                        {t.details.article}: {trace.article}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="mt-6 flex justify-center">
        <Button variant="outline" onClick={onReset}>
          {t.restart}
        </Button>
      </div>
    </div>
  );
}
