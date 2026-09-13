from django.http import HttpResponse
from django.shortcuts import render

from tasks.forms import TaskModelForm


# Create your views here.
def manager_dashboard(request):
    return render(request, "manager-dashboard.html")


def user_dashboard(request):
    return render(request, "user-dashboard.html")


def create_task(request):

    form = TaskModelForm()
    context = {"form": form}
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("Task created successfully!")
    return render(request, "create-task.html", context)
