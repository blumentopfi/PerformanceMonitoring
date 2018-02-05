from rest_framework import generics, permissions


from PerformanceMonitoring.serializiers import *
from .models import *

class ModelList(generics.ListCreateAPIView):
    model = ClimateModel
    queryset = ClimateModel.objects.all()
    serializer_class = ClimateModelSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class ModelDetail(generics.RetrieveAPIView):
    model = ClimateModel
    queryset = ClimateModel.objects.all()
    serializer_class = ClimateModelSerializer

class ExperimentList(generics.ListCreateAPIView):
    model = Experiment
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class ExperimentDetail(generics.RetrieveAPIView):
    model = Experiment
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ModelExperimentList(generics.ListAPIView):
    model = Experiment
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        queryset = super(ModelExperimentList, self).get_queryset()
        return queryset.filter(model__pk=self.kwargs.get('pk'))
class ModelTimerList(generics.ListAPIView):
    model = timer
    queryset = timer.objects.all()
    serializer_class = TimerSerializer

    def get_queryset(self):
        queryset = super(ModelTimerList, self).get_queryset()
        return queryset.filter(model__pk=self.kwargs.get('pk'))

class JobDetail(generics.RetrieveAPIView):
    model = Job
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class JobList(generics.ListCreateAPIView):
    model = Job
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class ExperimentJobList(generics.ListAPIView):
    model = Job
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = super(ExperimentJobList, self).get_queryset()
        return queryset.filter(experiment__pk=self.kwargs.get('pk'))

class JobRankDetail(generics.RetrieveAPIView):
    model = job_rank
    queryset = job_rank.objects.all()
    serializer_class = JobRankSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class JobRankList(generics.ListCreateAPIView):
    model = job_rank
    queryset = job_rank.objects.all()
    serializer_class = JobRankSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class JobJobRankList(generics.ListAPIView):
    model = job_rank
    queryset = job_rank.objects.all()
    serializer_class = JobRankSerializer
    def get_queryset(self):
        queryset = super(JobJobRankList, self).get_queryset()
        return queryset.filter(job__pk=self.kwargs.get('pk'))

class JobTimingsList(generics.ListAPIView):
    model = timing
    queryset = timing.objects.all()
    serializer_class = TimingSerializer
    def get_queryset(self):
        queryset = super(JobTimingsList, self).get_queryset()
        return queryset.filter(job__pk=self.kwargs.get('pk'))

class TimerDetail(generics.RetrieveAPIView):
    model = timer
    queryset = timer.objects.all()
    serializer_class = TimerSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class TimerList(generics.ListCreateAPIView):
    model = timer
    queryset = timer.objects.all()
    serializer_class = TimerSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class TimingDetail(generics.RetrieveAPIView):
    model = timing
    queryset = timing.objects.all()
    serializer_class = TimingSerializer
    permission_classes = [
        permissions.AllowAny
    ]
class TimingList(generics.ListCreateAPIView):
    model = timing
    queryset = timing.objects.all()
    serializer_class = TimingSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class TimerTimingsList(generics.ListAPIView):
    model = timing
    queryset = timing.objects.all()
    serializer_class = TimingSerializer
    def get_queryset(self):
        queryset = super(TimerTimingsList, self).get_queryset()
        return queryset.filter(timer__pk=self.kwargs.get('pk'))