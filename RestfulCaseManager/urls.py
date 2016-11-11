"""RestfulCaseManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import patterns
from RestfulCaseManager import RequestHandler
from RestfulCaseManager import settings
from RestfulCaseManager.request_handles import *
'''
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
'''

urlpatterns = patterns("",
            (r'^$', homepage_handle.homepage),
            (r'^index', homepage_handle.homepage),
            (r'^addmodule/$', homepage_handle.add_module_html),
            (r'^manage', homepage_handle.manageCase),
            (r'^add_module_todb/$', homepage_handle.save_module_db),
            (r'^paramters_list', homepage_handle.paramtersListHtml),
            (r'^processflowhtml', homepage_handle.process_flow_html),

            (r'^copy_process_case', process_handle.copy_process_case),
            (r'^delete_process_case', process_handle.delete_process_case),
            (r'^run_process_case', process_handle.run_process_case),
            (r'^edit_process_case', process_handle.edit_process_case),
            (r'^show_result', process_handle.show_result),
            (r'^run_module_process', process_handle.run_module_process),
            (r'^show_module_process_result', process_handle.show_module_process_result),
            (r'^delete_process', process_handle.delete_process),
            (r'^add_oracle_case_html', process_handle.add_oracle_case_html),
            (r'^save_oracle_case', process_handle.save_oracle_case),
            (r'^edit_oracle_case', process_handle.edit_oracle_case),
            (r'^copy_process', process_handle.copy_process),

            (r'^addcase/$', manage_handle.addCase),
            (r'^executeCase', manage_handle.runCase),
            (r'^addcasehtml', manage_handle.add_case_html),
            (r'^delete', manage_handle.deletecase),
            (r'^copy?', manage_handle.copyCase),
            (r'^modify', manage_handle.modifyCase),
            (r'^updatecase/$', manage_handle.updateCase),
            (r'^export/$', manage_handle.exportCaseTofile),
            (r'^show_case_result', manage_handle.show_case_result),

            (r'^add_paramter/$', patamter.addParamterHtml),
            (r'^add_paramter_todb/$', patamter.addParameerToDB),

            (r'^addprocesshtml', process_handle.add_process_html),
            (r'^add_process_todb', process_handle.add_process_to_db),
            (r'^process_case_list', process_handle.process_case_list),
            (r'^add_process_case_html', process_handle.add_process_case_html),
            (r'^save_process_case', process_handle.save_process_case),
            (r'^save_order', process_handle.save_order),

            (r'^history_result', RequestHandler.historyResultHtml),
            (r'^caselog', RequestHandler.caseLog),
            (r'^testajax', RequestHandler.index),
            (r'^returnjson', RequestHandler.returnjson),
            (r'^zrx', RequestHandler.zrx),
)



