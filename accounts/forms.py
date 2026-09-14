from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


ROLE_CHOICES = (
    ("ALUMNI", "Alumni"),
    ("STUDENT", "Student"),
)

DEPARTMENT_CHOICES = (
    ("BSC_CS", "B.Sc. Computer Science"),
    ("BSC_AI", "B.Sc. Artificial Intelligence"),
    ("BCA", "B.C.A"),
    ("BCOM", "B.Com"),
    ("BCOM_CA", "B.Com. Computer Applications"),
    ("BA_ENGLISH", "B.A. English"),
    ("BA_TAMIL", "B.A. Tamil"),
    ("BBA", "B.B.A"),
    ("BSC_MATHS", "B.Sc. Mathematics"),
    ("BSC_PHYSICS", "B.Sc. Physics"),
    ("BSC_CHEMISTRY", "B.Sc. Chemistry"),
    ("BSC_BIOLOGY", "B.Sc. Biology"),
    ("BSC_BOTANY", "B.Sc. Botany"),
    ("BSC_ZOOLOGY", "B.Sc. Zoology"),
    ("OTHER", "Other"),
)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Name", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}))
    last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Account Type", widget=forms.Select(attrs={"class": "form-select", "id": "id_role"}))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=True, label="Department", widget=forms.Select(attrs={"class": "form-select"}))
    current_job = forms.CharField(required=False, label="Current Job", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Software Developer", "id": "id_current_job"}))
    phone = forms.CharField(required=True, label="Phone Number", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}))

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "role", "department",
            "graduation_year", "current_job", "phone", "profile_picture", "bio", "skills",
            "linkedin", "github", "portfolio", "password1", "password2",
        )
        widgets = {
            "graduation_year": forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 2026", "min": "1900", "max": "2100"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
        }

    password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}))
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}))


    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        current_job = (cleaned.get("current_job") or "").strip()
        if role == "ALUMNI" and not current_job:
            self.add_error("current_job", "Current Job is required for Alumni.")
        elif role == "STUDENT":
            cleaned["current_job"] = ""
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # Username is kept internally for Django authentication; users register with email instead.
        if not user.username:
            base = (user.email.split("@")[0] if user.email else "user").strip() or "user"
            username = base
            counter = 1
            while User.objects.filter(username=username).exclude(pk=user.pk).exists():
                username = f"{base}{counter}"
                counter += 1
            user.username = username
        if commit:
            user.save()
        return user


class AdminUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}), required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}), required=False)

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "role", "department",
            "graduation_year", "current_job", "phone", "profile_picture", "bio", "skills",
            "linkedin", "github", "portfolio", "is_active",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(choices=(("ADMIN", "Admin"),) + ROLE_CHOICES, attrs={"class": "form-select"}),
            "department": forms.Select(choices=DEPARTMENT_CHOICES, attrs={"class": "form-select"}),
            "graduation_year": forms.NumberInput(attrs={"class": "form-control", "min": "1900", "max": "2100"}),
            "current_job": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 or p2:
            if p1 != p2:
                self.add_error("password2", "Passwords do not match.")
            elif len(p1) < 8:
                self.add_error("password1", "Password must contain at least 8 characters.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password1"):
            user.set_password(self.cleaned_data["password1"])
        if user.role == "ADMIN":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "phone", "graduation_year", "current_job",
            "profile_picture", "bio", "skills", "linkedin", "github", "portfolio",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "graduation_year": forms.NumberInput(attrs={"class": "form-control", "min": "1900", "max": "2100"}),
            "current_job": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Software Developer"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
        }
