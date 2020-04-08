from django.contrib import admin

from .models import Status, Affil, Guess, Article, Work

# Register your models here.

admin.site.register(Status)
admin.site.register(Affil)
admin.site.register(Guess)
admin.site.register(Article)
admin.site.register(Work)