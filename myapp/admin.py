from django.contrib import admin
from .models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "email", "updated_at", "created_at") # this will dispaly at admin


admin.site.register(Student, StudentAdmin)
