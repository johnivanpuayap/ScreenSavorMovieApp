from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(WatchList)
admin.site.register(WatchHistory)
