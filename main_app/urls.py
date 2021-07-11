
from django.urls import path
from django.urls.conf import include # path function is used to define each route
from . import views

# '' is root or localhost:8000
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('coins/', views.coins_index, name='index'),
    path('coins/<int:coin_id>/', views.coins_detail, name='detail'),
    # new route used to show a form and create a coin
    path('coins/create/', views.CoinCreate.as_view(), name='coins_create'),
    path('coins/<int:pk>/update/', views.CoinUpdate.as_view(), name='coins_update'),
    path('coins/<int:pk>/delete/', views.CoinDelete.as_view(), name='coins_delete'),
    path('coins/<int:coin_id>/add_appraisals/', views.add_appraisals, name='add_appraisals'),
    # associate a grading with a coin (M:M)
    path('coins/<int:coin_id>/assoc_grading/<int:grading_id>/', views.assoc_grading, name='assoc_grading'),
    path('gradings/', views.GradingList.as_view(), name='gradings_index'),
    path('gradings/<int:pk>/', views.GradingDetail.as_view(), name='gradings_detail'),
    path('gradings/create/', views.GradingCreate.as_view(), name='gradings_create'),
    path('gradings/<int:pk>/update/', views.GradingUpdate.as_view(), name='gradings_update'),
    path('gradings/<int:pk>/delete/', views.GradingDelete.as_view(), name='gradings_delete'),

    path('accounts/signup/', views.signup, name='signup'),
]