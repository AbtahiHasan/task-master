from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from tasks.models import Task


@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_task_creating(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        print("checking", assigned_emails)
        send_mail(
            "Tasks assigned",
            f"Task {instance.title} has been assigned to you.",
            "abathihasananik@gmail.com",
            assigned_emails,
        )
