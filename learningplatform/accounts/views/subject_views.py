from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import UserProfile

def get_all_subjects(request):
    subjects = [
        'Biology', 'Chemistry', 'Physics', 'Law', 'Engineering', 'Computer Science',
        'Mathematics', 'English', 'Geography', 'Religious Studies', 'Design and Technology',
        'Art', 'Home Economics', 'Textiles', 'Business Studies', 'Economics',
        'Psychology', 'Sociology', 'Foreign Languages'
    ]
    # Add more subjects as needed

    return render(request, 'all_subjects.html', {'subjects': subjects})

@login_required
def select_subjects(request):
    user = request.user

    if request.method == 'POST':
        selected_subjects = request.POST.getlist('selected_subjects')
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.subjects.set(selected_subjects)  # Set the selected subjects
        user_profile.save()

        return redirect('profile')  # Redirect to the user's profile

    # Get the user's currently selected subjects
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    selected_subjects = user_profile.subjects.all()

    all_subjects = [
        'Biology', 'Chemistry', 'Physics', 'Law', 'Engineering', 'Computer Science',
        'Mathematics', 'English', 'Geography', 'Religious Studies', 'Design and Technology',
        'Art', 'Home Economics', 'Textiles', 'Business Studies', 'Economics',
        'Psychology', 'Sociology', 'Foreign Languages'
    ]
    # Add more subjects as needed

    return render(request, 'select_subjects.html', {'selected_subjects': selected_subjects, 'all_subjects': all_subjects})

@login_required
def update_selected_subjects(request):
    user = request.user

    if request.method == 'POST':
        selected_subjects = request.POST.getlist('selected_subjects')
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.subjects.set(selected_subjects)  # Set the selected subjects
        user_profile.save()

        return redirect('profile')  # Redirect to the user's profile

    return redirect('profile')  # Redirect to the user's profile if the request method is not POST