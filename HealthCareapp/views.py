from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from .models import *
from django.db import models
import re
import smtplib, ssl
import random
import math
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from datetime import datetime 
from django.http import JsonResponse
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("API_KEY")



def home_page(request):
    return render(request, 'home.html')

def signup_page(request):
        # Check if the request method is POST
        if request.POST:
            # Regular expression to validate email
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'
            # Get form values
            fname = request.POST['fname']
            lname = request.POST['lname']
            pnumber = request.POST['pnumber']
            state = request.POST['state']
            city = request.POST['city']
            Address = request.POST['Address']
            # Save email in the session
            request.session['email'] = request.POST['eml']
            Password = request.POST['Password']
            Confirm_Password = request.POST['Confirm_Password']

            # Validate the first name
            if (fname == ""):
                # Error message for first name
                name = {"first_Name_error":"First Name Must be filled!"}
                # Render signup page with error message
                return render(request, "signup.html", name)

            # Validate the last name
            elif (lname == ""):
                # Error message for last name
                lname = {"last_Name_error":"Last Name Must be filled!"}
                # Render signup page with error message
                return render(request, "signup.html", lname)

            # Validate the phone number
            elif (len(pnumber) > 11 or len(pnumber) < 11):
                # Error message for phone number
                number = {"number_error":"Correct the phone number!"}
                # Render signup page with error message
                return render(request, "signup.html", number)

            # Validate the state
            elif (state == ""):
                # Error message for state
                state = {"state_error":"State Must be filled!"}  
                # Render signup page with error message
                return render(request, "signup.html", state)

            # Validate the city
            elif (city == "" ):
                # Error message for city
                city = {"city_error":"City Must be filled!"}
                # Render signup page with error message
                return render(request, "signup.html", city)

            # Validate the address
            elif (Address == "" ):
                # Error message for address
                address = {"address_error":"Address Must be filled!"}
                # Render signup page with error message
                return render(request, "signup.html", address)

            # Validate the email
            elif (request.session['email'] == "" or not re.fullmatch(regex, request.session['email'])):
                # Error message for email
                email_address = {"email_address_error":"Invalid Email Address"}
                # Render signup page with error message
                return render(request, "signup.html", email_address)

            # Check if the password is filled or is at least 8 characters
            elif (Password == "" or len(Password) < 8):
                password_error = {"password_error":"Password Must be filled or greater than 8 characters"}
                return render(request, "signup.html", password_error)

            # Check if the password confirmation matches the password
            elif (not Confirm_Password == Password):
                confirm_error = {"confirm_error":"Password must match"}
                return render(request, "signup.html", confirm_error)

            # Save the user data to the database
            else:
                obj = Signup(first_name=fname, last_name=lname,
                            phone_number=pnumber, state=state, city=city, Address=Address, email_address=request.session['email'], password=Password )
                count = Signup.objects.filter(
                    email_address=request.session['email']).count()
                # Check if the user already exists
                if count > 0:
                    username_error = {"username_error": "User already exists"}
                    return render(request, 'signup.html', username_error)
                # Save the user and redirect to the login page
                else:
                    obj.save()
                    return redirect('/home/login')

        return render(request, 'signup.html')

def login_page(request):
    # Check if the request method is POST
    if request.POST:
        # Store the email address in the session
        request.session['email'] = request.POST['email']
        # Store the password from the form
        Password = request.POST['password']
        
        # Check if there's a match of email and password in the Signup model
        count_patient = Signup.objects.filter(
            email_address=request.session['email'], password= Password).count()
        # Check if there's a match of email and password in the Doctors model
        count_doctor = Doctors.objects.filter(
            doc_email_address=request.session['email'], password=Password).count()
        # If there's a match in the Signup model
        if count_patient > 0:
            # Redirect the user to the patient home page
            return redirect("/home/patient/")
        # If there's a match in the Doctors model
        elif count_doctor > 0 :
            # Redirect the user to the doctor home page
            return redirect("/home/doctor/")
        elif (request.session['email'] == "admin123@healthcare.com" and Password == "adminisadmin"):
            return redirect("/admin")

        else:
            # If there's no match, render the login page with an error message
            return render(request, 'login.html', {"Details_Error": "Invalid Details"})

    # If the request method is not POST, render the login page
    return render(request, 'login.html')

