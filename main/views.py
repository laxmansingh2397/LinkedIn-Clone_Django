from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Post, Experience, Connection, Notification, Like
from .models import Share
from .forms import PostForm, ExperienceForm
from .forms import ProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.
def default(request):
    return render(request, 'default_page/index.html')


def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=login_input)
            username = user_obj.username
        except ObjectDoesNotExist:
            username = login_input

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid credentials')

    return render(request, 'login_page/login.html')


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        if not username:
            if email:
                username = email.split('@')[0]
            else:
                return f"user_{User.objects.count()+1}"

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists')
            return render(request, 'signup_page/signup.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
    return render(request, 'signup_page/signup.html')

@login_required
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Posted successfully")
            return redirect("home")
        else:
            print("PostForm error:", form.errors)
            messages.error(request, "Could not create post. Check server console for form errors.")
    else:
        form = PostForm()

    posts = Post.objects.all().order_by("-created_at")
    # compute which posts the current user has liked to render UI state
    liked_post_ids = set(Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True))
    experiences = Experience.objects.filter(user=request.user).order_by("-start_date")
    experience_form = ExperienceForm()

    # build connection helpers for templates
    connections = Connection.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
    accepted_ids = set()
    pending_sent_ids = set()
    pending_received_map = {}  # from_user_id -> connection_id
    pending_received_ids = set()

    for connection in connections:
        if connection.status == 'accepted':
            other = connection.to_user if connection.from_user == request.user else connection.from_user
            accepted_ids.add(other.id)
        elif connection.status == 'pending':
            if connection.from_user == request.user:
                pending_sent_ids.add(connection.to_user.id)
            else:
                pending_received_map[connection.from_user.id] = connection.id
                pending_received_ids.add(connection.from_user.id)

    # notifications for header
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:6]

    connection_count = len(accepted_ids)
    # list of user objects for accepted connections (useful for share dropdown)
    user = get_user_model()
    connection_users = user.objects.filter(id__in=accepted_ids)

    return render(request, 'home_page/home_page.html', {"posts": posts, "form": form, "experience_form": experience_form,  "experiences": experiences, 'accepted_ids': accepted_ids, 'pending_sent_ids': pending_sent_ids, 'pending_received_map': pending_received_map, 'pending_received_ids': pending_received_ids, 'unread_notif_count': unread_count, 'recent_notifications': recent_notifications, 'connection_count': connection_count, 'liked_post_ids': liked_post_ids, 'connection_users': connection_users})


@login_required
def add_experience(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, "Experience added successfully")
        else:
            messages.error(request, "Failed to add experience")
            print(form.errors)
    
    return redirect("home")


@login_required
def send_connection(request, to_user_id):
    
    User = get_user_model()
    try:
        to_user = User.objects.get(pk=to_user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('home')

    # prevent duplicate or self connection
    if to_user == request.user:
        messages.error(request, "You cannot connect to yourself")
        return redirect('home')

    if Connection.objects.filter(from_user=request.user, to_user=to_user).exists() or Connection.objects.filter(from_user=to_user, to_user=request.user).exists():
        messages.info(request, "Connection already exists or pending")
        return redirect('home')

    Connection.objects.create(from_user=request.user, to_user=to_user, status='pending')
    # create notification for recipient
    Notification.objects.create(user=to_user, from_user=request.user, notif_type='connection_request', message=f"{request.user.username} sent you a connection request")
    messages.success(request, "Connection request sent")
    return redirect('home')


@login_required
def accept_connection(request, connection_id):
    try:
        connection = Connection.objects.get(pk=connection_id, to_user=request.user, status='pending')
    except Connection.DoesNotExist:
        messages.error(request, "Connection request not found")
        return redirect('connections')

    connection.status = 'accepted'
    connection.save()
    # notify the requester
    Notification.objects.create(user=connection.from_user, from_user=request.user, notif_type='connection_accepted', message=f"{request.user.username} accepted your connection request")
    messages.success(request, "Connection accepted")
    return redirect('connections')


@login_required
def reject_connection(request, connection_id):
    try:
        connection = Connection.objects.get(pk=connection_id, to_user=request.user, status='pending')
    except Connection.DoesNotExist:
        messages.error(request, "Connection request not found")
        return redirect('connections')

    connection.status = 'rejected'
    connection.save()
    messages.success(request, "Connection rejected")
    return redirect('connections')


@login_required
def withdraw_connection(request, connection_id):
    try:
        connection = Connection.objects.get(pk=connection_id, from_user=request.user)
    except Connection.DoesNotExist:
        messages.error(request, "Connection not found")
        return redirect('home')

    connection.delete()
    messages.success(request, "Connection withdrawn")
    return redirect('home')


@login_required
def my_connections(request):
    sent = Connection.objects.filter(from_user=request.user).order_by('-created_at')
    received = Connection.objects.filter(to_user=request.user, status='pending').order_by('-created_at')
    accepted = Connection.objects.filter((Q(from_user=request.user) | Q(to_user=request.user)), status='accepted')
    # mark related notifications as read when visiting connections
    Notification.objects.filter(user=request.user, notif_type='connection_request', is_read=False).update(is_read=True)
    # connection count for sidebar
    connection_count = accepted.count()
    # include notification context for header
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:6]
    return render(request, 'connections/connections.html', {'sent': sent, 'received': received, 'accepted': accepted, 'connection_count': connection_count, 'unread_notif_count': unread_count, 'recent_notifications': recent_notifications})


