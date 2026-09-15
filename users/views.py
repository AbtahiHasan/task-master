from django.shortcuts import render

from users.forms import RegistrationForm


# Create your views here.
def sign_up(request):
    form = RegistrationForm()
    if request.method == "GET":
        pass
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, "registeration/sign-up.html", {"form": form})
