from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

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

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=True,
        label="Department",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "department",
            "graduation_year",
            "current_job",
            "phone",
            "profile_picture",
            "bio",
            "skills",
            "linkedin",
            "github",
            "portfolio",
            "password1",
            "password2",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "role": forms.Select(
                attrs={"class": "form-select"}
            ),

            "graduation_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 2026",
                    "min": "1900",
                    "max": "2100",
                }
            ),

            "current_job": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Software Developer",
                }
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "skills": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "linkedin": forms.URLInput(
                attrs={"class": "form-control"}
            ),

            "github": forms.URLInput(
                attrs={"class": "form-control"}
            ),

            "portfolio": forms.URLInput(
                attrs={"class": "form-control"}
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "graduation_year",
            "current_job",
            "profile_picture",
            "bio",
            "skills",
            "linkedin",
            "github",
            "portfolio",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "graduation_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1900",
                    "max": "2100",
                }
            ),

            "current_job": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Software Developer",
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "skills": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "linkedin": forms.URLInput(
                attrs={"class": "form-control"}
            ),

            "github": forms.URLInput(
                attrs={"class": "form-control"}
            ),

            "portfolio": forms.URLInput(
                attrs={"class": "form-control"}
            ),
        }