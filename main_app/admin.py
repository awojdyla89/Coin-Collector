from django.contrib import admin
# import your models here
from .models import Coin, Appraisals, Grading

# Register your models here
admin.site.register(Coin)
admin.site.register(Appraisals)
admin.site.register(Grading)