from datetime import time
from django.db import models

# Create your models here.

class AddDepartment(models.Model):
    Department = models.CharField(max_length=255)

    def __str__(self):
        template = '{0.Department}'
        return template.format(self)



class Doctors(models.Model):
    doc_name = models.CharField(max_length=75)
    doc_post = models.CharField(max_length=255)
    doc_timming = models.CharField(max_length=19)
    doc_ranking = models.FloatField(max_length=3)
    doc_department = models.ForeignKey(AddDepartment, on_delete=models.CASCADE)
    doc_room = models.IntegerField()
    doc_specialization = models.CharField(max_length=100)
    phone_number = models.PositiveIntegerField()
    doc_email_address = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        template = '{0.doc_name} , {0.doc_specialization}'
        return template.format(self)


class MakeAppointment(models.Model):
    Your_Name = models.CharField(max_length=80)
    Age = models.CharField(max_length=2)
    Disease = models.CharField(max_length=50)
    description = models.CharField(max_length=800)
    email_address = models.EmailField()
    Doctor = models.ForeignKey(Doctors , on_delete=models.CASCADE)
    created = models.DateTimeField()

    def __str__(self):
        template = '{0.Your_Name} , {0.Disease}'
        return template.format(self)

class PatientRecord(models.Model):
    patient_name = models.CharField(max_length=50)
    problem = models.CharField(max_length=20)
    time = models.DurationField(max_length=11)
    doctor = models.ForeignKey(Doctors  , on_delete=models.CASCADE)
    def __str__(self):
            template = '{0.patient_name} , {0.problem}'
            return template.format(self)

class Login(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=12)

    def __str__(self):
        template = '{0.email}'
        return template.format(self)


class Signup(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state = models.CharField(max_length = 20)
    city = models.CharField(max_length = 25)
    Address = models.CharField(max_length = 500)
    email_address = models.EmailField()
    password = models.CharField(max_length=50)
    phone_number = models.PositiveIntegerField()

    def __str__(self):
        template = '{0.first_name} , {0.email_address}'
        return template.format(self)


class Review(models.Model):
    doc = models.ForeignKey(Doctors  , on_delete=models.CASCADE)
    patient = models.ForeignKey(Signup  , on_delete=models.CASCADE)
    appoint = models.ForeignKey(MakeAppointment, on_delete=models.CASCADE)
    review_write = models.CharField(max_length=500)
    review_star = models.FloatField()


    def __str__(self):
        template = ' {0.doc.doc_name} | {0.patient.first_name} | {0.review_star} '
        return template.format(self)    


class ChatsRecord(models.Model):
    userid = models.ForeignKey(Signup  , on_delete=models.CASCADE)
    usermsg = models.CharField(max_length=1000)
    botmsg = models.CharField(max_length=500)
    
     