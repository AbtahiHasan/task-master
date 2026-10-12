from decouple import config
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{config('FRONTEND_URL')}/activate/{instance.id}/{token}/"
        subject = "Activate your account"
        message = f"Click the following link to activate your account: {activation_url}"

        try:
            send_mail(subject, message, config("EMAIL_HOST_USER"), [instance.email])
        except Exception as e:
            print(f"Failed to send activation email: {e}")
