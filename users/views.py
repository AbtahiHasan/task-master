from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from users.forms import LoginForm, RegistrationForm


# Create your views here.
def sign_up(request):
    form = RegistrationForm()
    if request.method == "GET":
        pass
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.is_active = True
            user.save()
            messages.success(
                request, "A confirmation email has been sent to your email address."
            )
            return redirect("sign-in")

    return render(request, "registeration/sign-up.html", {"form": form})
def sign_in(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save()
            username = form.cleaned_data.get("username")
            password = form.changed_data.get("password1")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

    return render(request, "login.html", {"form": form})
