from django.core.validators import MinValueValidator
from django.db import models

class Patient(models.Model):
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=254)
    glucose = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    haemoglobin = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    cholesterol = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"
