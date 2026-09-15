                    ┌─────────────────────┐
                    │      React UI       │
                    │                     │
                    │ Calculator           │
                    │ History              │
                    │ Results              │
                    └──────────┬──────────┘
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │    Django REST      │
                    │                     │
                    │ API endpoints       │
                    │ Calculation logic   │
                    │ Validation          │
                    │ Authentication      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL       │
                    │                     │
                    │ Calculations        │
                    │ Users               │
                    │ History             │
                    └─────────────────────┘


Phase 1 — UI

Modern calculator interface
Responsive React layout
CSS animations
Keyboard support
Dark/light theme
Scientific/basic calculator modes

Phase 2 — Backend

Django project
Django REST Framework
Calculation API
Input validation
Error handling

Phase 3 — Database

PostgreSQL
Calculation history
User-specific history
Timestamps
Saved calculations

Phase 4 — Integration

React ↔ REST API
Loading/error states
History panel
Delete/clear history

Phase 5 — Quality

Django unit tests
API tests
React tests
Security review
Docker
Production configuration