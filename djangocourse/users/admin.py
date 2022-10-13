from django.contrib import admin

# Register your models here.


from .models import UserProfile, Skill

admin.site.register(UserProfile)
admin.site.register(Skill)
