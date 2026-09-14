from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User
from jobs.models import Job, JobApplication
from mentorship.models import MentorshipRequest
from notifications.models import Notification


@login_required
def dashboard(request):
    user = request.user
    role = str(getattr(user, "role", "")).upper()

    context = {
        "alumni_count": User.objects.filter(role="ALUMNI").count(),
        "student_count": User.objects.filter(role="STUDENT").count(),
        "job_count": Job.objects.count(),
        "unread_count": Notification.objects.filter(
            user=user, is_read=False
        ).count(),
        "role": role,
        "recent_jobs": Job.objects.select_related("posted_by")[:5],
    }

    if role == "STUDENT":
        context["my_applications_count"] = JobApplication.objects.filter(
            student=user
        ).count()
        context["my_mentorship_count"] = MentorshipRequest.objects.filter(
            student=user
        ).count()
    elif role == "ALUMNI":
        context["my_jobs_count"] = Job.objects.filter(posted_by=user).count()
        context["pending_applications_count"] = JobApplication.objects.filter(
            job__posted_by=user, status="APPLIED"
        ).count()
        context["mentorship_requests_count"] = MentorshipRequest.objects.filter(
            alumni=user, status="Pending"
        ).count()

    return render(request, "dashboard/dashboard.html", context)


@login_required
def admin_dashboard(request):
    return dashboard(request)
