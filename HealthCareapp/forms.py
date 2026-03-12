from django import forms
from .models import *


class AddDepartmentForm(forms.ModelForm):
    Department = forms.CharField(required=True)
    class Meta:
        model = AddDepartment
        fields = '__all__'


class AddDoctorsForm(forms.ModelForm):
    doc_name = forms.CharField(required=True)
    doc_post = forms.CharField(required=True)
    doc_specialization = forms.CharField(required=True)
    doc_timming = forms.CharField(required=True)
    doc_room = forms.IntegerField()
    doc_email_address = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = Doctors
        fields = "__all__"


class MakeAppointmentForm(forms.ModelForm):
    Your_Name = forms.CharField(required=True)
    Age = forms.CharField(required=True)
    Disease = forms.CharField(required=True)
    # Description = forms.CharField(required=True)
    Doctor = models.ForeignKey(Doctors , on_delete=models.CASCADE)

    class Meta:
        model = MakeAppointment
        fields = "__all__"


class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = Login
        fields = '__all__'


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    state = forms.CharField(required = True)
    city = forms.CharField(required = True)
    Address = forms.CharField(required = True)
    email_address = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)


    class Meta:
        model = Signup
        fields = '__all__'
