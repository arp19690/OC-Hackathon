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
        response = {'impressions': temp[0]['impressions'],
                    'spend': temp[0]['spend'], 'clicks': temp[0]['clicks'],
                    'unique_clicks': temp[0]['unique_clicks'],
                    'cost_per_unique_click': temp[0][
                        'cost_per_unique_click'], }
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

        params = {'time_range': {'since': start, 'until': end}, }
        for i in my_account.get_campaigns(params=params,
                                          fields=[Campaign.Field.name,
                                                  Campaign.Field.status]):
            if i['status'] == "ACTIVE":
                campaign_dict = {'id': i['id'], 'name': i['name']
                                 }
                campaign = Campaign(i['id'])
                campaign_dict['campaign_data'] = list(campaign.get_insights(
                    params=params, fields=fields))
                response.append(campaign_dict)
    except:
        pass
    return response
