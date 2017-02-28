from django.shortcuts import render
from helpers import googleAnalytics
from app.dal import app as appDAL
from datetime import datetime

GA_WEBSITE_VIEW_ID = "ga:73399225"

# Create your views here.
def get_ga_real_time_data(request):
    website_data = googleAnalytics.get_realtime_active_users(
        GA_WEBSITE_VIEW_ID)
    total_users = website_data["totalsForAllResults"]["rt:activeUsers"]
    all_sources = website_data["rows"]

    from_datetime = "2017-01-01 00:00:00"
    end_datetime = "2017-01-02 00:00:00"
    top_retail_customers = appDAL.get_top_retail_customers(from_datetime,
                                                           end_datetime,
                                                           limit=10)
    top_products_delivered = appDAL.get_top_products_delivered(from_datetime,
                                                               end_datetime,
                                                               limit=10)
    top_customers_by_city = appDAL.get_top_customers_by_city(from_datetime,
                                                             end_datetime,
                                                             limit=10)
    top_sellers = appDAL.get_top_sellers(from_datetime,
                                         end_datetime,
                                         limit=10)

    orders_sold_per_minute = appDAL.get_orders_per_minutes(
        str(datetime.now().strftime("%Y-%m-%d")) + " 00:00:00",
        str(datetime.now().strftime("%Y-%m-%d %H:%M:%s")),
        float(datetime.now().hour * datetime.now().minute))

    data_context = {
        "website": {
            "total_users": total_users,
            "all_sources": all_sources,
        },
        "top_retail_customers": top_retail_customers,
        "top_products_delivered": top_products_delivered,
        "top_customers_by_city": top_customers_by_city,
        "top_sellers": top_sellers,
        "orders_sold_per_minute": orders_sold_per_minute,
    }

    return render(request, "app/realtime-data.html", context=data_context)
