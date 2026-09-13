from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from tasks.views import create_task, manager_dashboard, user_dashboard

urlpatterns = [
    path("manager-dashboard/", manager_dashboard),
    path("user-dashboard/", user_dashboard),
    path("create-task/", create_task),
] + debug_toolbar_urls()
