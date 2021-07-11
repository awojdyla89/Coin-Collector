# Add the following import
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Coin, Grading #importing the model, model talks to db 
# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import AppraisalsForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class CoinCreate(LoginRequiredMixin, CreateView):
  model = Coin
  # fields = '__all__'
  fields = ['name', 'metallurgy', 'description', 'year']
  #success_url = '/coins/'
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class CoinUpdate(LoginRequiredMixin, UpdateView):
  model = Coin
  # Let's disallow the renaming of a coin by excluding the name field!
  fields = ['metallurgy', 'description', 'year']

class CoinDelete(LoginRequiredMixin, DeleteView):
  model = Coin
  success_url = '/coins/'


# Define the home view, the route is in urls.py
def home(request):
  return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def coins_index(request):
    #coins = Coin.objects.all()
    coins = Coin.objects.filter(user=request.user)
    return render(request, 'coins/index.html', {'coins': coins})

@login_required
def coins_detail(request, coin_id):
    coin = Coin.objects.get(id=coin_id)

    gradings_coin_doesnt_have = Grading.objects.exclude(id__in = coin.gradings.all().values_list('id'))
    # instantiate FeedingForm to be rendered in the template
    appraisals_form = AppraisalsForm()
    return render(request, 'coins/detail.html', {
      'coin': coin, 
      'appraisals_form': appraisals_form,
      'gradings': gradings_coin_doesnt_have
      })

@login_required
def add_appraisals(request, coin_id):
      # create a ModelForm instance using the data in request.POST
    form = AppraisalsForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_appraisals = form.save(commit=False)
        new_appraisals.coin_id = coin_id
        new_appraisals.save()
    return redirect('detail', coin_id=coin_id)

@login_required
def assoc_grading(request, coin_id, grading_id):
  Coin.objects.get(id=coin_id).gradings.add(grading_id)
  return redirect('detail', coin_id=coin_id)

class GradingList(LoginRequiredMixin, ListView):
  model = Grading

class GradingDetail(LoginRequiredMixin, DetailView):
  model = Grading

class GradingCreate(LoginRequiredMixin, CreateView):
  model = Grading
  fields = '__all__'

class GradingUpdate(LoginRequiredMixin, UpdateView):
  model = Grading
  fields = ['grading', 'luster']

class GradingDelete(LoginRequiredMixin, DeleteView):
  model = Grading
  success_url = '/gradings/'