# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.views.generic import TemplateView




urlpatterns = [

    ############################################## Homepage ##############################################
    path('', views.homepage, name='homepage'),
    path('requests_demo/', views.requests_demo, name='requests_demo'),
    re_path(r'^blog/', views.homepage_blog, name="blog"), # use regular expression for handle all pages /P*
    re_path(r'^Post_', views.homepage_blog_post_id, name="blog_post_id"), # use regular expression for handle all posts /Post_*
    re_path(r'^Post/', views.homepage_blog_post_name, name="blog_post_name"), # use regular expression for handle all posts /Post_*
    path('services/', views.homepage_services, name='services'),
    path('pricing/', views.homepage_pricing, name='pricing'),
    path('contact/', views.homepage_contact, name='contact'),
    path('overview/', views.homepage_overview, name='overview'),
    path('terms/', views.homepage_terms, name='terms'),
    path('privacy/', views.homepage_privacy, name='privacy'),
    
    # sitemap and robots
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots),


    ############################################## Client ################################################
    path('dashboard_client/', views.dashboard_client, name="dashboard_client"),
    path('dashboard_client_weekly/', views.dashboard_client_weekly, name="dashboard_client_weekly"),
    path('requests_new_bulk/', views.requests_new_bulk, name="requests_new_bulk"),
    re_path(r'^requests_new_bulk_data_confirm/', views.requests_new_bulk_data_confirm, name="requests_new_bulk_data_confirm"), # use regular expression for handle all pages /P*
    re_path(r'^requests_bulk_status_client/', views.requests_bulk_status_client, name="requests_bulk_status_client"), # use regular expression for handle all pages /P*
    re_path(r'^update_bulk_status_ajax_client/', views.update_bulk_status_ajax_client, name="update_bulk_status_ajax_client"), # use regular expression for handle all pages /P*
    re_path(r'^requests_single_client/', views.requests_single_client, name="requests_single_client"), # use regular expression for handle all pages /P*
    re_path(r'^requests_bulk_client/', views.requests_bulk_client, name="requests_bulk_client"), # use regular expression for handle all pages /P*
    path('plans_preview_client/', views.plans_preview_client, name="plans_preview_client"),
    re_path(r'transaction_submit/', views.transaction_submit, name="transaction_submit"),
    re_path(r'transaction_success/', views.transaction_success, name="transaction_success"),
    re_path(r'transaction_fail/', views.transaction_fail, name="transaction_fail"),
    re_path(r'transactions_client/', views.transactions_client, name="transactions_client"),
    re_path(r'bulk_export_csv/', views.export_bulk_csv, name="bulk_export"),
    re_path(r'bulk_export_xlsx/', views.export_bulk_xlsx, name="bulk_export"),
    re_path(r'invoice/', views.invoice, name="invoice"),
    re_path(r'invoice_pdf/', views.download_pdf_invoice, name="download_pdf_invoice"),
    re_path(r'^tickets_client/', views.tickets_client, name="tickets_client"), # use regular expression for handle all pages /P*
    path('new_ticket_client/', views.new_ticket_client, name="new_ticket_client"),
    re_path(r'^ticket_messages_client/', views.ticket_messages_client, name="ticket_messages_client"), # use regular expression for handle all pages /P*
    re_path(r'^new_message_client/', views.new_message_client, name="new_message_client"), # use regular expression for handle all pages /P*
    re_path(r'^delete_ticket/', views.delete_ticket, name="delete_ticket"), # use regular expression for handle all pages /P*
    re_path(r'^delete_message_client/', views.delete_message_client, name="delete_message_client"), # use regular expression for handle all pages /P*


    ############################################## Admin #################################################
    path('dashboard_admin/', views.dashboard_admin, name="dashboard_admin"),
    re_path(r'^userslist_admin/', views.userslist_admin, name='userslist_admin'), # use regular expression for handle all pages /P*
    re_path(r'^requests_bulk_status_admin/', views.requests_bulk_status_admin, name="requests_bulk_status_admin"), # use regular expression for handle all pages /P*
    re_path(r'^update_bulk_status_ajax_admin/', views.update_bulk_status_ajax_admin, name="update_bulk_status_ajax_admin"), # use regular expression for handle all pages /P*
    re_path(r'^requests_single_admin/', views.requests_single_admin, name="requests_single_admin"), # use regular expression for handle all pages /P*
    re_path(r'^requests_bulk_admin/', views.requests_bulk_admin, name="requests_bulk_admin"), # use regular expression for handle all pages /P*
    re_path(r'^requests_demo_admin/', views.requests_demo_admin, name="requests_demo_admin"), # use regular expression for handle all pages /P*
    re_path(r'^plans_admin/', views.plans_admin, name="plans_admin"), # use regular expression for handle all pages /P*
    path('plans_admin_new_plan/', views.plans_admin_new_plan, name="plans_admin_new_plan"),
    re_path(r'plans_admin_edit_plan/', views.plans_admin_edit_plan, name="plans_admin_edit_plan"),
    path('plans_preview_admin/', views.plans_preview_admin, name="plans_preview_admin"),
    re_path(r'transactions_admin/', views.transactions_admin, name="transactions_admin"),
    re_path(r'user_log_admin/', views.user_log_admin, name="user_log_admin"),
    re_path(r'^tickets_admin/', views.tickets_admin, name="tickets_admin"), # use regular expression for handle all pages /P*
    re_path(r'^ticket_messages_admin/', views.ticket_messages_admin, name="ticket_messages_admin"), # use regular expression for handle all pages /P*
    re_path(r'^new_message_admin/', views.new_message_admin, name="new_message_admin"), # use regular expression for handle all pages /P*
    re_path(r'^delete_message_admin/', views.delete_message_admin, name="delete_message_admin"), # use regular expression for handle all pages /P*
    path('new_ticket_admin/', views.new_ticket_admin, name="new_ticket_admin"),
    re_path(r'^blog_admin/', views.blog_admin, name="blog_admin"), # use regular expression for handle all pages /P*
    path('new_post_admin/', views.new_post_admin, name="new_post_admin"),
    re_path(r'^post_paragraph_admin/', views.post_paragraph_admin, name="post_paragraph_admin"), # use regular expression for handle all pages /P*
    re_path(r'^new_paragraph_admin/', views.new_paragraph_admin, name="new_paragraph_admin"), # use regular expression for handle all pages /P*
    re_path(r'^delete_post/', views.delete_post, name="delete_post"), # use regular expression for handle all pages /post_*
    re_path(r'^toggle_publish_status/', views.toggle_publish_status, name="toggle_publish_status"), # use regular expression for handle all pages /post_*
    re_path(r'^delete_paragraph_admin/', views.delete_paragraph_admin, name="delete_paragraph_admin"), # use regular expression for handle all pages /paragraph_*
    re_path(r'^edit_paragraph_admin/', views.edit_paragraph_admin, name="edit_paragraph_admin"), # use regular expression for handle all pages /paragraph_*
    re_path(r'^edit_post_title_admin/', views.edit_post_title_admin, name="edit_post_title_admin"), # use regular expression for handle all pages /post_*
    re_path(r'^edit_post_image_name_admin/', views.edit_post_image_name_admin, name="edit_post_image_name_admin"), # use regular expression for handle all pages /post_*
    re_path(r'^upload_post_image/', views.upload_post_image, name="upload_post_image"), # use regular expression for handle all pages /post_*
    re_path(r'^discounts_admin/', views.discounts_admin, name="discounts_admin"), # use regular expression for handle all pages /P*
    re_path(r'^toggle_publish_status_discount/', views.toggle_publish_status_discount, name="toggle_publish_status_discount"), # use regular expression for handle all pages /discount_*
    re_path(r'^delete_discount/', views.delete_discount, name="delete_discount"), # use regular expression for handle all pages /discount_*
    path('new_discount_admin/', views.new_discount_admin, name="new_discount_admin"),
    re_path(r'^delete_user_admin/user_', views.delete_user_admin, name="delete_user_admin"), # use regular expression for handle all pages /user_*


    ############################################## Match any html files ###################################
    re_path(r'^.*\.*', views.pages, name='pages'),

]
