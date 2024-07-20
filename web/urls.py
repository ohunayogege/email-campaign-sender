from django.urls import re_path as path
from . views import (
    add_smtp_configuration,
    campaign_create,
    campaign_delete,
    campaign_list,
    campaign_update,
    dashboard,
    delete_all_subscribers,
    delete_smtp_configuration,
    import_subscribers,
    message_log_list,
    redirect_order,
    redirect_short_url,
    send_campaign,
    smtp_list,
    subscriber_list,
    test_smtp_configuration
)

urlpatterns = [
    path(r"^$", dashboard, name="dashboard"),

    path(r'^smtp-configurations/$', smtp_list, name='smtp_list'),
    path(r'^smtp-configurations/add/$', add_smtp_configuration, name='add_smtp_configuration'),
    path(r'^smtp-configurations/delete/(?P<smtp_id>\d+)/$', delete_smtp_configuration, name='delete_smtp_configuration'),
    path(r'^smtp-configurations/test/$', test_smtp_configuration, name='test_smtp_configuration'),

    path(r'^import-subscribers/$', import_subscribers, name='import_subscribers'),
    path(r'^subscribers/$', subscriber_list, name='subscriber_list'),
    path(r'^message-log/$', message_log_list, name='message_log_list'),
    path(r'^delete-all-subscribers/$', delete_all_subscribers, name='delete_all_subscribers'),

    path(r'^campaigns/$', campaign_list, name='campaign_list'),
    path(r'^campaigns/create/$', campaign_create, name='campaign_create'),
    path(r'^campaigns/update/(?P<pk>\d+)/$', campaign_update, name='campaign_update'),
    path(r'^campaigns/delete/(?P<pk>\d+)/$', campaign_delete, name='campaign_delete'),
    path(r'^campaigns/send/(?P<pk>\d+)/$', send_campaign, name='send_campaign'),


    path(r'^redirect/order/(?P<token>\w+)$', redirect_order, name='redirect_order'),
    path(r'^s/(?P<short_code>\w+)/$', redirect_short_url, name='redirect_short_url'),
]
