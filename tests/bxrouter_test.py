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
-JobApiRouter(prefix=appJob)
/appJob/registerPush?deviceToken=(c=新的信鸽绑定):get
/appJob/index(c=企业信息-获取主界面信息):get
/appJob/companytype(c=企业信息-行业分类):get
/appJob/companyInfo(c=企业信息-信息):get
/appJob/companyInfoUpdate(params,c=企业信息-增加/更新信息):post
/appJob/companyauthConfirm(params,c=企业信息-申请认证):post
/appJob/jobCategory(c=兼职-分类,group=job):get
/appJob/jobTag(params,c=兼职-标签,group=job):get
/appJob/jobCheckout(c=兼职-结算方式,group=job):post
/appJob/jobupdate(params,c=兼职-新增/更新信息,group=job):get
/appJob/jobList(params,c=兼职-列表,group=job):get
/appJob/joboffline(params,c=兼职-申请下线,group=job):post
/appJob/jobDetail?job_id=(c=兼职-详情,group=job):get
/appJob/jobapplyStatus?job_id=(c=求职管理-状态,,group=jobApply):get
/appJob/jobapplyList(params,c=求职管理-列表,,group=jobApply):get
/appJob/jobapplyUpdate(params,c=求职管理-更新申请者信息,,group=jobApply):get
/appJob/jobuserDetail(params,c=求职管理-详情,group=jobUser):get
/appJob/jobuserList(params,c=人才管理-列表,group=jobUser):get
/appJob/jobapplyinvitation(params,c=人才管理-人才邀请,group=JobApplyInvitation):get
/appJob/jobapplyinvitationList(params,c=人才管理-邀请列表,group=JobApplyInvitation):get
/appJob/jobjoinList(params,c=工资结算-列表,group=JobJoin):get
/appJob/jobjoinPay(params,c=工资结算-兼职结算,group=JobJoin):post
        ''')
        sys.stdin = strio
        bxrouter.main('api_service')


if __name__ == '__main__':
    unittest.main()
