# Decision Tree

This document describes the decision tree used for simplified tax eligibility determination.

## Overview

The decision tree is optimized for:
1. **Early exit** on disqualifiers
2. **Minimal questions** (≤15 top-level)
3. **Conditional subquestions** only when needed

## Flow Diagram

```
START
  │
  ▼
Q1: VAT Registered?
  │
  ├─ YES ──► NOT ELIGIBLE (218.1.1)
  │
  ▼
Q2: Automatic Route Selection (218.4)
  │
  ├─ Passenger transport/taxi (218.4.1) ──► AUTO_TRANSPORT route
  ├─ Betting/lottery (218.4.2) ──► AUTO_BETTING_LOTTERY route
  ├─ Property transfer (218.4.3) ──► Q2.C: Property exemption check
  │     │
  │     ├─ 3yr registered (218-1.1.5.1) ──► EXEMPT (0 tax)
  │     ├─ 3yr proof + one home (218-1.1.5.1-1) ──► EXEMPT (0 tax)
  │     ├─ Family gift/inheritance (102.1.3.2) ──► EXEMPT (0 tax)
  │     └─ None ──► AUTO_PROPERTY route (with 30m² exemption)
  │
  ├─ Fixed activity 220.10 (218.4.4) ──► AUTO_FIXED_220_10 route
  └─ Land transfer (218.4.5) ──► AUTO_LAND route
  │
  ▼
Q3: Trade/Catering?
  │
  └─ (Affects rate selection for 218.1.2)
  │
  ▼
Q4: Turnover (PATCH 2)
  │
  ├─ Collect: gross_turnover, vat_exempt, pos_retail, pos_services
  ├─ Calculate: adjusted_turnover with VAT-exempt exclusion + POS 0.5 coefficient
  │
  ├─ adjusted_turnover > 200k AND NOT trade/catering ──► NOT ELIGIBLE (218.1.1)
  ├─ adjusted_turnover > 200k AND trade/catering ──► TRADE_CATERING route (218.1.2)
  └─ adjusted_turnover ≤ 200k ──► GENERAL route
  │
  ▼
DISQUALIFIER CHECKS (218.5.*)
  │
  ▼
Q5: Excise/Mandatory Marking Producer?
  ├─ YES ──► NOT ELIGIBLE (218.5.1)
  │
  ▼
Q6: Financial Sector?
  │  (credit org, insurance participant, investment fund, securities, pawnshop)
  ├─ ANY YES ──► NOT ELIGIBLE (218.5.2)
  │
  ▼
Q7: Non-State Pension Fund?
  ├─ YES ──► NOT ELIGIBLE (218.5.3)
  │
  ▼
Q8: Rental/Royalty Income?
  ├─ YES ──► NOT ELIGIBLE (218.5.4)
  │
  ▼
Q9: Natural Monopoly?
  ├─ YES ──► NOT ELIGIBLE (218.5.5)
  │
  ▼
Q10: Fixed Assets > 1M AZN?
  ├─ YES ──► NOT ELIGIBLE (218.5.6)
  │
  ▼
Q11: Licensed Activities? (PATCH 3)
  │  (with comprehensive Annex 1 list)
  │
  ├─ YES, with activities selected
  │     │
  │     ├─ Q11.1: Compulsory insurance carve-out?
  │     │     ├─ YES ──► CONTINUE (carve-out applies)
  │     │     └─ NO ──► NOT ELIGIBLE (218.5.13)
  │
  ▼
Q12: Production + Employees?
  ├─ Production AND employees > 10 ──► NOT ELIGIBLE (218.5.8)
  │
  ▼
Q13: Wholesale Trade? (if does_trade)
  │
  ├─ YES ──► Q13.1: E-invoice ratio?
  │     │     ├─ > 30% ──► NOT ELIGIBLE (218.5.9)
  │     │     └─ ≤ 30% ──► CONTINUE (218.6.1 exception)
  │
  ▼
Q14: B2B Works/Services?
  │
  ├─ YES ──► Q14.1: E-invoice ratio?
  │     │     ├─ > 30% ──► NOT ELIGIBLE (218.5.10)
  │     │     └─ ≤ 30% ──► CONTINUE (218.6.2 exception)
  │
  ▼
Q15: Precious Goods / Fur?
  ├─ Gold/jewelry/diamonds ──► NOT ELIGIBLE (218.5.11)
  ├─ Fur/leather ──► NOT ELIGIBLE (218.5.12)
  │
  ▼
ALL CHECKS PASSED ──► ELIGIBLE
  │
  ▼
CALCULATE TAX (based on route)
  │
  ├─ GENERAL: 2% × turnover (220.1)
  ├─ TRADE_CATERING: 8% general, 6% POS (220.1-1)
  ├─ AUTO_PROPERTY: 15 AZN/m² × zone coefficient (220.8)
  ├─ AUTO_LAND: 2× land tax (220.8)
  └─ AUTO_TRANSPORT/BETTING/FIXED: per 220.4/220.6/220.10
  │
  ▼
RETURN RESULT
```

## Question Details

### Q1: VAT Registration (Hard Stop)
- **Type**: Boolean
- **Legal Basis**: 218.1.1
- **Early Exit**: If YES → NOT ELIGIBLE immediately

### Q2: Route Selection (Fast Pass)
- **Type**: Multi-select
- **Legal Basis**: 218.4
- **Options**: Transport, Betting, Property, Fixed 220.10, Land
- **Behavior**: If any selected, route is determined and some eligibility checks are skipped

### Q2.C: Property Exemption (PATCH 1)
- **Condition**: Only if "Property transfer" selected in Q2
- **Type**: Select
- **Legal Basis**: 218-1.1.5, 102.1.3.2
- **Options**:
  - 3-year registered (→ 0 tax)
  - 3-year proof + one home (→ 0 tax)
  - Family gift/inheritance (→ 0 tax)
  - None (→ 30m² exemption applies)

### Q4: Turnover (PATCH 2)
- **Type**: Object (structured input)
- **Legal Basis**: 218.1.1, 218.1-1, 164
- **Fields**:
  - Gross turnover (required)
  - VAT-exempt turnover
  - POS retail turnover
  - POS services turnover
- **Calculation**:
  ```
  vat_taxable = gross - vat_exempt
  adjusted = vat_taxable - pos_eligible × 0.5
  ```

### Q11: Licensed Activities (PATCH 3)
- **Type**: Multi-select
- **Legal Basis**: 218.5.13, License Law Annex 1
- **Options**: Comprehensive list from Annex 1
- **Carve-out**: Compulsory insurance contracts (218.5.2-1)

### Q13/Q14: Wholesale / B2B Exceptions
- **Type**: Object (boolean + decimal)
- **Legal Basis**: 218.5.9, 218.5.10, 218.6.1, 218.6.2
- **Exception**: If e-invoice ratio ≤ 30%, simplified tax preserved

## Question Count

| Category | Questions |
|----------|-----------|
| VAT check | 1 |
| Route selection | 1 |
| Property exemption (conditional) | 1 |
| Trade/catering | 1 |
| Turnover | 1 |
| Disqualifiers | 9 |
| **Total** | **14** |

Total top-level questions: **14** (within ≤15 requirement)

## Exit Conditions

### Early Exits (NOT ELIGIBLE)
1. VAT registered
2. Turnover > 200k (non-trade/catering)
3. Any 218.5.* disqualifier

### Success Exits (ELIGIBLE)
1. All checks pass → Calculate tax
2. Property exemption (3yr/family) → 0 tax

## Notes

- Subquestions only appear when triggered by parent answer
- Tooltips provide legal context for each question
- Debug mode shows full evaluation trace
