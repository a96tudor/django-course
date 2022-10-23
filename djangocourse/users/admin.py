from django.contrib import admin

# Register your models here.


from .models import UserProfile, Skill, Message

admin.site.register(UserProfile)
admin.site.register(Skill)
admin.site.register(Message)
