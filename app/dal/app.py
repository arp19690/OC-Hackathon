from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def get_top_retail_customers(from_datetime, end_datetime, limit=10):
    sql = """select sfo.entity_id, customer_firstname, customer_lastname, customer_email, sum(sfo.grand_total) as total_order_amount, sum(sfo.shipping_amount) as total_shipping_cost, sum(sfo.total_qty_ordered) as total_qty from overcart.sales_flat_order as sfo
            left join overcart.sales_flat_order_payment as sfop on sfop.parent_id = sfo.entity_id
            where sfop.method not in ('purchaseorder', 'free', 'banktransfer', 'checkmo') and sfo.status = 'delivered' and sfo.customer_email is not NULL
            and sfo.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            group by sfo.customer_email
            order by total_qty desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results


def get_top_products_delivered(from_datetime, end_datetime, limit=10):
    sql = """select sfoi.item_id, sfoi.sku, sfoi.name, count(sfoi.item_id) as total_qty from overcart.`sales_flat_order` as sfo
            left join overcart.`sales_flat_order_item` as sfoi on sfoi.`order_id` = sfo.`entity_id`
            where sfo.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            and sfo.status = 'delivered'
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
    where_str = """sfop.method not in ('purchaseorder', 'free', 'banktransfer', 'checkmo') and sfo.status = 'delivered' and sfo.customer_email is not NULL
            and sfo.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'"""
    if cities_str is not None:
        where_str += """ AND sfoa.city in (""" + str(cities_str) + """)"""

    sql = """select sfo.entity_id, customer_firstname, customer_lastname, customer_email, sum(sfo.grand_total) as total_order_amount, sum(sfo.shipping_amount) as total_shipping_cost, sum(sfo.total_qty_ordered) as total_qty , sfoa.city, sfoa.region
            from overcart.sales_flat_order as sfo
            left join overcart.sales_flat_order_payment as sfop on sfop.parent_id = sfo.entity_id
            left join overcart.`sales_flat_order_address` as sfoa on sfo.`billing_address_id` = sfoa.`entity_id`
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
            where sfo.created_at between '""" + str(
        from_datetime) + """' and '""" + str(end_datetime) + """'
            and sfo.status = 'delivered'
            group by asm.`seller_id`
            order by total_amount desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results
