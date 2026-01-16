# Data Dictionary

This document defines all variables and parameters used in the Azerbaijan Simplified Tax Calculator.

## Input Variables

### VAT Status
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `is_vat_registered` | boolean | Whether taxpayer is VAT registered | 218.1.1 |

### Route Selection (218.4)
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `route_auto_transport` | boolean | Passenger transport/taxi activity | 218.4.1 |
| `route_auto_betting_lottery` | boolean | Betting/lottery activity | 218.4.2 |
| `route_auto_property` | boolean | Transfer/sale of own real estate | 218.4.3 |
| `route_auto_fixed_220_10` | boolean | Fixed activity under 220.10 without employees | 218.4.4 |
| `route_auto_land` | boolean | Sale/transfer of own land | 218.4.5 |

### Property Transfer
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `property_type` | enum | RESIDENTIAL or NON_RESIDENTIAL | 220.8 |
| `area_m2` | decimal | Property area in square meters | 220.8 |
| `location_zone` | enum | Zone for coefficient determination | 220.8.1-4 |
| `is_registered_3yr` | boolean | Registered at address ≥3 years | 218-1.1.5.1 |
| `has_proof_3yr_one_home` | boolean | Proof of 3yr + one home only | 218-1.1.5.1-1 |
| `is_family_gift_inheritance` | boolean | Family gift/inheritance | 102.1.3.2 |

### Turnover (PATCH 2)
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `gross_turnover_12m` | decimal | Total gross turnover for 12 months | 218.1.1 |
| `vat_exempt_turnover_12m` | decimal | VAT-exempt turnover (Art 164) | 218.1.1, 164 |
| `vat_exempt_categories` | list[enum] | Categories of VAT-exempt operations | 164 |
| `pos_retail_nonregistered_12m` | decimal | POS retail to unregistered persons | 218.1-1 |
| `pos_services_nonregistered_12m` | decimal | POS services to unregistered persons | 218.1-1 |

### Activity Type
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `does_trade` | boolean | Engaged in trade activity | 218.1.2 |
| `does_catering` | boolean | Engaged in public catering | 218.1.2 |
| `does_production` | boolean | Conducts production activity | 218.5.8 |
| `does_wholesale` | boolean | Conducts wholesale trade | 218.5.9 |
| `does_b2b_works_services` | boolean | Performs B2B works/services | 218.5.10 |

### Disqualifiers
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `produces_excise_goods` | boolean | Produces excise/mandatory-label goods | 218.5.1 |
| `is_credit_org` | boolean | Is a credit organization | 218.5.2 |
| `is_insurance_market_participant` | boolean | Insurance market participant | 218.5.2 |
| `is_investment_fund` | boolean | Investment fund or manager | 218.5.2 |
| `is_securities_licensed` | boolean | Securities market licensed | 218.5.2 |
| `is_pawnshop` | boolean | Is a pawnshop | 218.5.2 |
| `is_non_state_pension_fund` | boolean | Non-state pension fund | 218.5.3 |
| `has_rental_income` | boolean | Has rental income | 218.5.4 |
| `has_royalty_income` | boolean | Has royalty income | 218.5.4 |
| `is_natural_monopoly` | boolean | Is a natural monopoly | 218.5.5 |
| `fixed_assets_residual_value` | decimal | Fixed assets value at year start | 218.5.6 |
| `is_public_legal_entity` | boolean | Is a public legal entity | 218.5.7 |
| `avg_quarterly_employees` | integer | Average quarterly employee count | 218.5.8 |
| `sells_gold_jewelry_diamonds` | boolean | Sells gold/jewelry/diamonds | 218.5.11 |
| `sells_fur_leather` | boolean | Sells fur/leather products | 218.5.12 |

### Licensed Activities (PATCH 3)
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `licensed_activity_codes` | list[enum] | Licensed activities from Annex 1 | 218.5.13 |
| `has_compulsory_insurance_carveout` | boolean | Only compulsory insurance services | 218.5.13 |

### Exception Ratios
| Variable | Type | Description | Legal Basis |
|----------|------|-------------|-------------|
| `wholesale_einvoice_ratio` | decimal | E-invoiced wholesale / total trade | 218.6.1 |
| `b2b_einvoice_ratio` | decimal | E-invoiced B2B / total works/services | 218.6.2 |

## Calculated Variables

| Variable | Formula | Description | Legal Basis |
|----------|---------|-------------|-------------|
| `vat_taxable_turnover` | gross - vat_exempt | VAT-taxable operations | 218.1.1 |
| `pos_eligible` | pos_retail + pos_services | Total POS eligible turnover | 218.1-1 |
| `adjusted_turnover` | vat_taxable - (pos_eligible × 0.5) | Adjusted turnover for threshold | 218.1-1 |

