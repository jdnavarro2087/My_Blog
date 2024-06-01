# posts/admin.py
from django.contrib import admin
from .models import Post, Status, Priority

admin.site.register(Post)
admin.site.register(Status)
admin.site.register(Priority)
