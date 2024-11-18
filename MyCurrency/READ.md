MyCurrency: Currency Exchange Rate Platform
MyCurrency is a web platform that allows users to calculate currency exchange rates. It integrates with external providers (like CurrencyBeacon) to retrieve and store daily currency rates. The project is built with Django and Django REST Framework, designed with flexibility to support multiple providers.

Key Features
Currency CRUD: Manage currencies (Create, Read, Update, Delete).
Exchange Rates API: Fetch currency exchange rates for specific periods.
Currency Conversion: Convert an amount from one currency to another.
Provider Priority: Dynamically change the default provider for exchange rates.
Resilience: Automatically switch to the next available provider if the default fails.
Historical Data Loading: Efficiently load and process historical currency data asynchronously.
Django Admin: Includes a converter view to showcase the currency conversion feature.


Technologies Used
Python: 3.11
Django: 4.x / 5.x
Django REST Framework: For building the RESTful API
Celery: For asynchronous historical data loading
Redis: As the Celery broker
PostgreSQL: Database for storing currency and exchange rate data


Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/mycurrency.git
cd mycurrency

2. Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Set Up the Environment Variables
Create a .env file in the project root and add the following:

makefile
Copy code
DEBUG=True
SECRET_KEY=your_django_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/mycurrency
CURRENCY_BEACON_API_KEY=your_currency_beacon_api_key

5. Apply Migrations
python manage.py migrate

6. Run the Development Server
python manage.py runserver

7. Start Celery Worker

celery -A mycurrency worker --loglevel=info


8. Access the Application
Admin Panel: http://localhost:8000/admin
API Endpoints: http://localhost:8000/api/


API Endpoints
1. Currency CRUD
List Currencies: GET /api/currencies/
Create Currency: POST /api/currencies/
Update Currency: PUT /api/currencies/<id>/
Delete Currency: DELETE /api/currencies/<id>/
2. Exchange Rates
List Exchange Rates: GET /api/exchange-rates/
Parameters: source_currency, date_from, date_to
3. Currency Conversion
Convert Currency: GET /api/convert/
Parameters: source_currency, amount, exchanged_currency


How It Works:

Retrieve Exchange Rates: Rates are fetched from the database or the configured provider using the get_exchange_rate_data() service.
Adapter Pattern: Supports multiple providers, ensuring flexibility for future integrations.
Dynamic Provider Priority: Admins can configure provider priorities dynamically.
Resilient Design: Automatically switches to the next provider if one fails.
Django Admin: Provides a user-friendly interface for managing currencies and testing conversions.

Testing:

Run the unit tests using Django's test runner or pytest:

python manage.py test
# Or
pytest
Django Admin Features
Currency Management: Add, edit, or delete currencies.
Converter View: Test currency conversions directly from the admin panel.
Historical Data Loader
Function: load_historical_data() asynchronously fetches and stores historical exchange rates.


How to Run:

python manage.py load_historical_data --provider=currency_beacon --start-date=YYYY-MM-DD --end-date=YYYY-MM-DD
Future Enhancements
Add support for more providers.
Implement API versioning.
Add caching for frequent queries.
Improve rate fetching performance.