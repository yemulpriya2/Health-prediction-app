from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import PatientForm
from .models import Patient
from .services import generate_health_remarks

def patient_list(request):
    query = request.GET.get("q", "").strip()
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(full_name__icontains=query) | patients.filter(email__icontains=query)
    return render(request, "patients/patient_list.html", {
        "patients": patients.distinct(),
        "query": query,
        "total_count": Patient.objects.count(),
    })



def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.remarks = generate_health_remarks(patient)
            patient.save()
            messages.success(request, f"Record for {patient.full_name} was saved.")
            return redirect("patient_list")
        messages.error(request, "Please correct the validation errors below.")
    else:
        form = PatientForm()
    return render(request, "patients/patient_form.html", {
        "form": form, "page_title": "Add patient", "submit_label": "Save patient"
    })



def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.remarks = generate_health_remarks(patient)
            patient.save()
            messages.success(request, f"Record for {patient.full_name} was updated.")
            return redirect("patient_list")
        messages.error(request, "Please correct the validation errors below.")
    else:
        initial = {"date_of_birth": patient.date_of_birth.strftime("%d.%m.%Y")}
        form = PatientForm(instance=patient, initial=initial)
    return render(request, "patients/patient_form.html", {
        "form": form, "page_title": "Edit patient", "submit_label": "Update patient"
    })



@require_POST
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    name = patient.full_name
    patient.delete()
    messages.success(request, f"Record for {name} was deleted.")
    return redirect("patient_list")
