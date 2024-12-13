# myapp/urls
from django.urls import path
from . import views
from .views import csrf
from .views import get_appointments
from .views import VedicListCreateAPIView, VedicDetailAPIView
from .views import HospitalListCreateAPIView, HospitalDetailAPIView
from .views import VideoCommentAPIList 

urlpatterns = [
    # View to display doctor details and areas of interest
    path('doctor/details/', views.doctor_details, name='doctor_details'),

    # View to send doctor email
    # path('doctor/email/', views.send_doctor_email, name='send_doctor_email'),

    path('add_service', views.add_service, name='add_services'),

    # View to create an appointment
    path('create_appointment/', views.create_appointment, name='create_appointment'),

    # View to manage appointments (for admin)
     path("api/manage_appointment/", views.manage_appointment, name="manage_appointment"),

    # View to submit feedback
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),

    # View to manage feedback (for admin)
    path('feedback/manage/', views.manage_feedback, name='manage_feedback'),

    # View to approve feedback (admin only)
    path('feedback/approve/<int:feedback_id>/', views.approve_feedback, name='approve_feedback'),

    # View to reject feedback (admin only)
    path('feedback/reject/<int:feedback_id>/', views.delete_feedback, name='approve_feedback'),

    path('feedback/approved/', views.approved_feedbacks, name='approved_feedbacks'),


    path('research-papers/', views.research_paper_list, name='research_paper_list'),
    path('research-papers/<int:pk>/', views.research_paper_detail, name='research_paper_detail'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/<int:pk>/', views.video_detail, name='video_detail'),

    path('api/appointments/', get_appointments, name='get_appointments'),

    path('research/', views.research_view, name='research_view'),
    path('research/<int:id>/', views.research_view),

    path('video_comments/', VideoCommentAPIList.as_view(), name='video_comments'),

    path("api/services/", views.get_services, name="get_services"),

    path('vedic/', VedicListCreateAPIView.as_view(), name='vedic-list-create'),
    path('vedic/<int:pk>/', VedicDetailAPIView.as_view(), name='vedic-detail'),



    path('hospitals/', HospitalListCreateAPIView.as_view(), name='hospital-list-create'),
    path('hospitals/<int:pk>/', HospitalDetailAPIView.as_view(), name='hospital-detail'),

    path('api/confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('appointments/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),


    path('delete_all_comments/', views.delete_all_video_comments, name='delete_all_video_comments'),

    path('api/hospital/', views.get_hospital_data, name='hospital_data'), 


    path('login/', views.login, name='login'),



    path("csrf/", csrf, name="csrf"),
]