from datetime import date, datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Patient

DATE_FORMATS = ("%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d")

class PatientForm(forms.ModelForm):
    date_of_birth = forms.CharField(
        label="Date of birth",
        help_text="Use dd.mm.yyyy (as in the assessment sheet). dd/mm/yyyy also works.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "28.01.1960"})
    )

    class Meta:
        model = Patient
        fields = [
            "full_name", "date_of_birth", "email",
            "glucose", "haemoglobin", "cholesterol"
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"}),
            "glucose": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "haemoglobin": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "cholesterol": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }


    def clean_full_name(self):
        value = self.cleaned_data["full_name"].strip()
        if not value:
            raise ValidationError("Full name is required.")
        return value

    

    def clean_date_of_birth(self):
        raw_value = self.cleaned_data["date_of_birth"].strip()
        parsed = None
        for date_format in DATE_FORMATS:
            try:
                parsed = datetime.strptime(raw_value, date_format).date()
                break
            except ValueError:
                continue
        if parsed is None:
            raise ValidationError("Enter a real date in dd.mm.yyyy format.")
        if parsed > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        return parsed

    

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()
