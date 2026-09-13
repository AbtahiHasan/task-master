from django.shortcuts import render

from tasks.forms import TaskForm
from tasks.models import Employee


# Create your views here.
def manager_dashboard(request):
    return render(request, "manager-dashboard.html")


def user_dashboard(request):
    return render(request, "user-dashboard.html")


def create_task(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees)
    context = {"form": form}
    if request.method == "POST":
        form = TaskForm(request.POST, employees=employees)
        if form.is_valid():
            print(form.cleaned_data)
    return render(request, "create-task.html", context)
