'use client';

import { forwardRef, type InputHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface CheckboxProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  description?: string;
  /** Shows a red "Disqualifies" warning badge */
  disqualifier?: boolean;
  /** Custom disqualifier reason text */
  disqualifierReason?: string;
  /** Shows a green "Qualifies" badge for positive options */
  qualifier?: boolean;
  /** Custom qualifier reason text */
  qualifierReason?: string;
  /** Shows an amber "Exception" badge */
  exception?: boolean;
  /** Custom exception reason text */
  exceptionReason?: string;
}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({
    className,
    label,
    description,
    id,
    disqualifier,
    disqualifierReason,
    qualifier,
    qualifierReason,
    exception,
    exceptionReason,
    ...props
  }, ref) => {
    const inputId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`;

    return (
      <div className={cn(
        "flex items-start p-3 rounded-lg border transition-colors",
        disqualifier && "border-red-200 bg-red-50/50 hover:bg-red-50",
        qualifier && "border-green-200 bg-green-50/50 hover:bg-green-50",
        exception && "border-amber-200 bg-amber-50/50 hover:bg-amber-50",
        !disqualifier && !qualifier && !exception && "border-transparent hover:bg-gray-50"
      )}>
        <div className="flex h-5 items-center">
          <input
            ref={ref}
            type="checkbox"
            id={inputId}
            className={cn(
              'h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500',
              className
            )}
            {...props}
          />
        </div>
        {(label || description) && (
          <div className="ml-3 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              {label && (
                <label
                  htmlFor={inputId}
                  className="text-sm font-medium text-gray-900 cursor-pointer"
                >
                  {label}
                </label>
              )}
              {disqualifier && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Disqualifies
                </span>
              )}
              {qualifier && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Auto-qualifies
                </span>
              )}
              {exception && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-700">
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Exception
                </span>
              )}
            </div>
            {description && (
              <p className="text-sm text-gray-500">{description}</p>
            )}
            {disqualifier && disqualifierReason && (
              <p className="text-xs text-red-600 mt-1">{disqualifierReason}</p>
            )}
            {qualifier && qualifierReason && (
              <p className="text-xs text-green-600 mt-1">{qualifierReason}</p>
            )}
            {exception && exceptionReason && (
              <p className="text-xs text-amber-600 mt-1">{exceptionReason}</p>
            )}
          </div>
        )}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export { Checkbox };
