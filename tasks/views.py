from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render

from tasks.forms import TaskModelForm
from tasks.models import Task


# Create your views here.
def manager_dashboard(request):
    tasks = Task.objects.prefetch_related("assigned_to").select_related("details").all()

    count = Task.objects.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="PENDING")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
        completed=Count("id", filter=Q(status="COMPLETED")),
    )
    return render(
        request,
        "manager-dashboard.html",
        {"tasks": tasks, "count": count},
    )


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
