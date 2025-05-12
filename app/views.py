from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Khabar, Comment, Notification
from .forms import KhabarForm, SignUpForm, ProfilePicForm, CommentForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.http import JsonResponse
from .gemini_integration import configure_gemini, generate_content




def home(request):
    if request.user.is_authenticated:
        form = KhabarForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                khabar = form.save(commit=False)
                khabar.user = request.user
                khabar.save()
                #СДЕЛАТЬ ПЛАВНУЮ АНИМАЦИЮ СООБЩЕНИЯ
                messages.success(request, ("Your message has been sent"))
                return redirect('home')
        
        khabars = Khabar.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"khabars": khabars, "form": form})

    else:    
        khabars = Khabar.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"khabars": khabars})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude( user = request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("Please log in to view profiles"))
        return redirect('home')
    

def unfollow(request, pk):
    if request.user.is_authenticated:

        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')

def create_notification(sender, recipient, notification_type, khabar=None, comment=None):
    if sender != recipient: 
        Notification.objects.create(
            sender=sender,
            recipient=recipient,
            notification_type=notification_type,
            khabar=khabar,
            comment=comment
        )

def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        create_notification(request.user, profile.user, 'follow')
        messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        khabars = Khabar.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

            current_user_profile.save()
        return render(request, 'profile.html', {"profile":profile, "khabars": khabars})
    else:
        messages.success(request, ("Please log in to view profiles"))
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    return render(request, 'login.html', {})

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles":profiles})
        else:
            messages.success(request, ("That's Not Your Profile Page..."))
            return redirect('home')	
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')
	

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles":profiles})
        else:
            messages.success(request, ("That's Not Your Profile Page..."))
            return redirect('home')	
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, ("You are logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You are registered"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error registering"))
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required
def update_user(request):
    if request.method == "POST":
        current_user = request.user
        user_form = UpdateUserForm(request.POST, instance=current_user)
        profile_form = ProfilePicForm(request.POST, request.FILES, instance=current_user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile Has Been Updated!")
            return redirect('home')
    else:
        current_user = request.user
        user_form = UpdateUserForm(instance=current_user)
        profile_form = ProfilePicForm(instance=current_user.profile)
    
    return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})



def khabar_like(request, khabar_id):
    if request.user.is_authenticated:
        khabar = get_object_or_404(Khabar, id=khabar_id)
        if khabar.likes.filter(id=request.user.id):
            khabar.likes.remove(request.user)
        else:
            khabar.likes.add(request.user)
            create_notification(request.user, khabar.user, 'like', khabar=khabar)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')


def khabar_show(request, khabar_id):
    khabar = get_object_or_404(Khabar, id=khabar_id)
    comment_form = CommentForm()
    return render(request, 'show_khabar.html', {
        'khabar': khabar,
        'comment_form': comment_form
    })


def delete_khabar(request, khabar_id):
    if request.user.is_authenticated:
        khabar = get_object_or_404(Khabar, id=khabar_id)
        if request.user.username == khabar.user.username:

            khabar.delete()
            
            messages.success(request, ("THis khabar has been deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))	
        else:
            messages.success(request, ("you dont own that khabar!"))
            return redirect('profile', pk=request.user.id)

    else:
        messages.success(request, ("Please Log In To Continue..."))
        return redirect(request.META.get("HTTP_REFERER"))


def edit_khabar(request, khabar_id):
    if request.user.is_authenticated:
        khabar = get_object_or_404(Khabar, id=khabar_id)
        if request.user.username == khabar.user.username:
            form = KhabarForm(request.POST or None, instance=khabar)
            if request.method == "POST":
                if form.is_valid():
                    khabar = form.save(commit=False)
                    khabar.user = request.user
                    khabar.save()
                    messages.success(request, ("Your khabar Has Been Updated!"))
                    return redirect('profile', pk=request.user.id)
            else:
                return render(request, "edit_khabar.html", {'form':form, 'khabar':khabar})
        else:
            messages.success(request, ("You Don't Own That khabar!!"))
            return redirect('home')
    else:
        messages.success(request, ("Please Log In To Continue..."))
        return redirect('home')



def search(request):
    if request.method == "POST":

        search = request.POST['search']
        searched = Khabar.objects.filter(body__contains = search)

        return render(request, 'search.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search.html', {})

@login_required
def add_comment(request, khabar_id):
    khabar = get_object_or_404(Khabar, id=khabar_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.khabar = khabar
            comment.user = request.user
            comment.save()
            create_notification(request.user, khabar.user, 'comment', khabar=khabar, comment=comment)
            return redirect('khabar_show', khabar_id=khabar_id)
    return redirect('khabar_show', khabar_id=khabar_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        khabar_id = comment.khabar.id
        comment.delete()
        return redirect('khabar_show', khabar_id=khabar_id)
    return redirect('home')

@login_required
def generate_ai_content(request):
    if request.method == 'POST':
        prompt = request.POST.get('Whats on your mind? write no more than 30 words', 'Write an interesting post to my social network, no more than 30 words')
        if prompt:
            configure_gemini()
            generated_text = generate_content(prompt)
            return JsonResponse({'content': generated_text})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def notifications(request):
    notifications = request.user.notifications.all()[:10]  # Get last 10 notifications
    unread_count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({
        'notifications': [
            {
                'id': n.id,
                'message': str(n),
                'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_read': n.is_read,
                'type': n.notification_type,
                'khabar_id': n.khabar.id if n.khabar else None,
            } for n in notifications
        ],
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})
