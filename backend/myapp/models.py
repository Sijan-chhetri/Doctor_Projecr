from django.db import models
from django.utils.timezone import now

# Doctor Model


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    specialization = models.CharField(max_length=255, null=False)
    profile_image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=15, null=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    


# Hospital Model
# class Hospital(models.Model):
#     name = models.CharField(max_length=255, null=False)
#     location = models.CharField(max_length=255, null=False)
#     available_time = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.name

class Services(models.Model):
    id = models.AutoField(primary_key=True)
    service_name=models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)

class Research(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='research_papers/')

    def __str__(self):
        return self.title



# Media Models
class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('research_paper', 'Research Paper'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=50, choices=MEDIA_TYPE_CHOICES, null=False)
    file_url = models.URLField(max_length=500, null=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Vedic(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='vedic_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        if self.file:
            return self.file.url
        return None
    
    def __str__(self):
        return self.title

class VideoComment(models.Model):
    comment_text = models.TextField()  # The comment text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment is created

    def __str__(self):
        return self.comment_text[:20] 





# Feedback Model
class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, null=False)
    user_email = models.EmailField(null=False)
    message = models.TextField(null=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Feedback by {self.user_name}"

# Appointment Model
class Appointment(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, null=False)
    user_age = models.IntegerField(null=False)
    user_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=False)
    user_email = models.EmailField(null=False)
    user_phone = models.CharField(max_length=15, null=False)
    problem_description = models.TextField(blank=True, null=True)
    appointment_date_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Appointment for {self.user_name}"


# AreaOfInterest Model
class AreaOfInterest(models.Model):
    id = models.AutoField(primary_key=True)
    interest = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.interest








class Hospital(models.Model):
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=50)  # Store active time in string format, e.g., '3 - 10'

    def __str__(self):
        return self.name



from django.db import models

class Logup(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # In real applications, store a hashed password

    def __str__(self):
        return self.username



