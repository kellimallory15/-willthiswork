from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from bookings.models import Client


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            ...
            messages.success(request, "An Error Occurred Validating Your Credentials. Please Try Again!")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You've Successfully Been Signed Out!")
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # This saves the User object and returns it
            # Now create a Client profile
            client = Client.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )
            # Authenticate and login the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Sign-up Successful!")
                return redirect('index')
            else:
                messages.success(request, "Authentication failed. Please try again.")
                return render(request, 'authenticate/register_user.html', {'form': form})
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })
