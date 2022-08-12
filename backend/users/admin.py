from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    search_fields = ('email', 'username')
