
# test_api

A Django REST API project with endpoints for Bitcoin conversion and contact import.

## Requirements

- Python 3.11+
- PostgreSQL
- Redis


## Local Development Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/oleslaw/test_api.git
   cd test_api
   ```

2. **Install dependencies**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL and Redis**
   - Ensure PostgreSQL and Redis are running locally.
   - Create a PostgreSQL database and user matching the defaults in [`api/settings.py`](api/settings.py) or set environment variables:
     - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
   - Redis defaults to `localhost:6379`.

4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run Celery worker and beat**
   ```sh
   ./run_celery.sh
   ```
   (on production environment this would be two separate background workers)

7. **Run the development server**
   ```sh
   python manage.py runserver
   ```


## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting.

- To check code style and linting issues, run:
  ```sh
  ruff check .
  ```

- To automatically format the code, run:
  ```sh
  ruff format .
  ```

Make sure to run these commands before committing changes to keep the codebase clean and consistent.

If needed, the production version could use other tools like tox, mypy, etc.

## Running Tests

To run the test suite:
```sh
python manage.py test
```

## API Endpoints

### Bitcoin Conversion

- **GET `/bitcoin/convert/`**

  Convert the price of Bitcoin from one currency to another using cached rates.

  **Query Parameters:**
  - `source_currency` (string, required): One of `EUR`, `GBP`, `USD`, `JPY`, `CHF`, `AUD`
  - `target_currency` (string, required): One of `EUR`, `GBP`, `USD`, `JPY`, `CHF`, `AUD`

  **Example Request:**
  ```
  GET /bitcoin/convert/?source_currency=USD&target_currency=EUR
  ```

  **Response:**
  - `200 OK` with JSON:
    ```json
    {
      "bitcoin_price": 30000,
      "exchange_rate": 0.9,
      "converted_price": 27000
    }
    ```
  - `400 Bad Request` if parameters are missing or invalid.
  - `404 Not Found` if rates are not available.

  See implementation: [`api.bitcoin.views.BitcoinConversionView`](api/bitcoin/views.py)

### Contacts Import

- **POST `/contacts/import/`**

  Import contacts from a CSV file.

  **Request:**
  - Content-Type: `multipart/form-data`
  - Field: `file` (CSV file with columns: `first_name`, `last_name`, `email`, `phone`)

  **Example Request:**
  ```
  POST /contacts/import/
  ```

  **Response:**
  - `201 Created` with JSON:
    ```json
    { "imported": 2 }
    ```
  - `400 Bad Request` if file is missing or data is invalid.

  See implementation: [`api.contacts.views.ContactImportView`](api/contacts/views.py)

### Admin

- **/admin/** — Django admin interface.

## Project Structure

- [`api/`](api/) — Django project and apps
- [`api/bitcoin/`](api/bitcoin/) — Bitcoin conversion logic
- [`api/contacts/`](api/contacts/) — Contacts import logic

## Hosted API

The API is deployed at: https://test-api-yi69.onrender.com

You can access the endpoints directly or use the provided Postman collection.

## Postman Collection

A Postman collection for testing the API is included in the repo as `postman_collection.json`.

## Notes

- Celery is used for background tasks and requires Redis. It is responsible for periodically refreshing Bitcoin and exchange rates.
- Exchange and Bitcoin rates are cached for performance.
- Cache was not required for the BTC conversion but I wanted it to more closely resemble what I would do in a real application.
- Also, the endpoint for acquiring BTC rates already has prices in different currencies, but I purposefully used the European Central Bank API to satisfy the assignment requirements.

## Security

The default secret key and DEBUG=True are for development only. For production, set a secure secret key and disable DEBUG.