from django.forms import ModelForm
from .models import Appraisals

class AppraisalsForm(ModelForm):
  class Meta:
    model = Appraisals
    fields = ['date', 'appointment']