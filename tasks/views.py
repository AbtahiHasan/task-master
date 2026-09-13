from django.shortcuts import render


# Create your views here.
def manager_dashboard(request):
    return render(request, "manager-dashboard.html")


def user_dashboard(request):
    return render(request, "user-dashboard.html")
