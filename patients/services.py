import os
import requests

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_health_remarks(patient):
    """
    Ask Groq for cautious, educational wording.
    This is not a clinical prediction and must not be presented as a diagnosis.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        return "AI remarks not generated: configure GROQ_API_KEY in your local .env file."

    prompt = f"""
You are generating a short educational note for a patient-record demonstration app.
Values supplied:
- Glucose: {patient.glucose}
- Haemoglobin: {patient.haemoglobin}
- Cholesterol: {patient.cholesterol}

Write 2-3 cautious sentences. Do not diagnose a disease, calculate a disease probability,
recommend medication, or claim certainty. Explain that interpretation depends on units,
fasting status, age, medical history and laboratory reference ranges. Recommend discussing
results with a qualified healthcare professional. If a value may warrant follow-up, say
only that it may merit professional review. Do not invent units or reference ranges.
"""

    try:
        response = requests.post(
            GROQ_CHAT_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You provide cautious general health education, never medical diagnosis."
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 180,
            },
            timeout=25,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException:
        return "AI remarks could not be generated because the external AI service is unavailable. Please try again."
    except (KeyError, IndexError, TypeError, ValueError):
        return "AI remarks could not be generated because the API returned an unexpected response."
