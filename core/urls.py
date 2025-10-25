from django.urls import path
from . import views

urlpatterns = [
    # ------Urls para libro------
    path('', views.book_list, name='home'),

]