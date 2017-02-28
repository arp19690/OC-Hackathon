from django.shortcuts import render
from helpers import googleAnalytics

# Create your views here.
def get_ga_real_time_data(request):
    data = googleAnalytics.get_realtime_active_users("ga:73399225")
    total_users = data["totalsForAllResults"]["rt:activeUsers"]
    all_sources = data["rows"]

    data_context={
        "total_users":total_users,
        "all_sources":all_sources,
    }

    return render(request, "app/realtime-data.html",context=data_context)
