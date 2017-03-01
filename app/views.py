from datetime import datetime

from django.shortcuts import render
from app.dal import app as appDAL
from helpers import googleAnalytics
from helpers import fbcampaigns
from django.contrib.auth.decorators import login_required
from django.conf import settings

GA_WEBSITE_VIEW_ID = "ga:73399225"
GA_APP_VIEW_ID = "ga:132813188"

# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def get_ga_real_time_data(request):
    website_data = googleAnalytics.get_realtime_active_users(
        GA_WEBSITE_VIEW_ID)
    ga_app_data = googleAnalytics.get_realtime_active_users(GA_APP_VIEW_ID)

    total_website_users = website_data["totalsForAllResults"]["rt:activeUsers"]
    website_geo_points = list()
    all_website_sources = list()
    if len(website_data["rows"]) > 0:
        for tmpdata in website_data["rows"]:
            if tmpdata[2] != '0.000000' and tmpdata[3] != '0.000000':
                website_geo_points.append({
                    "geo_coords": [tmpdata[2], tmpdata[3]],
                    "city_name": tmpdata[4],
                    "count": tmpdata[5]
                })
            tmpdict = {"device": tmpdata[1],
                       "data": {
                           "source": tmpdata[0],
                           "latitude": tmpdata[2],
                           "longitude": tmpdata[3],
                           "city_name": tmpdata[4],
                           "count": tmpdata[5]
                       }}
            all_website_sources.append(tmpdict)

    total_app_users = ga_app_data["totalsForAllResults"]["rt:activeUsers"]
    app_geo_points = list()
    all_app_sources = list()
    if len(ga_app_data["rows"]) > 0:
        for tmpdata in ga_app_data["rows"]:
            if tmpdata[2] != '0.000000' and tmpdata[3] != '0.000000':
                app_geo_points.append({
                    "geo_coords": [tmpdata[2], tmpdata[3]],
                    "city_name": tmpdata[4],
                    "count": tmpdata[5]
                })
            tmpdict = {"device": tmpdata[1],
                       "data": {
                           "source": tmpdata[0],
                           "latitude": tmpdata[2],
                           "longitude": tmpdata[3],
                           "city_name": tmpdata[4],
                           "count": tmpdata[5]
                       }}
            all_app_sources.append(tmpdict)

    top_website_page_views = googleAnalytics.get_pageviews(GA_WEBSITE_VIEW_ID,
                                                           datetime.now().strftime(
                                                               "%Y-%m-%d"),
                                                           datetime.now().strftime(
                                                               "%Y-%m-%d"))

    # top_app_page_views = googleAnalytics.get_pageviews(GA_APP_VIEW_ID,
    #                                                    datetime.now().strftime(
    #                                                        "%Y-%m-%d"),
    #                                                    datetime.now().strftime(
    #                                                        "%Y-%m-%d"))

    orders_sold_per_minute = appDAL.get_orders_per_minutes(
        str(datetime.now().strftime("%Y-%m-%d")) + " 00:00:00",
        str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        float(datetime.now().hour * datetime.now().minute))

    data_context = {
        "website": {
            "total_users": total_website_users,
            "all_sources": all_website_sources,
            "top_page_views": top_website_page_views,
            "geo_points": website_geo_points,
        },
        "app": {
            "total_users": total_app_users,
            "all_sources": all_app_sources,
            # "top_page_views": top_app_page_views,
            "geo_points": app_geo_points,
        },
        "orders_sold_per_minute": orders_sold_per_minute,
    }

    return render(request, "app/realtime-data.html", context=data_context)


@login_required(login_url=settings.LOGIN_URL)
def get_ga_time_based_data(request):
    data_context = dict()
    if "range" in request.GET:
        datetime_range = request.GET.get("range", None).split(" - ")
        from_datetime = str(datetime.strptime(datetime_range[0].strip(),
                                              "%Y-%m-%d %H:%M %p").strftime(
            "%Y-%m-%d %H:%M:%S"))
        end_datetime = str(datetime.strptime(datetime_range[1].strip(),
                                             "%Y-%m-%d %H:%M %p").strftime(
            "%Y-%m-%d %H:%M:%S"))

        # fetching info now
        top_website_page_views = googleAnalytics.get_pageviews(
            GA_WEBSITE_VIEW_ID,
            datetime.now().strftime(
                "%Y-%m-%d"),
            datetime.now().strftime(
                "%Y-%m-%d"))
        google_analytics_website = googleAnalytics.get_insights(
            GA_WEBSITE_VIEW_ID,
            from_datetime[:10],
            end_datetime[:10])
        facebook_ads_data = fbcampaigns.insights(from_datetime[:10],
                                                 end_datetime[:10])
        facebook_campaigns_data = fbcampaigns.campaigns_with_insights(
            from_datetime[:10], end_datetime[:10])
        top_retail_customers = appDAL.get_top_retail_customers(
            from_datetime,
            end_datetime,
            limit=10)
        top_products_sold = appDAL.get_top_products_sold(
            from_datetime,
            end_datetime,
            limit=10)
        top_customers_by_city = appDAL.get_top_customers_by_city(
            from_datetime,
            end_datetime,
            limit=10)
        top_sellers = appDAL.get_top_sellers(from_datetime,
                                             end_datetime,
                                             limit=10)
        top_sale_info = appDAL.get_top_sale_data(from_datetime,
                                                 end_datetime,
                                                 limit=10)

        website_orders_by_campaigns = googleAnalytics.get_orders_by_campaigns(
            GA_WEBSITE_VIEW_ID, from_datetime[:10], end_datetime[:10],
            type="google")

        orders_sold_per_minute = appDAL.get_orders_per_minutes(
            str(datetime.now().strftime("%Y-%m-%d")) + " 00:00:00",
            str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            float(datetime.now().hour * datetime.now().minute))

        data_context = {"data": {
            "top_retail_customers": top_retail_customers,
            "top_products_sold": top_products_sold,
            "top_customers_by_city": top_customers_by_city,
            "top_sellers": top_sellers,
            "orders_sold_per_minute": orders_sold_per_minute,
            "top_website_page_views": top_website_page_views,
            "google_analytics_website": google_analytics_website,
            "facebook_ads_data": facebook_ads_data,
            "facebook_campaigns_data": facebook_campaigns_data,
            "top_sale_info": top_sale_info
        }
        }

    return render(request, "app/data-info.html", context=data_context)
