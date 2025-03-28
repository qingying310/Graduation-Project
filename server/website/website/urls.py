#
# OtterTune - urls.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#
import debug_toolbar
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache

from website import settings
from website import views as website_views


admin.autodiscover()

# pylint: disable=line-too-long,invalid-name
urlpatterns = [
    # URLs for user registration & login
    url(r'^signup/', website_views.signup_view, name='signup'),
    url(r'^login/', website_views.login_view, name='login'),
    url(r'^logout/$', website_views.logout_view, name='logout'),
    url(r'^change_password/', website_views.change_password_view, name='change_password'),

    # URLs for project views
    url(r'^$', website_views.redirect_home),
    url(r'^projects/$', website_views.home_projects_view, name='home_projects'),
    url(r'^projects/new/$', website_views.create_or_edit_project, name='new_project'),
    url(r'^projects/(?P<project_id>[0-9]+)/edit/$', website_views.create_or_edit_project, name='edit_project'),
    url(r'^projects/delete/$', website_views.delete_project, name="delete_project"),

    # URLs for session views
    url(r'^projects/(?P<project_id>[0-9]+)/sessions$', website_views.project_sessions_view, name='project_sessions'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/$', website_views.session_view, name='session'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/new/$', website_views.create_or_edit_session, name='new_session'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/edit/$', website_views.create_or_edit_session, name='edit_session'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/editKnobs/$', website_views.edit_knobs, name='edit_knobs'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/delete/$', website_views.delete_session, name='delete_session'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/dump/$', website_views.download_debug_info, name='dump_debug_data'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/dump_objectives/$', website_views.download_objectives, name='dump_objectives'),

    # URLs for result views
    url(r'^new_result/', website_views.new_result, name='new_result'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/results/(?P<result_id>[0-9]+)/$', website_views.result_view, name='result'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/workloads/(?P<wkld_id>[0-9]+)/$', website_views.workload_view, name='workload'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/knobs/(?P<data_id>[0-9]+)/$', website_views.knob_data_view, name='knob_data'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/metrics/(?P<data_id>[0-9]+)/$', website_views.metric_data_view, name='metric_data'),
    url(r'^projects/(?P<project_id>[0-9]+)/sessions/(?P<session_id>[0-9]+)/results/(?P<result_id>[0-9]+)/status$', website_views.tuner_status_view, name="tuner_status"),

    # URLs for the DBMS knob & metric reference pages
    url(r'^ref/(?P<dbms_name>.+)/(?P<version>.+)/knobs/(?P<knob_name>.+)/$', website_views.dbms_knobs_reference, name="dbms_knobs_ref"),
    url(r'^ref/(?P<dbms_name>.+)/(?P<version>.+)/metrics/(?P<metric_name>.+)/$', website_views.dbms_metrics_reference, name="dbms_metrics_ref"),

    # URLs to the helper functions called by the javascript code
    url(r'^get_workload_data/', website_views.get_workload_data),
    url(r'^get_data/', website_views.get_timeline_data),
    url(r'^get_result_data_file/', website_views.download_next_config),

    # Admin URLs
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),

    # Static URL
    url(r'^static/(?P<path>.*)$', never_cache(serve)),

    # Back door
    url(r'^query_and_get/(?P<upload_code>[0-9a-zA-Z]+)$', website_views.give_result, name="backdoor"),
    url(r'^dump/(?P<upload_code>[0-9a-zA-Z]+)', website_views.get_debug_info, name="backdoor_debug"),
    url(r'^create/project/', website_views.alt_create_or_edit_project, name='backdoor_create_project'),
    url(r'^edit/project/', website_views.alt_create_or_edit_project, name='backdoor_edit_project'),
    url(r'^create/session/', website_views.alt_create_or_edit_session, name='backdoor_create_session'),
    url(r'^edit/session/', website_views.alt_create_or_edit_session, name='backdoor_edit_session'),
    url(r'^create/user/', website_views.alt_create_user, name='backdoor_create_user'),
    url(r'^delete/user/', website_views.alt_delete_user, name='backdoor_delete_user'),
    url(r'^info/(?P<name>[0-9a-zA-Z]+)', website_views.alt_get_info, name="backdoor_info"),

    # train ddpg with results in the given session
    url(r'^train_ddpg/sessions/(?P<session_id>[0-9]+)$', website_views.train_ddpg_loops, name='train_ddpg_loops'),

    # Test
    url(r'^test/create/', website_views.create_test_website, name='create_test_website'),
    url(r'^test/pipeline/', website_views.pipeline_data_ready, name='pipeline_data_ready'),
    url(r'^test/task_status/(?P<upload_code>[0-9a-zA-Z]+)$', website_views.tuner_status_test, name="tuner_status_test"),

    # Pipeline data
    url(r'^pipeline/data/(?P<pipeline_id>[0-9]+)', website_views.pipeline_data_view, name='pipeline_data_view')
]

if settings.DEBUG:
    urlpatterns.insert(0, url(r'^__debug__/', include(debug_toolbar.urls)))
