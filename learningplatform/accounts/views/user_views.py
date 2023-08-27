from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import random
import string


#code here mainly concerns the user class

def register_new_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        # Basic validation
        if not (username and email and password and confirm_password):
            return render(request, 'registration.html', {'error': 'All fields are required'}) # Replace 'xyz.html' with corresponding react component

        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'}) # Replace 'xyz.html' with corresponding react component

        # Hash the password
        hashed_password = make_password(password)

        # Create a new user
        new_user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password,
        )
        new_user.phone_number = phone_number
        new_user.save()

        # Send verification email
        verification_token = 'generate_your_verification_token_here'
        subject = 'Verify Your Email'
        message = f'Click the link to verify your email: {settings.BASE_URL}/verify-email/{verification_token}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('registration_success')  # Redirect to a success page

    return render(request, 'registration.html') # Replace 'xyz.html' with corresponding react component

def verify_user_email(request, verification_token):
    user = get_object_or_404(User, verification_token=verification_token)
    
    if user.is_verified:
        return render(request, 'verification_error.html', {'error_message': 'Email already verified'}) # Replace 'xyz.html' with corresponding react component
    
    # Mark user as verified
    user.is_verified = True
    user.save()

    return render(request, 'verification_success.html') # Replace 'xyz.html' with corresponding react component

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')  # Replace 'login.html' with corresponding react component

def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def forgotten_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)

        new_password = generate_random_password()
        user.set_password(new_password)
        user.save()

        subject = 'New Password'
        message = f'Your new password is: {new_password}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, 'A new password has been sent to your email')

        return redirect('login_user')  # Redirect to the login page

    return render(request, 'forgotten_password.html')  # Replace 'forgotten_password.html' with your template

#CRUD operations on the user profile

def view_user_profile(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }

    return render(request, 'user_profile.html', context)  # Replace 'user_profile.html' with your template

@login_required
def edit_user_profile(request):
    user = request.user

    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')

        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email

        user.save()
        messages.success(request, 'Profile updated successfully')

    return render(request, 'edit_user_profile.html', {'user': user})  # Replace 'edit_user_profile.html' with your template

@login_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect')
        elif new_password != confirm_new_password:
            messages.error(request, 'Passwords do not match')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully')

    return render(request, 'change_password.html')  # Replace 'change_password.html' with your template