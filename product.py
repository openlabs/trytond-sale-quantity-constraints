# -*- coding: utf-8 -*-
"""
    product

    Sale Quantity Constraints

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
from trytond.model import Workflow, ModelView, ModelSQL, fields


class Product(ModelSQL, ModelView):
    "Product"
    _name = 'product.product'

    order_minimum = fields.Float('Minimum Quantity')
    order_multiple = fields.Float('Quantity Multiple')
    order_maximum = fields.Float('Maximum Quantity')

    def default_order_minimum(self):
        return 1.0

    def default_order_multiple(self):
        return 1.0

    def default_order_maximum(self):
        return 100.0

Product()


class Sale(Workflow, ModelSQL, ModelView):
    "Sale"
    _name = 'sale.sale'

    qty_strict_check = fields.Boolean('Ensure Strict Quantity Check')

    def default_qty_strict_check(self):
        return True

Sale()


class SaleLine(ModelSQL, ModelView):
    'Sale Line'
    _name = 'sale.line'

    def __init__(self):
        super(SaleLine, self).__init__()
        self._constraints += [
            ('check_qty_minimum', 'wrong_mimimum'),
            ('check_qty_multiple', 'wrong_multiple'),
            ('check_qty_maximum', 'wrong_maximum')
        ]
        self._error_messages.update({
            'wrong_minimum': 'Minimum Order Quantity for Product %s is %s %s',
            'wrong_multiple': \
                'Order Quantity for Product %s must be a multiple of %s',
            'wrong_maximum': 'Maximum Order Quantity for Product %s is %s %s'
        })

    def check_qty_minimum(self, ids):
        """Make sure the ordered quantity is more than the minimum
            qunantity specified in the corresponding product
        """
        for line in self.browse(ids):
            if not line.sale.qty_strict_check:
                return True
            if line.quantity and line.product and line.product.order_minimum \
                    and line.quantity < line.product.order_minimum:
                self.raise_user_error('wrong_minimum', error_args=(
                    line.product.name, line.product.order_minimum,
                    line.product.sale_uom.name
                ))
        return True

    def check_qty_multiple(self, ids):
        """Make sure the ordered quantity is a multiple of the multiple
            qunantity specified in the corresponding product
        """
        for line in self.browse(ids):
            if not line.sale.qty_strict_check:
                return True
            if line.quantity and line.product and line.product.order_multiple \
                    and (line.quantity % line.product.order_multiple != 0):
                self.raise_user_error('wrong_multiple', error_args=(
                    line.product.name, line.product.order_multiple
                ))
        return True

    def check_qty_maximum(self, ids):
        """Make sure the ordered quantity is less than the maximum
            qunantity specified in the corresponding product
        """
        for line in self.browse(ids):
            if not line.sale.qty_strict_check:
                return True
            if line.quantity and line.product and line.product.order_maximum \
                    and line.quantity > line.product.order_maximum:
                self.raise_user_error('wrong_maximum', error_args=(
                    line.product.name, line.product.order_maximum,
                    line.product.sale_uom.name
                ))
        return True

SaleLine()
