from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^real-time/', views.get_ga_real_time_data, name="real-time"),
    url(r'^data-info/', views.get_ga_time_based_data, name="data-info"),
    url(r'^google-auth/', views.google_auth, name="google-auth"),
]
