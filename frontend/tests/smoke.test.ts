/**
 * Smoke tests for the frontend.
 */

import { describe, it, expect } from 'vitest';

describe('Smoke Tests', () => {
  it('should have correct types defined', () => {
    // Import types to ensure they compile
    const types = require('../lib/types');
    expect(types).toBeDefined();
  });

  it('should have API client defined', () => {
    const api = require('../lib/api');
    expect(api.evaluateSimplifiedTax).toBeDefined();
    expect(api.getQuestions).toBeDefined();
    expect(api.getLicensedActivities).toBeDefined();
  });

  it('should have utility functions defined', () => {
    const utils = require('../lib/utils');
    expect(utils.cn).toBeDefined();
    expect(utils.formatCurrency).toBeDefined();
    expect(utils.getRouteName).toBeDefined();
  });
});