def forget_page(request):
    # Check if the request method is POST
    if request.POST:
        # Store the email address from the form data in the session
        request.session['email'] = request.POST['email']

        # Count the number of patients with the specified email address
        count_patient = Signup.objects.filter(
                email_address= request.session['email']).count()
        # Count the number of doctors with the specified email address
        count_doctor = Doctors.objects.filter(
                doc_email_address= request.session['email']).count()
        # If no patients or doctors have the specified email address
        if count_patient < 1 or count_doctor < 0:
            # Provide error message to the user
            context = {"User_error":"User Not Found double check your email"}
            # Render the forget.html template with the error message
            return render(request,'forget.html', context)
        # If at least one patient or doctor has the specified email address
        elif count_patient  > 0 or count_doctor > 0 :
            # Provide success message to the user
            content = {"success":"Email Sent! Check your inbox or spam folder."}
            
            # Generate a random 6-digit string for the password reset code
            digits = [i for i in range(0, 10)]
            request.session['random_str'] = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                request.session['random_str'] += str(digits[index])
            
            # Email settings
            port = 587  # For starttls
            smtp_server = "smtp.gmail.com"
            sender_email = "grizzlyproducts.contact@gmail.com"
            password = "laoasievylzghdye"
            receiver_email = request.session['email']
            Subject= "Reset Code for AI Healthcare "
            headers = f"From: {sender_email}\nTo: {request.session['email']}\nSubject: {Subject}\n"
            message = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reset Password</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f0f0f0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }

                    .container {
                        background-color: #fff;
                        padding: 2rem;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        width: 100%;
                        max-width: 500px;
                    }

                    h1 {
                        font-size: 2rem;
                        color: #333;
                        margin-bottom: 1rem;
                    }

                    p {
                        font-size: 1.125rem;
                        color: #666;
                        margin-bottom: 1.5rem;
                    }

                    .btn {
                        display: inline-block;
                        background-color: #007bff;
                        color: #fff;
                        text-decoration: none;
                        padding: 0.5rem 1rem;
                        border-radius: 5px;
                        margin-bottom: 1.5rem;
                    }

                    .support {
                        font-size: 15px;
                        color: #666;
                        margin-bottom: 1rem;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Reset Password</h1>
                    <p>Dear , 
                        We have received your request for a reset code for your AI healthcare account. Your reset code for """+ request.session.get('email') +""" is : </p>
                        <a disabled class="btn p-3" style="padding:10px;font-size:25px">"""+ request.session.get('random_str') +"""</a>
                    <p class="support">Please use this code to reset your password on the 'Reset Password' page and follow the prompts to create a new password for your account.</p>
                    <p class="support">If you have any trouble with this process, please do not hesitate to reach out to our customer support team for assistance. </p>
                    <p class="support">Please use this code to reset your password on the 'Reset Password' page and follow the prompts to create a new password for your account.Thank you for using our AI healthcare service.</p>
                    <p class="support">Best,</p>
                    <p class="support">AI Healthcare Team,</p>
                </div>
            </body>
            </html>"""
            
            # Connect to the SMTP server and send the email
            context = ssl.create_default_context()
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, headers+str(message))
            return render(request,'forget.html',content)
    return render(request,'forget.html')

def reset(request):
    # Check if the request method is POST
    if request.POST:
        # Get the pin code from the POST request
        pin = request.POST['pin_code']

        # Compare the pin code with the one stored in the session
        if pin ==  request.session['random_str']:
            # If the pin codes match, return a render with the message "Code Is Correct"
            return render(request,'reset_page.html',{"correct_code":"COde Is Correct Enter Your New Password"})
        else:
            # If the pin codes do not match, return a render with the message "Code Is Incorrect"
            return render(request,'reset_page.html',{"wrong_code":"Code Is Incorrect"})        

    # If the request method is not POST, return a render of the reset_page.html template
    return render(request,'reset_page.html')

def reset_pass(request):
    # Check if the request method is POST
    if request.POST:
        # Get the new password from the POST request
        password = request.POST['password']

        # Count the number of patients with the same email address as the one stored in the session
        count_patient = Signup.objects.filter(
                email_address= request.session['email']).count()
        
        # Count the number of doctors with the same email address as the one stored in the session
        count_doctor = Doctors.objects.filter(
                doc_email_address= request.session['email']).count()

        # If there is at least one doctor with the same email address
        if count_doctor > 0:
            # Get the doctor object
            doctor = Doctors.objects.get(
                doc_email_address= request.session['email'])

            # Get the doctor object using its primary key
            obj = get_object_or_404(Doctors, pk=doctor.id)

            # Update the password of the doctor object
            obj.password = password

            # Save the changes to the doctor object
            obj.save   

            # Return a render with the message "Password Has Been Changed"
            return render(request,'reset_page.html',{"changed":"Password Has Been Changed"})

        # If there is at least one patient with the same email address
        elif count_patient > 0:
            # Get the patient object
            patient = Signup.objects.get(
                email_address= request.session['email'])

            # Get the patient object using its primary key
            obj =get_object_or_404(Signup, pk=patient.id)

            # Update the password of the patient object
            obj.password = password

            # Save the changes to the patient object
            obj.save()

            # Return a render with the message "Password Has Been Changed"
            return render(request,'reset_page.html',{"changed":"Password Has Been Changed"})

    # If the request method is not POST, return a render of the reset_page.html template
    return render(request,'reset_page.html')

    
def logout(request):
    # Try to delete the session 'email'
    try:
    # Delete the session 'email'
        del request.session['email']
    # If the session 'email' does not exist
    except KeyError:
    # Do nothing
        pass
    # Redirect the user to the home page
    return redirect("/home/")

# ////////////////////////////////////
# ////////////////////////////////////
# ////////////////////////////////////
def admin_page(request):
    if request.session.get('email') != "admin123@healthcare.com":
        return redirect('/home')
    # if email is stored in session and patient object is found

    elif (request.session.get('email') == "admin123@healthcare.com"):
        # Check if the request method is GET
        if request.method == 'GET':
            formdata = AddDoctorsForm()
            formdata2 = AddDepartmentForm()
        else:
            formdata = AddDoctorsForm(data=request.POST)
            formdata2 = AddDepartmentForm(data=request.POST)
            if formdata.is_valid():
                formdata.save()
            elif formdata2.is_valid():
                formdata2.save()
            else:
                messages.error(request, 'The form is invalid.')
            return redirect('/admin')
    return render(request, 'admin.html', {'printdata': formdata, 'doc_data': Doctors.objects.all(), 'doc_department': AddDepartmentForm, 'docterdata': AddDepartment.objects.all()})


def patient_page(request):
    # retrieve patient object based on email stored in session
    patient_verified = Signup.objects.filter(email_address = request.session.get('email'))
    print(patient_verified)
    # check if email is stored in session, redirect to login page if not
    if not request.session.get('email'):
        return redirect('/home/')
    # if email is stored in session and patient object is found

    elif patient_verified:
        user = Signup.objects.get(email_address = request.session.get('email'))
        request.session['user_id'] = user.id
        print(request.session.get('user_id'))
        # check if form has been submitted
        if request.POST:
            # retrieve form data
            patient_name = request.POST['patient_name']
            patient_age = request.POST['patient_age']
            patient_disease = request.POST['patient_disease']
            patient_description = request.POST['patient_description']
            # retrieve doctor object based on selected doctor in form
            doctor_info = Doctors.objects.filter(id=request.POST['doctor'])
            
            # create MakeAppointment object and store form data
            appointment = MakeAppointment(
                Your_Name=patient_name,
                Age=patient_age,
                Disease=patient_disease,
                description=patient_description,
                email_address=request.session.get("email"),
                Doctor=doctor_info[0],
                created = datetime.now().date())
            # print(datetime.now().date())
            # print(now().date())
            # save appointment to database
            if appointment:
                appointment.save()

            # redirect to patient page
            return redirect('/home/patient/') 
    
    # Previous Appointments
    previous_appointments = MakeAppointment.objects.filter(email_address = request.session["email"]).order_by('-created')

        # retrieve appointments made by patient
    get_doc_details = MakeAppointment.objects.filter(email_address = request.session.get("email"))
    # store current date
    cur_date = now().date()
    # count number of appointments made today
    order_filter_today = MakeAppointment.objects.filter(created=now().date()).count()
    patient_page = get_doc_details.all()
    paginator = Paginator(patient_page, 5)
    page = request.GET.get('page')
    records = paginator.get_page(page)
    try:
        ids = []
        for i in get_doc_details.all():
            appoint = Review.objects.filter(appoint = i.id).count()     
            if appoint > 0:
                # print(i.id)
                ids.append(i.id)
        # print(ids)
        context = {"appointinfo":{'rcds':records,'ids':ids},'PT':previous_appointments,'patient':patient_verified.all(), "Your_Email":request.session.get('email'), "doc_data":Doctors.objects.all()}
    except Review.DoesNotExist:
            context = {'PT':previous_appointments,'patient':patient_verified.all(),"appointinfo":records, "Your_Email":request.session.get('email'), "doc_data":Doctors.objects.all()}
        
    # print(appoint.id)
    # render patient page with context data
    return render(request, 'patient.html', context)

def review(request,id):
    # retrieve patient object based on email stored in session
    patient_varified = Signup.objects.filter(email_address = request.session.get('email'))
    # retrieve appointment object with specific id and patient email address
    patient_review = MakeAppointment.objects.filter(pk=id, email_address = request.session.get("email"))
    # store doctor id in session
    request.session['doc_id'] = id
    # check if email is stored in session, redirect to login page if not
    if not request.session.get('email'):
        return redirect('/home/')
    # if email is stored in session and patient object is found
    elif patient_varified:
        # render review page with appointment data
        return render(request, 'review.html',{'revieww':patient_review.all()})
    # render review page without appointment data
    return render(request, 'review.html')


def review_page(request):
    # Verify that the user is signed in
    patient_varified = Signup.objects.filter(email_address = request.session.get('email'))
    if not patient_varified:
            return redirect('/home/')
    elif patient_varified :
        patient = Signup.objects.get(email_address = request.session.get('email'))
        # Get the appointment information based on the appointment ID stored in the session
        patient_info = MakeAppointment.objects.filter(pk=request.session.get('doc_id'), email_address = request.session.get("email"))
        # Get the specific appointment object based on the appointment ID stored in the session
        patient_review = MakeAppointment.objects.get(pk=request.session.get('doc_id'), email_address = request.session.get("email"))
        # Print the appointment ID
        # print(patient_review.id)
        # request.session['key'] = 0
        # Check if the form was submitted
        if request.POST:
            # Get the patient object
            patient_id = patient
            # Get the doctor object associated with the appointment
            doc_id =  patient_review.Doctor
            # Print the doctor ID
            # print(doc_id)
            # Get the doctor rating from the form
            doctor_rating = request.POST['doctor_rating']
            # Get the doctor review from the form
            doctor_review = request.POST['doctor_review']

            # Create a Review object
            review = Review(patient = patient_id, 
                            doc = doc_id,
                            appoint=patient_review, 
                            review_write = doctor_review, 
                            review_star=doctor_rating )
             # Save the updated doctor object
            review.save()
                # Render the review page with an error message
            return render(request, 'review.html',{'revieww':patient_info.all(),"success":"Review Sent Successfully! "})
        
    # Render the review page with the appointment information
    return render(request, 'review.html',{'revieww':patient_info.all()})

def doctor_page(request):
    # Check if the doctor is registered in the system
    count_doctor = Doctors.objects.filter(doc_email_address=request.session.get("email"))
    # If the doctor is not registered, redirect to home page
    if not count_doctor:
        return redirect('/home/')
    # If the doctor is registered, retrieve the doctor's information and appointments
    elif count_doctor:
        for i in count_doctor.all():
            timing = i.doc_timming
            treatments = MakeAppointment.objects.filter(Doctor = i.id)
            created = MakeAppointment.objects.filter(Doctor = i.id , created=now().date()).count()
        date = now().date()
        total_no_of_treatments = treatments.count()
        paginator = Paginator(treatments, 10)
        page = request.GET.get('page')
        appointment = paginator.get_page(page)
        # Create a context dictionary to store the doctor's information and appointments
        context = {"Your_Email": request.session.get('email'),"treatments":appointment, 'date': date, 'total_no_of_treatments': total_no_of_treatments,'timing':timing, 'today_appointment':created}
        return render(request, 'doctor.html', context)

# ////////////////////////////////////
# ////////////////////////////////////
# ////////////////////////////////////

def doctor_rec(request):
    # Get all departments from the database
    departments = AddDepartment.objects.all()
    # Check if the user has submitted a department
    if request.method == 'POST':
        # Get the selected department
        selected_department = request.POST.get('department')
        print(selected_department)
        # Get all doctors belonging to the selected department
        if selected_department == 'all':
            doctors = Doctors.objects.all()
        else:
            doctors = Doctors.objects.filter(doc_department=selected_department)

        # Render the doctors page with the filtered doctors
        return render(request, 'doctorRec.html', {'departments':departments, 'doctors':doctors})

    # If no department is selected, show all doctors
    doctors = Doctors.objects.all()
    # Create a context dictionary to store the department and doctor information
    CONTEXT = {'departments':departments, 
                'doctors': doctors}
    return render(request, 'doctorRec.html', CONTEXT)

def patient_rec(request):
    # Create a context dictionary to store the patient and department information
    CONTEXT = {'patientrec_details': Signup.objects.all(), 'docterdata': AddDepartment.objects.all()}
    return render(request, 'patientsRec.html', CONTEXT)

def treatments(request):
    appoint = MakeAppointment.objects.all()
    department = AddDepartment.objects.all()

    paginator = Paginator(appoint, 10)
    page = request.GET.get('page')
    appointment = paginator.get_page(page)
    # Create a context dictionary to store the treatment information
    CONTEXT = {'treated':appointment, 'docterdata': department}
    return render(request, 'treatments.html', CONTEXT)


# ////////////////////////////////////
# ////////////////////////////////////
# ////////////////////////////////////

# The view_doctor_pro function retrieves the doctor details associated with the current session email.
# If the email is not found, the user is redirected to the home page.
# Otherwise, the details are displayed in the "viewDoctorProfile.html" template.

def view_doctor_pro(request):
    # Count the number of doctors with the same email address as the current session's email.
    count_doctor = Doctors.objects.filter(doc_email_address=request.session.get("email")).count()
    # If no doctor is found, redirect to the home page.
    if count_doctor < 1:
        return redirect('/home/')
    else:
        # Get the doctor's details.
        get_doc_details = Doctors.objects.filter(doc_email_address = request.session.get("email"))
    # Render the doctor's details in the "viewDoctorProfile.html" template.
    return render(request, 'viewDoctorProfile.html' , {"doc_details":get_doc_details.all()})

# The view_patient_pro function retrieves the patient details associated with the current session email.
# If the email is not found, the user is redirected to the home page.
# Otherwise, the patient's details and treatments are displayed in the "viewPatientProfile.html" template.

def view_patient_pro(request):
    # Check if the patient with the current session email exists in the database.
    count_patient = Signup.objects.filter(email_address=request.session.get("email"))
    # If the patient is not found, redirect to the home page.
    if not count_patient:
        return redirect('/home/')
    else:
        # Get the patient's treatments.
        patient_treatments = MakeAppointment.objects.filter(email_address=request.session["email"])
        # Get the patient's details.
        get_patient_details = Signup.objects.get(email_address = request.session.get("email"))
    # Render the patient's details and treatments in the "viewPatientProfile.html" template.
    return render(request, 'viewPatientProfile.html' , {"patient_details":get_patient_details,"patient_treat":patient_treatments.all()})

# ////////////////////////////////////
# ////////////////////////////////////
# ////////////////////////////////////

def view_admin_pro(request):
    # Render the "viewAdminProfile.html" template.
    return render(request, 'viewAdminProfile.html')


def view_patient_edit_pro(request,id):
    # Get the patient data associated with the current session email.
    patient_data = Signup.objects.filter(email_address=request.session.get("email"))
    # Count the number of patients with the same email address.
    count_patient = patient_data.count()
    # If the patient is not found, redirect to the home page.
    if count_patient < 1:
        return redirect('/home/')
    else:
        # If the patient is found...
        if count_patient > 0:
            # Get the patient's record with the given id.
            record = get_object_or_404(Signup, pk=id)
            # Check if the request method is POST
            if request.method == 'POST':
                # Get the updated data from the form
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                state = request.POST.get('state')
                city = request.POST.get('city')
                address = request.POST.get('Address')
                email_address = request.POST.get('email_address')
                password = request.POST.get('password')
                phone_number = request.POST.get('phone_number')

                # Update the record's fields with the data from the form
                record.first_name = first_name
                record.last_name = last_name
                record.state = state
                record.city = city
                record.Address = address
                record.email_address = email_address
                record.password = password
                record.phone_number = phone_number

                # Save the updated record to the database
                record.save()

                # Return the updated data to the template for display
                return render(request, 'editpro.html', {
                    'data_patient': patient_data.all(),
                    "success": "Updated Successfully! "
                })
        return render(request, "editpro.html", {'data_patient':patient_data.all()})
        

def view_doctor_edit_pro(request, id):
    # Get the doctor's data for the current logged in user
    doctor_data = Doctors.objects.filter(doc_email_address=request.session.get("email"))
    # Count the number of doctors
    count_doctor = doctor_data.count()
    # If no doctor is found, redirect to home
    if count_doctor < 1:
        return redirect('/home/')
    else:
        if count_doctor > 0:
            # Get the doctor with the given id
            doctor = get_object_or_404(Doctors, pk=id)
            # Print the email address of the doctor
            if request.method == 'POST':
                # Update the doctor's fields with the data from the form
                doctor.doc_name = request.POST.get('doc_name')
                doctor.doc_post = request.POST.get('doc_post')
                doctor.doc_timming = request.POST.get('doc_timming')
                doctor.doc_ranking = request.POST.get('doc_ranking')
                doctor.doc_room = request.POST.get('doc_room')
                doctor.doc_specialization = request.POST.get('doc_specialization')
                doctor.phone_number = request.POST.get('phone_number')
                doctor.doc_email_address = request.POST.get('doc_email_address')
                doctor.password = request.POST.get('password')
                # Save the changes to the database
                doctor.save()
                # Render the doctor_edit.html template with success message and all doctor data
                return render(request, "doctor_edit.html", {'data_doctor':doctor_data.all(), 'success':"Updated Successfully! "})
    # Render the doctor_edit.html template with all doctor data
    return render(request, 'doctor_edit.html',{'data_doctor':doctor_data.all()})


def chat_send(request):
    # Get the patient data associated with the current session email.
    patient_data = Signup.objects.filter(email_address=request.session.get("email"))
    # Count the number of patients with the same email address.
    count_patient = patient_data.count()
    # If the patient is not found, redirect to the home page.
    if count_patient < 1:
        return redirect('/home/')
    else:
        if request.method == "POST":
            model_engine = "gpt-3.5-turbo"
            message = request.POST['message']
            # Initialize the messages with a system message if it's the first message.
            # Get the conversation history from the session
            conversation_history = request.session.get('conversation_history', [{"role": "system", "content": 
                """
                you will provide a statment in which user tell you about there physical condition and also ask your help to suggest them medicine to reduce the pain or effect of disease. 
                Note: 
                1-> [Don't answer question which is not related to the medical field just say 'As a medical assistant, I can’t answer the [provided request] but I can help with medical-related queries'] 
                2-> [your reply must be straitforward do not explain anything! ]
                3-> [try to use emojies in your answer]
                """
                }])
        
            # Check if there's a message
            if message:
                conversation_history.append({"role": "user", "content": message})

                # Create the chat
                chat = openai.ChatCompletion.create(
                    model=model_engine,
                    messages=conversation_history,
                    max_tokens=300
                )

            reply = chat.choices[0].message['content']
            conversation_history.append({"role": "assistant", "content": reply})
            
            # Save the updated conversation history back to the session
            request.session['conversation_history'] = conversation_history
            response = {'message': reply}
        return JsonResponse(response)


# calculate the average of review_Stars and add into each doctor's record
doctors = Doctors.objects.all()
for doctor in doctors:
    # get all reviews for the doctor
    reviews = Review.objects.filter(doc=doctor)
    # count the number of reviews
    review_count = reviews.count()
    # sum of all review stars
    review_sum = reviews.aggregate(Sum('review_star'))['review_star__sum']
    # calculate the average
    if review_count > 0:
        average = review_sum / review_count
    else:
        # set average to 0 if there are no reviews
        average = 0
    # save the average as doctor's ranking
    doctor.doc_ranking = round(average,1)
    # print(round(average,1))
    doctor.save() 