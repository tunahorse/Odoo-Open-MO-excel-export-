# Odoo Open MO execel export

Because it should be easy to see whats left to make 

## Packages Needed


```python
import pandas as pd
import xmlrpc.client
import ssl
```

## Usage

```python
# Add you login info
url = ""
db = ""
username = ""
password = ""

# Filter your sales, in this case only actives ones are selected. 
orginal_sales_order = models.execute_kw(db, uid, password,
                                        'sale.order', 'search_read',
                                        [[['state', '!=', 'cancel'],
                                            ['state', '!=', 'draft']]])
```
## Excel sheet is made with Sales#, product, and QTY. 
