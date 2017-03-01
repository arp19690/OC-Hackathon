#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse

from googleapiclient import sample_tools
from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)


def main(argv):
    argparser.add_argument('table_id', type=str,
                           help=(
                               'The table ID of the profile you wish to access. '
                               'Format is ga:xxx where xxx is your profile ID.'))
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'analytics', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics')

    # Try to make a request to the API. Print the results or handle errors.
    try:
        # results = get_api_query(service, flags.table_id).execute()
        # print_results(results)

        results = service.data().realtime().get(
            ids=argv[1],
            metrics='rt:activeUsers',
            dimensions='rt:medium').execute()
        totals = results.get('totalsForAllResults')["rt:activeUsers"]
        print(totals)
        print_rows(results)

    except TypeError as error:
        # Handle errors in constructing a query.
        print(('There was an error in constructing your query : %s' % error))

    except HttpError as error:
        # Handle API errors.
        print(('Arg, there was an API error : %s : %s' %
               (error.resp.status, error._get_reason())))

    except AccessTokenRefreshError:
        # Handle Auth errors.
        print('The credentials have been revoked or expired, please re-run '
              'the application to re-authorize')


def get_realtime_active_users(view_id):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        [view_id], 'analytics', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics')
    results = service.data().realtime().get(
        ids=view_id,
        metrics='rt:activeUsers',
        dimensions='rt:medium,rt:deviceCategory,rt:latitude,rt:longitude,rt:city').execute()
    return results


def get_pageviews(view_id, start_date, end_date, max_results=20):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        [view_id], 'analytics', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics')
    results = service.data().ga().get(
        ids=view_id,
        dimensions='ga:pageTitle,ga:pagePath',
        metrics='ga:pageviews,ga:uniquePageviews',
        start_date=start_date,
        end_date=end_date,
        sort='-ga:pageviews',
        max_results=max_results
    ).execute()
    return results


def get_insights(view_id, start_date, end_date, max_results=20):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        [view_id], 'analytics', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics')
    response = service.data().ga().get(
        ids=view_id,
        dimensions='ga:adGroup,ga:campaign',
        metrics='ga:impressions,ga:adClicks,ga:adCost',
        start_date=start_date,
        end_date=end_date,
        max_results=max_results
    ).execute()

    try:
        cost_per_click = float(
            response['totalsForAllResults']['ga:adCost']) / float(
            response['totalsForAllResults']['ga:adClicks'])
    except:
        cost_per_click = 0

    summary_details = [{'field': "Impression",
                        'value': response['totalsForAllResults'][
                            'ga:impressions']},
                       {'field': "Cost",
                        'value': response['totalsForAllResults'][
                            'ga:adCost']},
                       {'field': "Clicks",
                        'value': response['totalsForAllResults'][
                            'ga:adClicks']},
                       {'field': "Cost Per Click", 'value': cost_per_click}]

    headers = ["Campaign", "AdGroup", "Impressions", "Clicks", "Cost",
               "Cost Per Click"]
    rows_list = list()
    for i in response['rows']:
        try:
            cost_per_click = float(i[4])/float(i[3])
        except:
            cost_per_click = 0
        row_dict = {"Campaign": i[1],
                    'AdGroup': i[0],
                    "Impressions": i[2], "Clicks": i[3], "Cost": i[4],
                    "cost_per_click": cost_per_click}
        rows_list.append(row_dict)
    results = {
        'column_headers': headers,
        'rows': rows_list,
        'summary': summary_details
    }
    return results


def get_api_query(service, table_id):
    """Returns a query object to retrieve data from the Core Reporting API.
    Args:
      service: The service object built by the Google API Python client library.
      table_id: str The table ID form which to retrieve data.
    """

    return service.data().ga().get(
        ids=table_id,
        start_date='2012-01-01',
        end_date='2012-01-15',
        metrics='ga:visits',
        dimensions='ga:source,ga:keyword',
        sort='-ga:visits',
        filters='ga:medium==organic',
        start_index='1',
        max_results='25')