@login_required
def mark_notification(request, notif_id):
    try:
        notification = Notification.objects.get(pk=notif_id, user=request.user)
        notification.is_read = True
        notification.save()
    except Notification.DoesNotExist:
        # silently ignore if not found or not permitted
        notification = None

    # if this notification refers to a post like, redirect user to the post on home feed
    if notification and notification.notif_type in ('post_like','post_shared'):
        import re
        message = re.search(r'id:(\d+)', notification.message or '')
        if message:
            post_id = message.group(1)
            return redirect(f"/profile/#post-{post_id}")

    return redirect('connections')


@login_required
def accept_connection_from(request, from_user_id):
    try:
        conn = Connection.objects.get(from_user__id=from_user_id, to_user=request.user, status='pending')
    except Connection.DoesNotExist:
        messages.error(request, "Connection request not found")
        return redirect('home')

    conn.status = 'accepted'
    conn.save()
    Notification.objects.create(user=conn.from_user, from_user=request.user, notif_type='connection_accepted', message=f"{request.user.username} accepted your connection request")
    messages.success(request, "Connection accepted")
    return redirect('home')


@login_required
def reject_connection_from(request, from_user_id):
    try:
        connection = Connection.objects.get(from_user__id=from_user_id, to_user=request.user, status='pending')
    except Connection.DoesNotExist:
        messages.error(request, "Connection request not found")
        return redirect('home')

    connection.status = 'rejected'
    connection.save()
    messages.success(request, "Connection rejected")
    return redirect('home')


@login_required
def withdraw_connection_to(request, to_user_id):
    try:
        connection = Connection.objects.get(from_user=request.user, to_user__id=to_user_id, status='pending')
    except Connection.DoesNotExist:
        messages.error(request, "Connection not found")
        return redirect('home')

    connection.delete()
    messages.success(request, "Connection withdrawn")
    return redirect('home')


@login_required
def profile(request):
    # show current user's profile page (for 'me')
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    experiences = Experience.objects.filter(user=user).order_by('-start_date')

    # connection counts
    conns = Connection.objects.filter(Q(from_user=user) | Q(to_user=user), status='accepted')
    connection_count = conns.count()

    # notifications for header
    unread_count = Notification.objects.filter(user=user, is_read=False).count()
    recent_notifications = Notification.objects.filter(user=user).order_by('-created_at')[:6]

    # determine which posts the current user has liked
    liked_post_ids = set(Like.objects.filter(user=user, post__in=posts).values_list('post_id', flat=True))

    # build list of accepted connection users for share dropdown
    accepted_ids = set()
    conns_all = Connection.objects.filter(Q(from_user=user) | Q(to_user=user))
    for c in conns_all:
        if c.status == 'accepted':
            other = c.to_user if c.from_user == user else c.from_user
            accepted_ids.add(other.id)
    user_model = get_user_model()
    connection_users = user_model.objects.filter(id__in=accepted_ids)

    return render(request, 'profile/profile.html', {'user_profile': user, 'posts': posts, 'experiences': experiences, 'connection_count': connection_count, 'unread_notif_count': unread_count, 'recent_notifications': recent_notifications, 'liked_post_ids': liked_post_ids, 'connection_users': connection_users})


@login_required
def edit_profile(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # populate first/last name from POST
        form.data = form.data.copy()
        form.data['first_name'] = request.POST.get('first_name','')
        form.data['last_name'] = request.POST.get('last_name','')
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
        else:
            messages.error(request, 'Could not save profile')
    else:
        initial = {'first_name': user.first_name, 'last_name': user.last_name}
        form = ProfileForm(instance=profile, initial=initial)

    return render(request, 'profile/edit_profile.html', {'form': form})


@login_required
@require_POST
def toggle_post_like(request):
    post_id = request.POST.get('post_id')
    if not post_id:
        return JsonResponse({'error': 'post_id required'}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'post not found'}, status=404)

    existing = Like.objects.filter(user=request.user, post=post).first()
    if existing:
        existing.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
        # notify post owner about the like (if not self)
        if post.user != request.user:
            Notification.objects.create(user=post.user, from_user=request.user, notif_type='post_like', message=f"{request.user.username} liked your post (id:{post.id})")

    count = post.likes.count()
    return JsonResponse({'ok': True, 'liked': liked, 'count': count})


@login_required
@require_POST
def share_post(request):
    post_id = request.POST.get('post_id')
    to_user_id = request.POST.get('to_user_id')
    message = request.POST.get('message', '')
    if not post_id or not to_user_id:
        return JsonResponse({'error': 'post_id and to_user_id required'}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'post not found'}, status=404)
    User = get_user_model()
    try:
        to_user = User.objects.get(pk=to_user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'target user not found'}, status=404)

    # create share record
    Share.objects.create(user=request.user, post=post, to_user=to_user, message=message)

    # notify the recipient
    if to_user != request.user:
        Notification.objects.create(user=to_user, from_user=request.user, notif_type='post_shared', message=f"{request.user.username} shared a post (id:{post.id})")

    return JsonResponse({'ok': True})