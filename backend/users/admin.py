from django.contrib import admin
from users.models import CustomUser, Subscribe


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'last_name')
    ordering = ('username', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscribe)
