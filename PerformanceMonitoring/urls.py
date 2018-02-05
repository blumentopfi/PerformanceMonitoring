from django.urls import path
from . import views
from django.conf.urls import url, include
from .views import ModelList,ModelDetail,ModelExperimentList,ModelTimerList
from .views import ExperimentList,ExperimentDetail,ExperimentJobList
from .views import JobList,JobDetail,JobJobRankList,JobTimingsList
from .views import JobRankDetail,JobRankList
from .views import TimerDetail,TimerList,TimerTimingsList
from .views import TimingDetail,TimingList
model_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/experiments$', ModelExperimentList.as_view(), name='model_experiments'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/timers$', ModelTimerList.as_view(), name='model_timers'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', ModelDetail.as_view(), name='model-detail'),
    url(r'^$', ModelList.as_view(), name='model-list')
]
experiment_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/jobs$', ExperimentJobList.as_view(), name='experiment_jobs'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', ExperimentDetail.as_view(), name='experiment-detail'),
    url(r'^$', ExperimentList.as_view(), name='experiment-list')
]
job_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/jobranks$', JobJobRankList.as_view(), name='job_jobranks'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/timings$', JobTimingsList.as_view(), name='job_timings'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', JobDetail.as_view(), name='job-detail'),
    url(r'^$', JobList.as_view(), name='job-list')
]
jobranks_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', JobRankDetail.as_view(), name='job_rank-detail'),
    url(r'^$', JobRankList.as_view(), name='job_rank-list')
]
timer_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/timings$', TimerTimingsList.as_view(), name='timer_timings'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', TimerDetail.as_view(), name='timer-details'),
    url(r'^$', TimerList.as_view(), name='timer-list')
]
timings_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', TimingDetail.as_view(), name='timing-details'),
    url(r'^$', TimingList.as_view(), name='timing-list')
]
urlpatterns = [
    url(r'^models', include(model_urls)),
    url(r'^experiments', include(experiment_urls)),
    url(r'^jobs', include(job_urls)),
    url(r'^jobranks', include(jobranks_urls)),
    url(r'^timer', include(timer_urls)),
    url(r'^timings', include(timings_urls)),
]