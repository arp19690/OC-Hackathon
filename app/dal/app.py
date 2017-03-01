from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def get_item_status_to_exclude():
    status_list = """'canceled',
                    'pending',
                    'pending_payment',
                    'preorder',
                    'zest_declined',
                    'zest_timeout'"""
    return status_list


def get_item_status_list():
    status_list = """'confirmed',
                       'InTransit',
                       'OutForDelivery',
                       'Delivered',
                       'initiate_reversepickup',
                       'return_received',
                       'reverse_pickup',
                       'readytoship',
                       'complete',
                       'returnreceived_rto',
                       'rto',
                       'redaytoship',
                       'Return Received - RTO',
                       'Initiate Reverse Pickup',
                       'Return Received Reverse Pickup'"""
    return status_list


def get_top_retail_customers(from_datetime, end_datetime, limit=10):
    sql = """select sfo.entity_id, customer_firstname, customer_lastname, customer_email, sum(sfo.grand_total) as total_order_amount, sum(sfo.shipping_amount) as total_shipping_cost, sum(sfo.total_qty_ordered) as total_qty from overcart.sales_flat_order as sfo
            left join overcart.sales_flat_order_payment as sfop on sfop.parent_id = sfo.entity_id
            left join overcart.`sales_flat_order_status_history` as sfosh on sfosh.`parent_id` = sfo.`entity_id`
            where sfop.method not in ('purchaseorder', 'free', 'banktransfer', 'checkmo') and sfosh.status IN (""" + get_item_status_list() + """) and sfo.customer_email is not NULL
            and sfosh.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            group by sfo.customer_email
            order by total_qty desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results


def get_top_products_sold(from_datetime, end_datetime, limit=10):
    sql = """select sfoi.item_id, sfoi.sku, sfoi.name, count(sfoi.item_id) as total_qty from overcart.`sales_flat_order` as sfo
            left join overcart.`sales_flat_order_item` as sfoi on sfoi.`order_id` = sfo.`entity_id`
            left join overcart.`sales_flat_order_status_history` as sfosh on sfosh.`parent_id` = sfo.`entity_id`
            where sfosh.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            and sfosh.status IN (""" + get_item_status_list() + """)
            group by sfoi.sku
            order by total_qty desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results


def get_top_customers_by_city(from_datetime, end_datetime, cities_str=None,
                              limit=10):
    where_str = """sfop.method not in ('purchaseorder', 'free', 'banktransfer', 'checkmo') and sfosh.status IN (""" + get_item_status_list() + """) and sfo.customer_email is not NULL
            and sfosh.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'"""
    if cities_str is not None:
        where_str += """ AND sfoa.city in (""" + str(cities_str) + """)"""

    sql = """select sfo.entity_id, customer_firstname, customer_lastname, customer_email, sum(sfo.grand_total) as total_order_amount, sum(sfo.shipping_amount) as total_shipping_cost, sum(sfo.total_qty_ordered) as total_qty , sfoa.city, sfoa.region
            from overcart.sales_flat_order as sfo
            left join overcart.sales_flat_order_payment as sfop on sfop.parent_id = sfo.entity_id
            left join overcart.`sales_flat_order_address` as sfoa on sfo.`billing_address_id` = sfoa.`entity_id`
            left join overcart.`sales_flat_order_status_history` as sfosh on sfosh.`parent_id` = sfo.`entity_id`
            where """ + str(where_str) + """
            group by sfo.customer_email
            order by total_qty desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results


def get_top_sellers(from_datetime, end_datetime, limit=10):
    sql = """select asm.`entity_id`, asm.seller_id, asm.seller_name, sum(sfo.grand_total) as total_amount
            from overcart.`sales_flat_order` as sfo
            left join overcart.`awa_serialcode_mysavedorder` as asm on asm.`orderid` = sfo.`entity_id`
            left join overcart.`sales_flat_order_status_history` as sfosh on sfosh.`parent_id` = sfo.`entity_id`
            where sfosh.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            and sfosh.status IN (""" + get_item_status_list() + """)
            group by asm.`seller_id`
            order by total_amount desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results


def get_orders_per_minutes(from_datetime, end_datetime,
                           current_minute_of_day):
    sql = """select count(entity_id) as total_orders from overcart.`sales_flat_order` as sfo
          where sfo.`created_at` between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """';"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    total_orders = results[0]["total_orders"]
    try:
        orders_per_minute = float(total_orders / current_minute_of_day)
    except:
        orders_per_minute = 0
    return orders_per_minute


def get_converted_orders(orders_list, from_datetime, end_datetime):
    if len(orders_list) > 0:
        orders_str = "'" + ("', '").join(orders_list) + "'"
        sql = """select distinct(increment_id) as order_ids from overcart.`sales_flat_order` WHERE increment_id IN (""" + orders_str + """) and `status` NOT IN (""" + str(
            get_item_status_to_exclude()) + """) AND created_at between '""" + str(
            from_datetime) + """' and '""" + str(end_datetime) + """';"""
        cursor = connection.cursor()
        cursor.execute(sql)
        results = dictfetchall(cursor)
        cursor.close()
        if len(results)>0:
            return results[0]["order_ids"]
        else:
            return []
    else:
        return []


def get_top_sale_data(from_datetime, end_datetime, limit=10):
    sql = """select product_id, product_name, count(distinct(email_id)) total_signups from overcart.redmi
            where product_id is not NULL and product_id != "" AND created_time between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            group by product_id
            order by total_signups desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results
