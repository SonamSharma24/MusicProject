from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.


admin.site.register(Profile)


class SongAdmin(admin.ModelAdmin):
	list_display=('song_id','name','singer','image','movie','song')

admin.site.register(Song,SongAdmin)
