from email.message import EmailMessage
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.http.response import HttpResponseRedirect
# from django.core.mail import EmailMessage
from django.conf import settings
from .models import Doctor,Appointment,AreaOfInterest
from django.utils.timezone import now
from django.contrib import messages
from .models import Feedback
import datetime
from django.core.files.storage import FileSystemStorage
from .models import Media
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import AppointmentSerializer, FeedbackSerializer, DoctorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from django.core.mail import send_mail
import json
from .serializers import ServicesSerializer, ResearchSerializer 
from rest_framework.parsers import JSONParser
from .models import Services, Research
from .models import VideoComment
from .serializers import VideoCommentSerializer
from .models import Services,Vedic
from rest_framework.views import APIView






@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"csrfToken": "Token set"})


# View to display doctor details and areas of interest






@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def doctor_details(request):
    if request.method == 'GET':
        try:
            # Fetch the doctor with the greatest id
            doctor = Doctor.objects.latest('id')  # This retrieves the doctor with the highest id
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=404)

    elif request.method == 'POST':
        try:
            serializer = DoctorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Saves the new doctor and uploaded file
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            # Catch other unexpected errors for debugging
            return Response({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)


from rest_framework.parsers import JSONParser

@csrf_exempt
@parser_classes([JSONParser])  # Change to JSONParser if no files are uploaded
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def add_service(request):
    if request.method == 'POST':
        try:
            serializer = ServicesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)

    elif request.method == 'GET':
        services = Services.objects.all()
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'DELETE':
        service_id = request.data.get('id')  # Get the service ID from the request body
        try:
            service = Services.objects.get(id=service_id)
            service.delete()
            return Response({'message': f'Service {service_id} deleted successfully'}, status=200)
        except Services.DoesNotExist:
            return Response({'error': 'Service not found'}, status=404)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)

    elif request.method == 'PUT':
        service_id = request.data.get('id')  # Get the service ID
        try:
            service = Services.objects.get(id=service_id)
            serializer = ServicesSerializer(service, data=request.data)
            if serializer.is_valid():
                serializer.save()  # Update the service
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Services.DoesNotExist:
            return Response({'error': 'Service not found'}, status=404)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)


