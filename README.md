# Azerbaijan Simplified Tax Calculator (Pilot)

A production-ready web application for determining simplified tax eligibility and calculating tax amounts based on the Azerbaijan Tax Code.

## Features

- **Eligibility Determination**: Check if you qualify for simplified tax regime
- **Tax Calculation**: Calculate the exact tax amount based on your route
- **Legal Traceability**: Every rule linked to Tax Code article numbers
- **Minimal Questions**: Only 10-15 questions with smart conditional logic
- **Debug Mode**: Full rule trace for developers (add `?debug=1`)
- **Bilingual**: English and Azerbaijani support

## Legal Basis

This calculator implements rules from:
- **Tax Code Articles**: 218, 218-1, 219, 220, 164, 102.1.3.2
- **License Law Annex 1**: Licensed activity determination

See [LEGAL_SOURCES.md](docs/LEGAL_SOURCES.md) for complete legal references.

## Quick Start

### Using Docker (Recommended)

```bash
# Build and start all services
docker compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Local Development

```bash
# Backend
cd backend
pip install -e ".[dev]"
uvicorn api.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Project Structure

```
az-sociofiscal-sim/
├── backend/
│   ├── az_sim/                 # Rules engine
│   │   ├── variables/          # Variable definitions
│   │   ├── parameters/         # Configurable parameters
│   │   ├── entities.py         # Data models
│   │   └── engine.py           # Core calculation engine
│   ├── api/                    # FastAPI application
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic
│   │   └── schemas/            # Pydantic schemas
│   └── tests/                  # Backend tests
├── frontend/
│   ├── app/                    # Next.js pages
│   ├── components/             # React components
│   └── lib/                    # Utilities and types
├── docs/
│   ├── LEGAL_SOURCES.md        # Legal references
│   ├── DECISION_TREE.md        # Decision flow
│   └── DATA_DICTIONARY.md      # Variable definitions
└── docker-compose.yml
```

## API Endpoints

### POST /api/v1/simplified-tax/evaluate

Evaluate eligibility and calculate tax.

```bash
curl -X POST http://localhost:8000/api/v1/simplified-tax/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "is_vat_registered": false,
    "turnover": {
      "gross_turnover_12m": 150000
    }
  }'
```

Response:
```json
{
  "eligible": true,
  "tax_amount": "3000.00",
  "currency": "AZN",
  "route": "general",
  "tax_rate": "0.02",
  "legal_basis": [
    {
      "article": "220.1",
      "description": "General simplified tax rate of 2%"
    }
  ]
}
```

### GET /api/v1/simplified-tax/questions

Get all interview questions.

### GET /api/v1/simplified-tax/licensed-activities

Get licensed activities list (for PATCH 3 implementation).

## Key Implementation Details

### PATCH 1: Property Sale Exemptions (218-1.1.5)

When selling residential property, the calculator checks:
1. 3-year registration at address → **0 tax**
2. 3-year proof + one home only → **0 tax**
3. Family gift/inheritance (102.1.3.2) → **0 tax**
4. Otherwise → 30 m² exemption applies

### PATCH 2: Turnover Definition

The 200,000 AZN threshold uses:
- **VAT-taxable** operations only (excluding Art 164 exemptions)
- **POS coefficient**: Non-cash retail/services to unregistered persons counted at 0.5

Formula:
```
adjusted_turnover = (gross - vat_exempt) - (pos_eligible × 0.5)
```

### PATCH 3: Licensed Activities

Users select from Annex 1 list with examples:
- Private medical activity (Özəl tibb fəaliyyəti)
- Education activity (Təhsil fəaliyyəti)
- Communications services (Rabitə xidmətləri)
- Construction work (permit-required buildings)

**Carve-out**: Compulsory insurance contract services are exempt from disqualification.

## Testing

```bash
# Run all tests
make test

# Backend tests only
make test-backend

# Frontend tests only
make test-frontend
```

## Development Commands

```bash
make dev           # Start both services in dev mode
make test          # Run all tests
make lint          # Run linters
make format        # Format code
make build         # Build Docker images
make up            # Start Docker containers
```

## Extending to Other Regimes

The architecture supports extension to other tax regimes:

1. **Add new variables** in `az_sim/variables/`
2. **Add new parameters** in `az_sim/parameters/`
3. **Create new engine** (or extend existing) in `az_sim/`
4. **Add API routes** in `api/routes/`
5. **Update frontend** questionnaire and result display

## Assumptions & Versioning

### Current Version
- Based on Tax Code as of January 2026
- POS 6% rate effective from 2026-01-01

### Assumptions
1. Strikethrough text in taxes.gov.az HTML is ignored
2. Zone coefficients are simplified (actual zones may have sub-zones)
3. 220.10 fixed activities use placeholder calculations

### Updating for Law Changes
See [LEGAL_SOURCES.md](docs/LEGAL_SOURCES.md#how-to-update-when-law-changes) for update procedures.

## License

This project is for educational and informational purposes. Always consult a qualified tax professional for official tax advice.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new rules
4. Ensure all tests pass
5. Submit a pull request

## Disclaimer

This calculator is provided for informational purposes only and does not constitute tax advice. The results should not be relied upon for making tax decisions. Always consult with a qualified tax professional.