## Output Variables

| Variable | Type | Description |
|----------|------|-------------|
| `eligible` | boolean | Eligibility for simplified tax |
| `tax_amount` | decimal | Calculated tax amount (AZN) |
| `route` | enum | Tax route/category |
| `tax_base` | decimal | Tax calculation base |
| `tax_rate` | decimal | Applied tax rate |
| `exemptions_applied` | list[string] | List of exemptions applied |
| `reason_code` | string | Disqualification reason (if not eligible) |
| `reason_description` | string | Human-readable reason |
| `legal_basis` | list[object] | Legal citations |
| `debug_trace` | list[object] | Evaluation trace (debug mode) |

## Enumerations

### TaxRoute
| Value | Description | Legal Basis |
|-------|-------------|-------------|
| `general` | Standard simplified tax | 218.1.1, 220.1 |
| `trade_catering_over_200k` | Trade/catering >200k | 218.1.2, 220.1-1 |
| `auto_transport` | Passenger transport/taxi | 218.4.1 |
| `auto_betting_lottery` | Betting/lottery | 218.4.2 |
| `auto_property` | Own real estate transfer | 218.4.3 |
| `auto_land` | Own land transfer | 218.4.5 |
| `auto_fixed_220_10` | Fixed activity 220.10 | 218.4.4 |

### PropertyType
| Value | Description |
|-------|-------------|
| `residential` | Residential property |
| `non_residential` | Non-residential property |

### LocationZone
| Value | Coefficient | Legal Basis |
|-------|-------------|-------------|
| `baku_center` | 2.5 | 220.8.1 |
| `baku_other` | 2.0 | 220.8.2 |
| `sumgait_ganja_lankaran` | 1.5 | 220.8.3 |
| `other_cities` | 1.2 | 220.8.3 |
| `rural` | 1.0 | 220.8.4 |

### LicensedActivityCode
| Value | Description (EN) | Description (AZ) |
|-------|------------------|------------------|
| `private_medical` | Private medical activity | Özəl tibb fəaliyyəti |
| `education` | Education activity | Təhsil fəaliyyəti |
| `communications` | Communications services | Rabitə xidmətləri |
| `fire_protection` | Fire protection activity | Yanğından mühafizə fəaliyyəti |
| `construction_survey` | Engineering surveys | Mühəndis axtarışları |
| `construction_install` | Construction-installation | Tikinti-quraşdırma |
| `construction_design` | Design | Layihələndirmə |
| `pharmaceutical` | Pharmaceutical activity | Əczaçılıq fəaliyyəti |
| `veterinary` | Veterinary activity | Baytarlıq fəaliyyəti |
| `auditing` | Auditing services | Audit xidməti |
| `notary` | Notary activity | Notariat fəaliyyəti |
| `legal_services` | Legal services | Vəkillik fəaliyyəti |
| `security_services` | Security services | Mühafizə fəaliyyəti |
| `gambling` | Gambling | Qumar oyunları |
| `alcohol_production` | Alcohol production | Spirtli içkilər istehsalı |
| `tobacco_production` | Tobacco production | Tütün məmulatları istehsalı |
| `banking` | Banking | Bank fəaliyyəti |
| `insurance` | Insurance | Sığorta fəaliyyəti |
| `securities` | Securities market | Qiymətli kağızlar bazarı |
| `other` | Other licensed activity | Digər lisenziyalı fəaliyyət |

## Constants

| Constant | Value | Description | Legal Basis |
|----------|-------|-------------|-------------|
| `TURNOVER_THRESHOLD` | 200,000 AZN | 12-month turnover limit | 218.1.1 |
| `POS_COEFFICIENT` | 0.5 | POS turnover coefficient | 218.1-1 |
| `FIXED_ASSETS_THRESHOLD` | 1,000,000 AZN | Fixed assets limit | 218.5.6 |
| `EMPLOYEE_THRESHOLD` | 10 | Production employee limit | 218.5.8 |
| `EXCEPTION_RATIO_THRESHOLD` | 0.30 (30%) | Wholesale/B2B exception | 218.6.1-2 |
| `GENERAL_TAX_RATE` | 0.02 (2%) | General simplified rate | 220.1 |
| `TRADE_GENERAL_RATE` | 0.08 (8%) | Trade/catering general | 220.1-1 |
| `TRADE_POS_RATE` | 0.06 (6%) | Trade/catering POS | 220.1-1 |
| `PROPERTY_TAX_PER_M2` | 15 AZN | Property tax per m² | 220.8 |
| `PROPERTY_EXEMPT_AREA` | 30 m² | Residential exemption | 218-1.1.5.3 |
