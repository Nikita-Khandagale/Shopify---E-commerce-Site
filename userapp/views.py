from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm


# ---------------------------------------------------------
# VIEW USER PROFILE
# ---------------------------------------------------------
@login_required
def view_profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'userapp/view-profile.html', {
        'profile': profile
    })


# ---------------------------------------------------------
# EDIT USER PROFILE
# ---------------------------------------------------------
@login_required
def edit_profile(request):
    user = request.user

    # Get or create profile for the user
    profile, created = UserProfile.objects.get_or_create(user=user)

    # If form is submitted
    if request.method == 'POST':
        # Bind user form and profile form
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        # Validate both forms
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('userapp:view-profile')

    else:
        # Pre-fill forms with existing data
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'userapp/edit-profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# ---------------------------------------------------------
# DELETE USER PROFILE
# ---------------------------------------------------------
@login_required
def delete_profile(request):
    user = request.user

    # If user confirms deletion
    if request.method == 'POST':
        user.delete()  # This deletes user + auto deletes linked profile
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('ShopifyApp:home')  # Redirect to home

    return render(request, 'userapp/delete-profile.html', {
        'user': user
    })


# ---------------------------------------------------------
# REGISTER NEW USER (BUYER / SELLER)
# ---------------------------------------------------------
def register(request, role):
    # If form submitted
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Assign role to user
            if role == 'seller':
                user.is_seller = True
            elif role == 'buyer':
                user.is_buyer = True

            user.save()

            messages.success(request, f"{role.upper()} account created successfully!")
            return redirect('userapp:login')

    else:
        # Display empty registration form
        form = CustomUserCreationForm()

    return render(request, 'userapp/register.html', {
        'form': form,
        'role': role
    })
