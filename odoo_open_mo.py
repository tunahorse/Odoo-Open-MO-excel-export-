#!/usr/bin/env python3

import pandas as pd
import xmlrpc.client
import ssl




try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = ""
db = ""
username = ""
password = ""

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})





sales_to_check_mo = []


orginal_sales_order = models.execute_kw(db, uid, password,
                                        'sale.order', 'search_read',
                                        [[['state', '!=', 'cancel'],
                                            ['state', '!=', 'draft']]],{'limit': 1})
for sales in orginal_sales_order:
    print(sales['name'])
    sales_to_check_mo.append(sales['name'])



sales_to_check_mo_no_duopes = list(set(sales_to_check_mo))

orders = []
products = []
qty = []



for each_order in sales_to_check_mo_no_duopes:

    check_mo = models.execute_kw(db, uid, password,
                                                       'mrp.production', 'search_read',
                                                       [[['origin', '=', str(each_order)],
                                                         '!',
                                                         ['state', '=', "cancel"], '!',
                                                         ['state', '=', "done"]]],
                                                       )
    if not check_mo:
        print('No MO record found')
    else:
        for mo in check_mo:
            print(mo)
            orders.append(mo['origin'])
            products.append(mo['product_id'][1])
            qty.append(mo['product_qty'])


df = pd.DataFrame()

df['Order Number'] = orders
df['Product'] = products
df['Remaining to make'] = qty


# Converting to excel
df.to_excel('Odoo_open_MO_to_make.xlsx', index=False)
