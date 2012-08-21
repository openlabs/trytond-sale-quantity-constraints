# -*- coding: UTF-8 -*-
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

{
    'name': 'Sale Quantity Constraints',
    'description': '''
        Check the quantity of the product while creating sale lines
        and apply specific contraints based on
            * Minimum Order Quantity
            * Order Quantity Multiple
            * Maximum Order Quantity
    ''',
    'version': '2.4.0.1',
    'author': 'Openlabs Technologies & Consulting (P) LTD',
    'email': 'info@openlabs.co.in',
    'website': 'http://www.openlabs.co.in/',
    'depends': [
        'sale',
    ],
    'xml': [
       'product.xml',
    ],
    'translation': [
    ],
}