def print_results(results):
    """Prints all the results in the Core Reporting API Response.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print_report_info(results)
    print_pagination_info(results)
    print_profile_info(results)
    print_query(results)
    print_column_headers(results)
    print_totals_for_all_results(results)
    print_rows(results)


def print_report_info(results):
    """Prints general information about this report.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Report Infos:')
    print('Contains Sampled Data = %s' % results.get('containsSampledData'))
    print('Kind                  = %s' % results.get('kind'))
    print('ID                    = %s' % results.get('id'))
    print('Self Link             = %s' % results.get('selfLink'))
    print()


def print_pagination_info(results):
    """Prints common pagination details.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Pagination Infos:')
    print('Items per page = %s' % results.get('itemsPerPage'))
    print('Total Results  = %s' % results.get('totalResults'))

    # These only have values if other result pages exist.
    if results.get('previousLink'):
        print('Previous Link  = %s' % results.get('previousLink'))
    if results.get('nextLink'):
        print('Next Link      = %s' % results.get('nextLink'))
    print()


def print_profile_info(results):
    """Prints information about the profile.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Profile Infos:')
    info = results.get('profileInfo')
    print('Account Id      = %s' % info.get('accountId'))
    print('Web Property Id = %s' % info.get('webPropertyId'))
    print('Profile Id      = %s' % info.get('profileId'))
    print('Table Id        = %s' % info.get('tableId'))
    print('Profile Name    = %s' % info.get('profileName'))
    print()


def print_query(results):
    """The query returns the original report query as a dict.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Query Parameters:')
    query = results.get('query')
    for key, value in query.iteritems():
        print('%s = %s' % (key, value))
    print()


def print_column_headers(results):
    """Prints the information for each column.
    The main data from the API is returned as rows of data. The column
    headers describe the names and types of each column in rows.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Column Headers:')
    headers = results.get('columnHeaders')
    for header in headers:
        # Print Dimension or Metric name.
        print('\t%s name:    = %s' % (header.get('columnType').title(),
                                      header.get('name')))
        print('\tColumn Type = %s' % header.get('columnType'))
        print('\tData Type   = %s' % header.get('dataType'))
        print()


def print_totals_for_all_results(results):
    """Prints the total metric value for all pages the query matched.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Total Metrics For All Results:')
    print('This query returned %s rows.' % len(results.get('rows')))
    print(('But the query matched %s total results.' %
           results.get('totalResults')))
    print('Here are the metric totals for the matched total results.')
    totals = results.get('totalsForAllResults')

    for metric_name, metric_total in totals.items():
        print('Metric Name  = %s' % metric_name)
        print('Metric Total = %s' % metric_total)
        print()


def print_rows(results):
    """Prints all the rows of data returned by the API.
    Args:
      results: The response returned from the Core Reporting API.
    """

    print('Rows:')
    if results.get('rows', []):
        for row in results.get('rows'):
            print('\t'.join(row))
    else:
        print('No Rows Found')


# if __name__ == '__main__':
#     main(sys.argv)

def get_orders_by_campaigns(view_id, start_date, end_date, type="google"):
    # Authenticate and construct service.
    if type == "google":
        filters = 'ga:source==google,ga:medium==cpc'
    else:
        filters = 'ga:source==facebook'
    service, flags = sample_tools.init(
        [view_id], 'analytics', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics')
    response = service.data().ga().get(
        ids=view_id,
        dimensions='ga:campaign,ga:transactionId,ga:medium,ga:source',
        metrics='ga:transactions',
        start_date=start_date,
        end_date=end_date,
        filters=filters
    ).execute()

    orders_dict = dict()
    campaigns_list = list()

    for i in response['rows']:
        campaigns_list.append(i[0])
    campaigns_list = list(set(campaigns_list))
    for m in campaigns_list:
        orders_dict[m] = []

    for i in response['rows']:
        orders_dict[i[0]].append(i[1])
    return orders_dict
