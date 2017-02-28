from django.shortcuts import render
from helpers import googleAnalytics
from app.dal import app as appDAL

GA_WEBSITE_VIEW_ID = "ga:73399225"

# Create your views here.
def get_ga_real_time_data(request):
    website_data = googleAnalytics.get_realtime_active_users(
        GA_WEBSITE_VIEW_ID)
    total_users = website_data["totalsForAllResults"]["rt:activeUsers"]
    all_sources = website_data["rows"]

    top_retail_customers = appDAL.get_top_retail_customers(limit=10)

    data_context = {
        "website": {
            "total_users": total_users,
            "all_sources": all_sources,
        },
        "top_retail_customers":top_retail_customers
    }

    return render(request, "app/realtime-data.html", context=data_context)
