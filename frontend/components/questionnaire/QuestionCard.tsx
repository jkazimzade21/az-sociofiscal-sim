'use client';

import { ReactNode } from 'react';
import { Tooltip } from '@/components/ui';
import { cn } from '@/lib/utils';

interface QuestionCardProps {
  question: string;
  questionAz?: string;
  tooltip?: string;
  tooltipAz?: string;
  legalBasis?: string;
  children: ReactNode;
  className?: string;
}

export function QuestionCard({
  question,
  questionAz,
  tooltip,
  tooltipAz,
  legalBasis,
  children,
  className,
}: QuestionCardProps) {
  return (
    <div className={cn('card', className)}>
      <div className="mb-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">{question}</h2>
            {questionAz && (
              <p className="text-sm text-gray-500 mt-1">{questionAz}</p>
            )}
          </div>
          {(tooltip || tooltipAz) && (
            <Tooltip
              content={
                <div>
                  {tooltip && <p>{tooltip}</p>}
                  {tooltipAz && (
                    <p className="mt-2 text-gray-300 text-xs">{tooltipAz}</p>
                  )}
                </div>
              }
              position="left"
            >
              <button
                type="button"
                className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-100 text-gray-500 hover:bg-gray-200 flex items-center justify-center text-sm"
              >
                ?
              </button>
            </Tooltip>
          )}
        </div>
        {legalBasis && (
          <div className="mt-2">
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800">
              {legalBasis}
            </span>
          </div>
        )}
      </div>
      {children}
    </div>
  );
}
