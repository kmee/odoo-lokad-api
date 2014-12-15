__author__ = 'mileo'


import oerplib
import csv
import base64
from io import StringIO, BytesIO

#oerp = oerplib.OERP('localhost', protocol='xmlrpc+ssl', port=443, version='7.0') # use this for https
oerp = oerplib.OERP('localhost', protocol='xmlrpc', port=8069, version='7.0')

all_dbs = oerp.db.list()


user = oerp.login('admin', 'admin', 'database')

product_ids = oerp.search('product.product', [('active', '=', True)])


def _export_item(ids):

        prod_obj = oerp.get('product.product')

        head = ['Id','LabelName','TagLabelCategory','TagSubcategory',
                        'ServiceLevel','LeadTime','StockOnHand','StockOnOrder','LotMultiplier']

        itemFile = BytesIO()

        with itemFile as tsvfile:
            spamwriter = csv.writer(tsvfile, delimiter='\t',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(head)
            for prod in oerp.browse('product.product', ids):
                delay = min_qty = 0
                for seller in prod.seller_ids:
                    delay = seller.delay
                    min_qty = seller.min_qty
                    break
                product = [prod.id,
                           prod.name.encode('utf8'),
#                           prod.categ_id.parent_id,
#                           prod.categ_id.id,
                          #prod.service_level,
                           #delay,
#                           prod.qty_available,
#                           prod.incoming_qty,
                           #min_qty or 0
                        ]
                spamwriter.writerow(product)

            return itemFile.getvalue()

result = _export_item(product_ids[:10])