from rest_framework import serializers
from .models import Doctor, Appointment, AreaOfInterest, Feedback, Media
from rest_framework.validators import UniqueValidator
from .models import Services
from .models import VideoComment

class DoctorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Doctor.objects.all(),
                message="A doctor with this email already exists."
            )
        ]
    )
    class Meta:
        model = Doctor
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'service_name', 'description'] 

from .models import Research

class ResearchSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Research
        fields = ['id', 'title', 'description', 'pdf', 'pdf_url']

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf and request:
            return request.build_absolute_uri(obj.pdf.url)
        return None

class AppointmentSerializer(serializers.ModelSerializer):
    appointment_date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")  # ISO 8601 format

    class Meta:
        model = Appointment
        fields = [
            'user_name',
            'user_age',
            'user_gender',
            'user_email',
            'user_phone',
            'problem_description',
            'appointment_date_time',
            'status',
        ]
class AreaOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfInterest
        fields = ['id', 'name', 'description']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user_name', 'user_email', 'message', 'approved']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'media_type', 'file_url']




# myapp/serializers.py
from .models import VideoComment


class VideoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = ['id', 'comment_text', 'created_at']  # Include the fields you need






from .models import Vedic


class VedicSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Vedic
        fields = ['id', 'title', 'file', 'file_url', 'created_at']

    def get_file_url(self, obj):
        return obj.get_file_url()

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_file(self, value):
        if not value:
            raise serializers.ValidationError("File is required.")
        return value



from .models import Hospital

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'time']



from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user_name', 'user_email', 'message', 'approved', 'created_at']


from rest_framework import serializers
from .models import Logup

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logup
        fields = ['username', 'password']