@csrf_exempt
def get_services(request):
    services = Services.objects.all()
    data = [
        {"id": services.id, "service_name": services.service_name, "description": services.description}
        for services in services
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def research_view(request, id=None):
    if request.method == 'GET':
        researches = Research.objects.all()
        serializer = ResearchSerializer(researches, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            research = Research.objects.get(id=id)
            serializer = ResearchSerializer(research, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Research.DoesNotExist:
            return Response({'error': 'Research not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        try:
            research = Research.objects.get(id=id)
            research.delete()
            return Response({'message': 'Research deleted successfully'}, status=status.HTTP_200_OK)
        except Research.DoesNotExist:
            return Response({'error': 'Research not found'}, status=status.HTTP_404_NOT_FOUND)

# @csrf_exempt
# def send_doctor_email(request):
#     """
#     Sends a notification email to the doctor for a created appointment.
#     """
#     if request.method == "POST":
#         try:
#             # Parse JSON data from the request body
#             data = json.loads(request.body)

#             # Get the appointment ID
#             appointment_id = data.get('appointmentId')
#             if not appointment_id:
#                 return JsonResponse({"error": "Missing appointment ID"}, status=400)

#             # Fetch the appointment details
#             appointment = Appointment.objects.get(id=appointment_id)

#             # Compose email
#             subject = f"New Appointment Request from {appointment.user_name}"
#             message = f"""
#                 Name: {appointment.user_name}
#                 Age: {appointment.user_age}
#                 Gender: {appointment.user_gender}
#                 Email: {appointment.user_email}
#                 Phone: {appointment.user_phone}
#                 Problem: {appointment.problem_description}
#                 Appointment Date/Time: {appointment.appointment_date_time}
#             """

#             # Send email
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email="your_email@example.com",
#                 recipient_list=["krishnarb08@gmail.com"],
#             )

#             return JsonResponse({"success": "Doctor notified successfully"}, status=200)

#         except Appointment.DoesNotExist:
#             return JsonResponse({"error": "Appointment not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid request method"}, status=405)

# working


from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer
from django.core.mail import send_mail

@csrf_exempt
@api_view(['POST'])
def create_appointment(request):
    if request.method == 'POST':
        # Serialize the incoming data
        serializer = AppointmentSerializer(data=request.data)
        
        # Validate the data
        if serializer.is_valid():
            # Save the data if valid
            appointment = serializer.save()

            # Compose the email content
            email_subject = f"Appointment Request from {appointment.user_name}"
            email_message = f"""
                Appointment Details:
                --------------------
                Staus: Unconfirmed
                Name: {appointment.user_name}
                Age: {appointment.user_age}
                Gender: {appointment.user_gender}
                Email: {appointment.user_email}
                Phone: {appointment.user_phone}
                Problem: {appointment.problem_description}
                Appointment Date/Time: {appointment.appointment_date_time}


                EMAIL about the appointment.
            """

            try:

                recipient_list = ["sijanofficial1@gmail.com", appointment.user_email]
                # Send email to `sijanofficial1@gmail.com`
                print("Sending email")
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email="krishnarb08@gmail.com",  # Replace with your email
                    recipient_list=recipient_list,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                # Optional: Return a partial success response indicating email failure
                return Response({
                    "appointment": serializer.data,
                    "email_error": "Appointment created but email failed to send."
                }, status=status.HTTP_201_CREATED)

            # Return success response with the created appointment data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log the errors to help identify the problem
            print(serializer.errors)  # This will print validation errors to the console for debugging
            # Return validation errors if data is invalid
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle cases where the method is not POST
    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



def get_appointments(request):
    appointments = Appointment.objects.all().values(
        "id",
        "user_name",
        "user_age",
        "user_gender",
        "user_email",
        "user_phone",
        "problem_description",
        "appointment_date_time",
        "status"
    )
    return JsonResponse(list(appointments), safe=False)


# View to manage feedback (for admin use)
@csrf_exempt 
def manage_feedback(request):
    # Ensure 'id' is included in the response
    feedbacks = Feedback.objects.all().values(
        "id",  # Ensure 'id' is included in the response
        "user_name",
        "user_email",
        "message",
    )  # Retrieve all feedback

    return JsonResponse(list(feedbacks), safe=False)

@csrf_exempt
def delete_feedback(request, feedback_id):
    if request.method == 'DELETE':
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.delete()  # Delete the feedback from the database
            print(f"Feedback with ID {feedback_id} deleted.")  # Debug log
            return JsonResponse({'message': 'Feedback deleted successfully'}, status=200)
        except Feedback.DoesNotExist:
            print(f"Feedback with ID {feedback_id} not found.")  # Debug log
            raise Http404("Feedback not found")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def approve_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.approved = True  # Mark the feedback as approved
            feedback.save()  # Save the changes
            return JsonResponse({'message': 'Feedback approved successfully'}, status=200)  # Return 200 status code
        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Feedback not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Catch other errors
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['GET'])
def approved_feedbacks(request):
    approved_feedbacks = Feedback.objects.filter(approved=True)
    serializer = FeedbackSerializer(approved_feedbacks, many=True)
    return Response(serializer.data)



@csrf_exempt
def manage_appointment(request):
    if request.method == "POST":
        # Retrieve the POST data
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment_id")

        try:
            # Fetch the appointment by ID
            appointment = Appointment.objects.get(id=appointment_id)

            # Update the appointment status and accepted date
            appointment.status = 'confirmed'  # Assuming confirmed means accepted
            appointment.appointment_date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")  # Convert string to datetime
            appointment.updated_at = datetime.datetime.now()  # Update the time to now
            appointment.save()

            # Prepare the email
            data = {
                "name": appointment.user_name,
                "date": date,
            }

            # Prepare the message body and send an email
            message = render_to_string('appointment_acceptance_email.html', data)  # type: ignore # Assuming you have an HTML template
            email = EmailMessage(
                subject="About your appointment",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[appointment.user_email]
            )
            email.content_subtype = "html"  # Set the email body as HTML
            email.send()

            # Success message
            messages.success(request, f"You have accepted the appointment of {appointment.user_name}.")

            # Redirect to the same page (or a different page, if necessary)
            return HttpResponseRedirect(request.path)

        except Appointment.DoesNotExist:
            return HttpResponse("Appointment not found.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    else:
        # GET request (display the list of appointments)
        appointments = Appointment.objects.all()
        context = {
            "title": "Manage Appointments",
            "appointments": appointments,
        }
        
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vedic
from .serializers import VedicSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class VedicListCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        vedics = Vedic.objects.all()
        serializer = VedicSerializer(vedics, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = VedicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VedicDetailAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk):
        vedic = Vedic.objects.get(id=pk)
        serializer = VedicSerializer(vedic, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        vedic = Vedic.objects.get(id=pk)
        serializer = VedicSerializer(vedic, data=request.data, partial=True)  # partial allows updating only some fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vedic = Vedic.objects.get(id=pk)
        vedic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# working
@csrf_exempt  # Only for development purposes
@api_view(['POST'])
def submit_feedback(request):
    if request.method == 'POST':
        # Use .data instead of .POST for JSON requests
        username = request.data.get('username')
        useremail = request.data.get('useremail')
        message = request.data.get('message')

        if username and useremail and message:
            Feedback.objects.create(
                user_name=username,
                user_email=useremail,
                message=message
        )

            return JsonResponse({"message": "Feedback submitted successfully!"}, status=201)
        return JsonResponse({"error": "Invalid data provided"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)

    

# View to approve feedback (admin only)
@csrf_exempt 
def approve_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.approved = True  # Set approved to True
        feedback.save()

        # Success message
        messages.success(request, f"Feedback from {feedback.user_name} has been approved.")

    except Feedback.DoesNotExist:
        messages.error(request, "Feedback not found.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page


# View to reject feedback (admin only)

def reject_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.approved = False  # Set approved to False
        feedback.save()

        # Success message
        messages.success(request, f"Feedback from {feedback.user_name} has been rejected.")

    except Feedback.DoesNotExist:
        messages.error(request, "Feedback not found.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Media


# Detail view for a specific Research Paper
def research_paper_detail(request, pk):
    research_paper = get_object_or_404(Media, pk=pk, media_type='research_paper')
    return render(request, 'media/research_paper_detail.html', {'research_paper': research_paper})

# Detail view for a specific Video
def video_detail(request, pk):
    video = get_object_or_404(Media, pk=pk, media_type='video')
    return render(request, 'media/video_detail.html', {'video': video})


# resaerch paper

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Media

# View for listing all Research Papers
def research_paper_list(request):
    research_papers = Media.objects.filter(media_type='research_paper')
    return render(request, 'media/research_paper_list.html', {'research_papers': research_papers})

# View for listing all Videos
def video_list(request):
    videos = Media.objects.filter(media_type='video')
    return render(request, 'media/video_list.html', {'videos': videos})

# Detail view for a specific Research Paper
def research_paper_detail(request, pk):
    research_paper = get_object_or_404(Media, pk=pk, media_type='research_paper')
    return render(request, 'media/research_paper_detail.html', {'research_paper': research_paper})

# Detail view for a specific Video
def video_detail(request, pk):
    video = get_object_or_404(Media, pk=pk, media_type='video')
    return render(request, 'media/video_detail.html', {'video': video})




from .models import VideoComment
from .serializers import VideoCommentSerializer

class VideoCommentAPIList(APIView):
    # Retrieve all comments
    def get(self, request):
        comments = VideoComment.objects.all()
        serializer = VideoCommentSerializer(comments, many=True)
        return Response(serializer.data)

    # Create a new comment
    def post(self, request):
        serializer = VideoCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the comment to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital
from .serializers import HospitalSerializer

class HospitalListCreateAPIView(APIView):
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HospitalSerializer(hospital)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalSerializer(hospital, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)

        hospital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def get_hospital_data(request):
    try:
        # Fetch all hospital data
        hospitals = Hospital.objects.all()  # Fetch all hospital data from the database
        serializer = HospitalSerializer(hospitals, many=True)  # Serialize all hospital records
        return Response(serializer.data)
    except Hospital.DoesNotExist:
        return Response({'error': 'No hospital data found'}, status=404)








import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment
from .utils import send_appointment_confirmation_email  # Assuming this is your email utility

@csrf_exempt
def confirm_appointment(request, appointment_id):
    print(request.GET)
    print(appointment_id)
    try:
        # Retrieve the appointment using the passed appointment_id
        appointment = Appointment.objects.get(id=appointment_id)

        # Update the status to confirmed
        appointment.status = 'confirmed'
        appointment.save()

        # Send confirmation email
        print("going inside send_mail")
        # send_appointment_confirmation_email(
        #     user_email=appointment.user_email,
        #     appointment_date=appointment.appointment_date_time,
        #     user_name=appointment.user_name  # Pass the user_name here
        # )
        subject = 'Appointment Confirmed'
        message = f'Hello {appointment.user_email},\n\nYour appointment has been confirmed for {appointment.appointment_date_time}. Please come for your check-up.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [appointment.user_email]
        send_mail(subject, message, from_email, recipient_list)
        print("send mail succeeded")

        return JsonResponse({'message': 'Appointment confirmed successfully!'})
    
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['DELETE'])
def delete_all_video_comments(request):
    try:
        VideoComment.objects.all().delete()  # Deletes all rows in the table
        return Response({"message": "All comments deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Logup
# from .serializers import UserSerializer


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework import status
from .models import Logup  # Assuming you have a Logup model (custom user model)

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# def login(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Authenticate the user by checking username and password
#         try:
#             user = Logup.objects.get(username=username)
#             if user.password == password:  # In a real app, compare hashed passwords
#                 return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Logup.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
