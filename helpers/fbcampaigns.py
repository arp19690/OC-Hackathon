import os

from facebookads import objects
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.api import FacebookAdsApi
from facebookads.objects import (
    Campaign,
)
from facebookads.session import FacebookSession

my_app_id = os.environ.get('FB_APP_ID')
my_app_secret = os.environ.get('FB_SECRET_KEY')
my_access_token = os.environ.get('FB_ACCESS_TOKEN')


def insights(start, end):
    response = {}
    try:
        my_session = FacebookSession(my_app_id, my_app_secret,
                                     my_access_token)
        my_api = FacebookAdsApi(my_session)
        FacebookAdsApi.set_default_api(my_api)
        me = objects.AdUser(fbid='me')
        my_accounts = list(me.get_ad_accounts())
        my_account = my_accounts[0]
        fields = [AdsInsights.Field.clicks, AdsInsights.Field.spend,
                  AdsInsights.Field.impressions,
                  AdsInsights.Field.unique_clicks,
                  AdsInsights.Field.cost_per_unique_click,
                  AdsInsights.Field.cost_per_inline_link_click]

        params = {'time_range': {'since': start, 'until': end}, }
        temp = my_account.get_insights(params=params, fields=fields)
        response = [{'field': 'Impressions', 'value': temp[0]['impressions']},
                    {'field': 'Cost', 'value': temp[0]['spend']},
                    {'field': 'Clicks', 'value': temp[0]['clicks']},
                    {'field': 'Unique Clicks', 'value': temp[0][
                        'unique_clicks']},
                    {'field': 'Cost per unique click', 'value': temp[0][
                        'cost_per_unique_click']}, {'field': 'Cost per Click',
                    'value': (float(temp[0]['spend']) / float(temp[0][
                                                              'clicks']))}]
    except:
        pass

    return response


def campaigns_with_insights(start, end):
    response = []
    try:
        my_session = FacebookSession(my_app_id, my_app_secret,
                                     my_access_token)
        my_api = FacebookAdsApi(my_session)
        FacebookAdsApi.set_default_api(my_api)
        me = objects.AdUser(fbid='me')
        my_accounts = list(me.get_ad_accounts())
        my_account = my_accounts[0]
        fields = [AdsInsights.Field.clicks, AdsInsights.Field.spend,
                  AdsInsights.Field.impressions,
                  AdsInsights.Field.unique_clicks,
                  AdsInsights.Field.cost_per_unique_click,
                  AdsInsights.Field.cost_per_inline_link_click]

        params = {'time_range': {'since': start, 'until': end},
                  'effective_status': ["ACTIVE"]}
        campaigns = my_account.get_campaigns(params=params,
                                             fields=[Campaign.Field.name,
                                                     Campaign.Field.status])
        headers = ["Name", 'Cost', "Impressions", "Clicks", "Unique Clicks",
                   "Cost per unique click", ]
        for i in campaigns:
            try:
                campaign = Campaign(i['id'])
                campaign_data = campaign.get_insights(
                    params=params, fields=fields)
                campaign_dict = {'id': i['id'], 'name': i['name'], 'Cost':
                    campaign_data[0]['spend'], "Clicks": campaign_data[0][
                    'clicks'], "Unique_Clicks": campaign_data[0][
                    'unique_clicks'], "Cost_per_unique_click":
                                     campaign_data[0][
                                         'cost_per_unique_click'],
                                 "Impressions":
                                     campaign_data[0]['impressions']}
                response.append(campaign_dict)
            except:
                pass
    except:
        pass
    return {'headers': headers, 'rows': response}
