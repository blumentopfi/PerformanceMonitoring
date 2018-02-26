from django.urls import path
from . import views
from django.conf.urls import url, include
from .views import ModelList,ModelDetail,ModelExperimentList,ModelTimerList
from .views import ExperimentList,ExperimentDetail,ExperimentJobList
from .views import JobList,JobDetail,JobJobRankList,JobTimingsList
from .views import JobRankDetail,JobRankList
from .views import TimerDetail,TimerList,TimerTimingsList
from .views import TimingDetail,TimingList
from django.views.generic import TemplateView
import PerformanceMonitoring.utils as u
import h5py
import logging
model_urls = [
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)/experiments$', ModelExperimentList.as_view(), name='model_experiments'),
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)/timers$', ModelTimerList.as_view(), name='model_timers'),
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)$', ModelDetail.as_view(), name='model-detail'),
    url(r'^$', ModelList.as_view(), name='model-list')
]
experiment_urls = [
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)/jobs$', ExperimentJobList.as_view(), name='experiment_jobs'),
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)$', ExperimentDetail.as_view(), name='experiment-detail'),
    url(r'^$', ExperimentList.as_view(), name='experiment-list')
]
job_urls = [
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)/jobranks$', JobJobRankList.as_view(), name='job_jobranks'),
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)/timings$', JobTimingsList.as_view(), name='job_timings'),
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)$', JobDetail.as_view(), name='job-detail'),
    url(r'^$', JobList.as_view(), name='job-list')
]
jobranks_urls = [
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)$', JobRankDetail.as_view(), name='job_rank-detail'),
    url(r'^$', JobRankList.as_view(), name='job_rank-list')
]
timer_urls = [
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)/timings$', TimerTimingsList.as_view(), name='timer_timings'),
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)$', TimerDetail.as_view(), name='timer-details'),
    url(r'^$', TimerList.as_view(), name='timer-list')
]
timings_urls = [
    url(r'^(?P<pk>[0-9a-zA-Z_-]+)$', TimingDetail.as_view(), name='timing-details'),
    url(r'^$', TimingList.as_view(), name='timing-list')
]
api_urls = [
    url(r'^models/', include(model_urls)),
    url(r'^experiments/', include(experiment_urls)),
    url(r'^jobs/', include(job_urls)),
    url(r'^jobranks/', include(jobranks_urls)),
    url(r'^timer/', include(timer_urls)),
    url(r'^timings/', include(timings_urls)),
]

doc_urls=[
url(r'^timer',TemplateView.as_view(template_name='docs/timerDoc.html'), name='timer-doc-view'),
url(r'^model', TemplateView.as_view(template_name='docs/modelDoc.html'), name='model-doc-view'),
url(r'^experiment', TemplateView.as_view(template_name='docs/experimentDoc.html'), name='exp-doc-view'),
url(r'^job', TemplateView.as_view(template_name='docs/jobDoc.html'), name='job-doc-view'),
]

urlpatterns = [
    path(r'api/',include(api_urls)),
    path('', views.index, name='index'),
    path('models/', views.ModelListView.as_view(), name='models'),
    path('models/<pk>', views.ModelDetailView.as_view(), name='model-detail-view'),
    path('experiments/<pk>/', views.experimentdetailview, name='experiment-detail-view'),
    path('experimentFilter/', views.experiment_filter_form_view, name='filter-view'),
    path('experiment_list/', views.experiment_filter_list, name='filter-list-view'),
    path('jobs/<pk>', views.jobdetailview, name='job-detail-view'),
    path(r'compare/', views.jobcompareview2, name='job-compare-view'),
    path(r'timer/<name>/', views.timerdetailview, name='timer-detail-view'),
    path('docs/', TemplateView.as_view(template_name='docs.html'), name='doc-view'),
    path('docs/', include(doc_urls)),
    ]

