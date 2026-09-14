from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, UserUpdateForm
from .google_sheets import send_registration_to_google_sheet


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            # Store the non-sensitive registration details in Google Sheets.
            # Passwords are never sent to Google Sheets.
            sheet_ok, sheet_message = send_registration_to_google_sheet(user)

            login(request, user)

            if sheet_ok:
                messages.success(
                    request,
                    "Registration successful. Your registration details were stored successfully."
                )
            else:
                # Do not block account creation if the external sheet is temporarily unavailable.
                messages.warning(
                    request,
                    "Registration successful, but Google Sheets could not be updated right now."
                )
                print(f"Google Sheets registration error: {sheet_message}")

            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile(request):
    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user,
        },
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )

@login_required
def settings_view(request):
    """Account settings page for updating the signed-in user's profile."""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect("settings")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "accounts/settings.html", {"form": form})
