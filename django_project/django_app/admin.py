from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import Profile


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('id', 'user', 'get_photo')
    list_display_links = ('id',)
    fields = ('user', 'image', 'get_photo', 'image_url')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return 'no avatar'

    get_photo.short_description = 'avatar'


admin.site.register(Profile, ProfileAdmin)
