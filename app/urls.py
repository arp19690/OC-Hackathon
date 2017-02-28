from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^test/', views.get_ga_real_time_data,name="test"),
]
