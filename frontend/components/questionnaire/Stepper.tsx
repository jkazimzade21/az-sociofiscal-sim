'use client';

import { cn } from '@/lib/utils';

interface Step {
  id: string;
  label: string;
  completed: boolean;
  current: boolean;
}

interface StepperProps {
  steps: Step[];
  currentStep: number;
}

export function Stepper({ steps, currentStep }: StepperProps) {
  return (
    <nav aria-label="Progress" className="mb-8">
      <ol className="flex items-center justify-between">
        {steps.map((step, index) => (
          <li key={step.id} className="stepper-item flex-1">
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  step.completed
                    ? 'stepper-circle-complete'
                    : step.current
                      ? 'stepper-circle-active'
                      : 'stepper-circle-pending'
                )}
              >
                {step.completed ? (
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                ) : (
                  index + 1
                )}
              </div>
              <span
                className={cn(
                  'mt-2 text-xs font-medium',
                  step.current ? 'text-primary-600' : 'text-gray-500'
                )}
              >
                {step.label}
              </span>
            </div>
            {index < steps.length - 1 && (
              <div
                className={cn(
                  'flex-1 h-0.5 mx-2 mt-5',
                  index < currentStep ? 'bg-primary-600' : 'bg-gray-300'
                )}
              />
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
