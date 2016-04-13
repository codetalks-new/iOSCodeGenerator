#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import unittest

import os
import sys
sys.path.insert(0, os.path.basename('..'))

from ios_code_generator import bxrouter
from StringIO import StringIO


class MyTestCase(unittest.TestCase):
    def test_bxrouter(self):
        strio = StringIO(u"""
-ApiRouter(prefix=api/appShop)
 /api/appShop/registerPush?deviceToken=
 /api/appShop/index
        """)
        sys.stdin = strio
        bxrouter.main()

    def test_bxrouter2(self):
        strio = StringIO( u' -JobApiRouter(prefix=appJob)\n /appJob/companyInfoUpdate(params,c=中文-结构):post')
        sys.stdin = strio
        bxrouter.main()

    def test_bxapiService(self):
        strio = StringIO(u'''
-ApiRouter(prefix=api/appShop)
/api/appShop/registerPush?deviceToken=
/api/appShop/index
/api/appShop/shopInfo
/api/appShop/shopInfoUpdate?p1=&p2=:p
/api/appShop/shopStatus?status=:p
/api/appShop/shopCard?type=
/api/appShop/shopType
/api/appShop/setTradePassword?p1=&p2=
/api/appShop/goodsFirstCategory
/api/appShop/categoryList
/api/appShop/goodsSecondCategory?id=
/api/appShop/supplierList
/api/appShop/supplierInfo?id=
/api/appShop/goodsList?category_id=&limit=&supplier_id=
/api/appShop/goodsInfo?goods_id=&supplier_id=
/api/appShop/supplierCartUpdate?id=&supplier_id=&goods_id=
/api/appShop/supplierCartView?type=
/api/appShop/supplierCartConfirm?p1=&p2=:p
/api/appShop/supplierShopOrderStatus
/api/appShop/supplierShopOrderList?type=1&limit=2&search=
/api/appShop/supplierShopOrderDetail?order_id=2666
/api/appShop/supplierShopOrderPay?order_id=&pay_type=
/api/appShop/supplierShopOrderClose?order_id=
/api/appShop/supplierShopOrderRefund?order_id=556
/api/appShop/supplierShopOrderRefundConfirm?order_id=&reason=:p
/api/appShop/supplierShopOrderReceive?order_id=22
/api/appShop/goods?type=1
/api/appShop/goodsUpdate?goods_id=&status=:p
/api/appShop/goodsDetail?goods_id=12
/api/appShop/goodsLoss?goods_id=12&quantity=1
/api/appShop/orderStatus
/api/appShop/orderList?type=1&limit=0&search=
/api/appShop/orderDelivery?order_id=12
/api/appShop/orderDetail?order_id=16968
/api/appShop/orderCancelConfirm?order_id=12&status=0
/api/appShop/orderReceive?order_id=0
/api/appShop/buildingMasterInfo
/appShop/customerInfo?uid=
/api/appShop/commentList?status=
api/appShop/commentReply?order_id=&goods_id=&reply:p
/api/appShop/goodsSearch?search=
/api/appShop/advertisement?type=
        ''')
        sys.stdin = strio
        bxrouter.main('api_service')


if __name__ == '__main__':
    unittest.main()
