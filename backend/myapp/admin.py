from django.contrib import admin
from .models import Doctor, Hospital, Media, Feedback, Appointment, AreaOfInterest

# Register models directly with the admin site
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Media)
admin.site.register(Feedback)
admin.site.register(Appointment)
admin.site.register(AreaOfInterest)