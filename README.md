# Travel Bucket List API

## Setup

1. Activate virtual environment:
```bash
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database:
- Copy `.env.example` to `.env`
- Update `DATABASE_URL` in `database.py` with your Neon DB connection string

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /destinations/` - Add new destination
- `GET /destinations/` - Get all destinations
- `GET /destinations/{id}` - Get specific destination
- `PUT /destinations/{id}` - Update destination
- `DELETE /destinations/{id}` - Delete destination
- `PATCH /destinations/{id}/visited` - Toggle visited status

## Example Request Body

```json
{
  "place_name": "Tokyo",
  "country": "Japan",
  "priority": "High",
  "notes": "Visit during cherry blossom season"
}
```