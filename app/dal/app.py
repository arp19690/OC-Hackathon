from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def get_top_retail_customers(limit=10):
    sql = """select sfo.entity_id, customer_firstname, customer_lastname, customer_email, sum(sfo.grand_total) as total_order_amount, sum(sfo.shipping_amount) as total_shipping_cost, sum(sfo.total_qty_ordered) as total_qty from overcart.sales_flat_order as sfo
            left join overcart.sales_flat_order_payment as sfop on sfop.parent_id = sfo.entity_id
            where sfop.method not in ('purchaseorder', 'free', 'banktransfer', 'checkmo') and sfo.status = 'delivered' and sfo.customer_email is not NULL
            group by sfo.customer_email
            order by total_qty desc
            limit """ + str(limit) + """;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dictfetchall(cursor)
    cursor.close()
    return results
