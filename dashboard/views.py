from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import admin_required
from accounts.forms import AdminUserForm
from accounts.models import User
from jobs.models import Job, JobApplication
from mentorship.models import MentorshipRequest
from notifications.models import Notification
from forum.models import Post


@login_required
def dashboard(request):
    user = request.user
    role = str(getattr(user, "role", "")).upper()
    context = {
        "alumni_count": User.objects.filter(role="ALUMNI").count(),
        "student_count": User.objects.filter(role="STUDENT").count(),
        "job_count": Job.objects.count(),
        "unread_count": Notification.objects.filter(user=user, is_read=False).count(),
        "role": role,
        "recent_jobs": Job.objects.select_related("posted_by")[:5],
    }
    if role == "STUDENT":
        context["my_applications_count"] = JobApplication.objects.filter(student=user).count()
        context["my_mentorship_count"] = MentorshipRequest.objects.filter(student=user).count()
    elif role == "ALUMNI":
        context["my_jobs_count"] = Job.objects.filter(posted_by=user).count()
        context["pending_applications_count"] = JobApplication.objects.filter(job__posted_by=user, status="APPLIED").count()
        context["mentorship_requests_count"] = MentorshipRequest.objects.filter(alumni=user, status="Pending").count()
    return render(request, "dashboard/dashboard.html", context)


@admin_required
def admin_dashboard(request):
    users = User.objects.all().order_by("-date_joined")
    search = request.GET.get("search", "").strip()
    if search:
        users = users.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search))
    context = {
        "users": users,
        "total_users": User.objects.count(),
        "total_alumni": User.objects.filter(role="ALUMNI").count(),
        "total_students": User.objects.filter(role="STUDENT").count(),
        "total_admins": User.objects.filter(role="ADMIN").count(),
        "total_jobs": Job.objects.count(),
        "total_mentorships": MentorshipRequest.objects.count(),
        "total_forum_posts": Post.objects.count(),
        "search": search,
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@admin_required
def admin_user_add(request):
    if request.method == "POST":
        form = AdminUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("admin_dashboard")
    else:
        form = AdminUserForm(initial={"role": "STUDENT", "is_active": True})
    return render(request, "dashboard/admin_user_form.html", {"form": form, "title": "Add User"})


@admin_required
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = AdminUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username} updated successfully.")
            return redirect("admin_dashboard")
    else:
        form = AdminUserForm(instance=user)
    return render(request, "dashboard/admin_user_form.html", {"form": form, "title": f"Edit {user.username}", "editing": True})


@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.pk == request.user.pk:
        messages.error(request, "You cannot delete your own administrator account.")
        return redirect("admin_dashboard")
    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"{username} deleted successfully.")
    return redirect("admin_dashboard")
