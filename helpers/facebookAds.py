from facebookads.session import FacebookSession
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdUser, AdCampaign
import os

my_app_id = os.environ.get('FB_APP_ID')
my_app_secret = os.environ.get('FB_SECRET_KEY')
my_access_token = os.environ.get('FB_ACCESS_TOKEN')
my_session = FacebookSession(my_app_id, my_app_secret, my_access_token)
my_api = FacebookAdsApi(my_session)
FacebookAdsApi.set_default_api(my_api)

me = objects.AdUser(fbid='me')
my_accounts = list(me.get_ad_accounts())

my_account = my_accounts[1]

print(">>> Campaign Stats")
for campaign in my_account.get_ad_campaigns(fields=[AdCampaign.Field.name]):
    for stat in campaign.get_stats(fields=[
        'impressions',
        'clicks',
        'spent',
        'unique_clicks',
        'actions',
    ]):
        print(campaign[campaign.Field.name])
    for statfield in stat:
        print("\t%s:\t\t%s" % (statfield, stat[statfield]))
