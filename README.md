# FinancialTrackingApp

**************************
- WHAT IS FINANCIAL TRACKING APP:
**************************
Financial Tracking Application allows you to easily track your financial income and expense. You can track your one-time income and expenses, as well as all your income and expenses in installments or for a period.

**************************
- HOW TO RUN PROJECT:
**************************

* Requirements:
  - Python 3.9
  - PostgresSQL

-> Download all package: ```pip install -r requirements.txt``` (file-path: /FinancialTracking) root

-> Also setup ```pip install python-jose[cryptography]```

-> Add ```.env``` file as descripted bellow (Check: ENV FILE)

-> Run Alembic: ```alembic revision --autogenerate```

-> Update Alembic: ```alembic upgrade head```

-> Run the project: uvicorn src.app:app --reload

**************************
- ENV FILE:
**************************
DB_USERNAME=

DB_PASSWORD=

DB_HOST=

DB_PORT=

DB_NAME=

SECRET_KEY=

ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

GOOGLE_CLIENT_ID=

GOOGLE_CLIENT_SECRET=


**************************
- SWAGGER UI: http://127.0.0.1:8000/docs
**************************

