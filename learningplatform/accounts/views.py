from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def register_new_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        # Basic validation
        if not (username and email and password and confirm_password):
            return render(request, 'registration.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

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

    return render(request, 'registration.html')
