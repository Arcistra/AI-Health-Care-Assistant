from django.contrib.admin.decorators import register
from django.urls import path, include
from .import views
# from .views import app_view

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('patient/', views.patient_page, name='patient_page'),
    path('send/', views.chat_send, name='chat_msg'),
    path('review/<int:id>/',views.review, name='review_func'),
    path('review_function/',views.review_page, name='review_page'),
    path('doctor/', views.doctor_page, name='doctor_page'),
    path('login/', views.login_page, name='login_page'),
    path('forget_password/', views.forget_page, name='forget_page'),
    path('reset/', views.reset, name='reset_page'),
    path('reset_password/', views.reset_pass, name='reset_pass_page'),
    path('logout/', views.logout, name='logged_out'),
    path('signup/', views.signup_page, name='signup_page'),
    path('doctorRec/', views.doctor_rec, name='doctor_rec'),
    path('viewDoctorProfile/', views.view_doctor_pro, name='view_doctor_pro'),
    path('viewAdminProfile/', views.view_admin_pro, name='view_admin_pro'),
    path('viewPatientProfile/', views.view_patient_pro, name='view_patient_pro'),
    path('patientprofileedit/<int:id>', views.view_patient_edit_pro, name='view_patient_edit'),
    path('doctorprofileedit/<int:id>', views.view_doctor_edit_pro, name='view_doctor_edit'),
    path('patientRec/', views.patient_rec, name='patient_rec'),
    path('treatments/',views.treatments, name='treatments_page'),
]
