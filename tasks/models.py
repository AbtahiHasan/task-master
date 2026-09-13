from django.db import models

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ManyToManyField(Employee, related_name="assigned_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskDetail(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"

    PRIORITY_OPTIONS = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="details")
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
