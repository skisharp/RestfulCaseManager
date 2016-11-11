# -*- coding: utf-8 -*-
from django.test import TestCase
import json


class ViewTestCase(TestCase):

    def test_index_view(self):
        response = self.client.get('/run_process_case?process_id=575e66b3fd7e741a6c21ca84&env=8030')

        content_json = json.loads(response.content)
        print '详细结果请看下面的url：'
        print content_json['result_url']

        self.assertEqual(response.status_code, 200)
