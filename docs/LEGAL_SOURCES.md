# Legal Sources

This document lists all legal sources used in the Azerbaijan Simplified Tax Calculator.

**Last Verified**: January 2026

## Primary Sources

### 1. Azerbaijan Tax Code (Vergi Məcəlləsi)

**URL**: https://taxes.gov.az/az/page/vergi-mecellesi

**Relevant Articles**:

#### Article 218 - Simplified Tax Eligibility

- **218.1.1**: Turnover threshold (200,000 AZN for consecutive 12 months)
  - "sadələşdirilmiş vergi ödəyicisi kimi qeydiyyata alınmış vergi ödəyicilərinin əməliyyatları ƏDV-yə cəlb edilmir"
  - Uses "vergi tutulan əməliyyatlar həcmi" (VAT-taxable operations)

- **218.1.2**: Trade/catering over 200k threshold
  - Different rates apply (see 220.1-1)

- **218.1-1**: POS coefficient
  - "nağdsız qaydada aparılan əməliyyatların həcmi 0,5 əmsalı ilə nəzərə alınır"
  - POS non-cash turnover counted at 0.5 coefficient

- **218.4**: Automatic simplified tax categories
  - 218.4.1: Passenger transport/taxi
  - 218.4.2: Betting/lottery
  - 218.4.3: Transfer/sale of own real estate
  - 218.4.4: Fixed activity under 220.10 without employees
  - 218.4.5: Sale/transfer of own land

- **218.5**: Disqualifiers
  - 218.5.1: Excise/mandatory marking producers
  - 218.5.2: Credit orgs, insurance market participants, investment funds, securities market licensed persons, pawnshops
  - 218.5.3: Non-state pension funds
  - 218.5.4: Rental/royalty income
  - 218.5.5: Natural monopolies
  - 218.5.6: Fixed assets > 1,000,000 AZN
  - 218.5.7: Public legal entities
  - 218.5.8: Production + avg quarterly employees > 10
  - 218.5.9: Wholesale trade
  - 218.5.10: B2B works/services
  - 218.5.11: Gold/jewelry/diamonds
  - 218.5.12: Fur/leather products
  - 218.5.13: Licensed activities (with compulsory insurance carve-out)

- **218.6**: Exceptions that preserve eligibility
  - 218.6.1: Wholesale ≤30% of quarterly trade operations
  - 218.6.2: B2B ≤30% of quarterly works/services operations

- **218.7**: When simplified right is canceled

#### Article 218-1 - Property Exemptions

- **218-1.1.5.1**: 3-year registration exemption
  - "Həmin yaşayış sahəsinin ünvanında azı 3 təqvim ili qeydiyyatda olduqda vergidən azaddır"

- **218-1.1.5.1-1**: 3-year proof + one home exemption
  - Proof via utility subscriber certificates
  - Only one residential property ownership

- **218-1.1.5.2**: Family gift/inheritance exemption (references 102.1.3.2)

- **218-1.1.5.3**: 30 m² exemption
  - "mülkiyyətində olan yaşayış sahəsinin ilk 30 kvadratmetri vergidən azaddır"

#### Article 219 - Simplified Tax Base

- Defines the tax base for simplified tax calculations

#### Article 220 - Simplified Tax Rates

- **220.1**: General rate = 2%
  - "Sadələşdirilmiş verginin dərəcəsi vergi tutulan əməliyyatların həcminin 2 faizi"

- **220.1-1**: Trade/catering over 200k
  - 8% general rate
  - 6% for POS (effective 2026-01-01 for 3 years)

- **220.8**: Property transfer tax
  - 15 AZN per m²
  - Zone coefficients (220.8.1-220.8.4)

- **220.10**: Fixed activity amounts

#### Article 164 - VAT Exemptions

- **164.1.2**: Financial services (VAT-exempt)
- **164.1.8**: Textbook production-related publishing/printing (VAT-exempt)

#### Article 102 - Income Tax Exemptions

- **102.1.3.2**: Family gift/inheritance exemption
  - "Ailə üzvləri arasında əmlakın bağışlanması vergidən azaddır"

### 2. License Law ("Lisenziyalar və icazələr haqqında")

**URL**: https://president.az/az/documents/licenses

**Annex 1**: List of licensed activities

Categories include:
- Healthcare (Özəl tibb fəaliyyəti, Əczaçılıq fəaliyyəti, etc.)
- Education (Təhsil fəaliyyəti)
- Communications (Rabitə xidmətləri)
- Construction (permit-required buildings)
- Financial Services
- Security Services
- Professional Services
- Manufacturing
- Transport

## How to Update When Law Changes

1. **Monitor Official Sources**:
   - Check taxes.gov.az for Tax Code amendments
   - Check president.az for License Law updates

2. **Update Process**:
   - Update relevant constants in `az_sim/variables/thresholds.py`
   - Update rates in `az_sim/parameters/rates.py`
   - Update licensed activities in `az_sim/parameters/licensed_activities.py`
   - Update legal citations in code comments
   - Update this document with new verification date
   - Run all tests to ensure compliance

3. **Version Control**:
   - Tag releases with law effective dates
   - Document changes in CHANGELOG.md

## Notes on Implementation

### Strikethrough Text
The taxes.gov.az HTML contains strikethrough markup (~~deleted~~) for repealed provisions. The implementation ignores deleted text and uses only effective (non-strikethrough) text.

### Legal Disclaimer
This calculator is for informational purposes only. Always consult with a qualified tax professional for official tax advice.
