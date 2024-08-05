from django.urls import re_path as path
from .views import (
    Logout,
    add_contact,
    campaign_view,
    delete_all_contacts,
    delete_contact,
    delete_smtp,
    login_view,
    create_user_view,
    dashboard_view,
    contact_view,
    contact_list,
    contact_create,
    preview_campaign,
    segment_detail,
    segment_create,
    delete_segment,
    SMTPPage,
    AddUpdateSMTP,
    send_campaign,
    test_smtp,
    settings_view,
    add_update_campaign,
)


urlpatterns = [
    path(r'^login/$', login_view, name='login'),
    path(r'^logout/$', Logout, name='logout'),
    path(r'^create_user/$', create_user_view, name='create_user'),
    path(r'^dashboard/$', dashboard_view, name='dashboard'),
    path(r'^$', dashboard_view, name='home'),
    path(r'^contacts/$', contact_view, name='contacts_page'),

    path(r'^manage-contacts/$', contact_list, name='manage-contacts'),
    path(r'^create-segment/$', segment_create, name='create-segment'),
    path(r'^upload-contacts/$', contact_create, name='upload-contacts'),
    path(r'^add-contact/$', add_contact, name='add-contact'),
    path(r'^delete-all/$', delete_all_contacts, name='delete_all_contacts'),
    path(r'^delete-contact/(?P<contact_id>[\w-]+)/$', delete_contact, name='delete_contact'),

    path(r'^segments/detail/(?P<pk>[\w-]+)/', segment_detail, name='segment-detail'),
    path(r'^delete-segment/(?P<segment_id>[\w-]+)/', delete_segment, name='segment-delete'),

    path(r'^smtp-list/$', SMTPPage, name='smtp'),
    path(r'^smtp/$', AddUpdateSMTP, name='add_smtp'),
    path(r'^smtp-test/$', test_smtp, name='test_smtp'),
    path(r'^delete-smtp/(?P<smtp_id>[\w-]+)/$', delete_smtp, name='delete_smtp'),

    path(r'^settings/$', settings_view, name='settings'),
    
    path(r'^campaigns/$', campaign_view, name='campaign_view'),
    path(r'^campaign/$', add_update_campaign, name='add_update_campaign'),
    path(r'^campaign/preview/(?P<campaign_id>[\w-]+)/$', preview_campaign, name='preview_campaign'),
    path(r'^campaign/send/(?P<campaign_id>[\w-]+)/$', send_campaign, name='send_campaign'),
]
