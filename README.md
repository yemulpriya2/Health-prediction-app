# Health Prediction & Patient Records Application

A Python assessment project built with Django, Django REST Framework, Bootstrap, SQLite and the Groq API.

> **Important:** AI remarks are educational risk-awareness text, not medical diagnoses or treatment advice. The application must not be used to make clinical decisions.

## Features

- Create, read, update and delete patient records.
- Validate email addresses, dates of birth and numeric blood-test values.
- Reject dates in the future and impossible calendar dates.
- Accept dates in `dd.mm.yyyy`, `dd/mm/yyyy` or ISO `yyyy-mm-dd` format.
- Generate informational remarks using the external Groq API.
- Keep patient records in SQLite.
- Expose CRUD endpoints through Django REST Framework.
- Search patient records in the web interface.
- Allow duplicate records (the assessment includes the same patient twice).

## Technology

- Python 3.10+
- Django 5.2
- Django REST Framework
- SQLite
- HTML, CSS, Bootstrap 5 and JavaScript
- Groq Chat Completions API
- python-dotenv

## 1. Setup

Open a terminal in the project folder.

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure the AI API

1. Create an API key in your Groq account.
2. Put your key in `GROQ_API_KEY`.
3. Keep `.env` private. It is excluded by `.gitignore`.

Example:

```env
GROQ_API_KEY=your_real_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DEBUG=True
SECRET_KEY=use-a-long-random-secret
```

The model name is configurable. If Groq retires or changes model availability, set `GROQ_MODEL` to a currently supported model in your Groq account.

If no API key is configured, records can still be saved, but the remarks field will explain that AI generation was not run. Configure the key to demonstrate the external API integration.

## 3. Create the database and run

```bash
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## 4. Assessment test data

Enter the ten rows exactly as shown in the assessment PDF. Do not silently correct the supplied values.

Expected validation behaviour:

| Test | Expected result | Reason |
|---|---|---|
| 1 Robyn Pears | Accept | Valid fields |
| 2 John Hunter | Reject | `hunter@gmail` is not a valid email address |
| 3 Darryl Tim | Accept | Valid fields |
| 4 Peter Larry | Reject | 31 November is not a valid calendar date |
| 5 Sam Kerr | Accept | Valid fields |
| 6 Robyn Pears | Accept | Duplicate records are permitted |
| 7 Madison XI | Accept | Valid fields |
| 8 Kris Wu | Reject | Future date of birth and invalid email |
| 9 Tenille Singh | Accept | Valid fields |
| 10 Prem Kumar | Accept | Valid fields |

Expected result: 7 records saved and 3 rejected. The form accepts dates with dots as supplied in the PDF, as well as slashes.

After creating the records:
1. Open the patient list and show all saved records.
2. Edit any one record and change its email to `gokul@infocare.com`.
3. Delete any one record.
4. Show the list again.

## 5. API endpoints

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/patients/` | List records |
| POST | `/api/patients/` | Create record |
| GET | `/api/patients/<id>/` | Retrieve one record |
| PUT/PATCH | `/api/patients/<id>/` | Update record |
| DELETE | `/api/patients/<id>/` | Delete record |

Example JSON for `POST /api/patients/`:

```json
{
  "full_name": "Alex Morgan",
  "date_of_birth": "1995-04-18",
  "email": "alex@example.com",
  "glucose": "98",
  "haemoglobin": "14.2",
  "cholesterol": "185"
}
```

The API generates AI remarks on create and update. If the API key is missing or the provider is unavailable, the patient record is still saved and the remarks field explains the failure.

## 6. Postman demonstration

- GET `http://127.0.0.1:8000/api/patients/`
- POST `http://127.0.0.1:8000/api/patients/` with the JSON above.
- PATCH `http://127.0.0.1:8000/api/patients/1/` to change a field.
- DELETE `http://127.0.0.1:8000/api/patients/1/`


## Medical safety

The application sends the three supplied numeric values to an external AI provider to generate general educational remarks. Do not use real patient information without appropriate consent, security controls, privacy review and legal compliance. AI output can be wrong and is not a diagnosis.
