/**
 * API client for the Simplified Tax Calculator backend.
 */

import type {
  EvaluateRequest,
  EvaluateResponse,
  Question,
  LicensedActivity,
} from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchWithError<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(response.status, response.statusText, errorText);
  }

  return response.json();
}

/**
 * Evaluate simplified tax eligibility and calculate tax amount.
 */
export async function evaluateSimplifiedTax(
  request: EvaluateRequest,
  debug = false
): Promise<EvaluateResponse> {
  const queryParams = debug ? '?debug=1' : '';
  return fetchWithError<EvaluateResponse>(
    `${API_URL}/api/v1/simplified-tax/evaluate${queryParams}`,
    {
      method: 'POST',
      body: JSON.stringify(request),
    }
  );
}

/**
 * Get all interview questions.
 */
export async function getQuestions(): Promise<Question[]> {
  return fetchWithError<Question[]>(`${API_URL}/api/v1/simplified-tax/questions`);
}

/**
 * Get a specific question by ID.
 */
export async function getQuestion(questionId: string): Promise<Question> {
  return fetchWithError<Question>(
    `${API_URL}/api/v1/simplified-tax/questions/${questionId}`
  );
}

/**
 * Get licensed activities list for Q11.
 */
export async function getLicensedActivities(
  search?: string,
  category?: string
): Promise<{ activities: LicensedActivity[]; categories: Record<string, string> }> {
  const params = new URLSearchParams();
  if (search) params.set('search', search);
  if (category) params.set('category', category);

  const queryString = params.toString();
  const url = `${API_URL}/api/v1/simplified-tax/licensed-activities${
    queryString ? `?${queryString}` : ''
  }`;

  return fetchWithError(url);
}

/**
 * Health check.
 */
export async function healthCheck(): Promise<{ status: string; version: string }> {
  return fetchWithError(`${API_URL}/health`);
}

export { ApiError };
