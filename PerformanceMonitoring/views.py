from rest_framework import generics, permissions
from django.shortcuts import render
from django.views import generic as g
from PerformanceMonitoring.serializiers import *
from .models import *
from django.http import Http404
from PerformanceMonitoring import utils as u
import json
from datetime import datetime
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


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_models = ClimateModel.objects.all().count()
    num_experiments = Experiment.objects.all().count()
    num_jobs = Job.objects.all().count()
    num_timings = timing.objects.all().count()
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_models': num_models, 'num_experiments': num_experiments,
                 'num_jobs': num_jobs, 'num_timings': num_timings},
    )

class ModelListView(g.ListView):
    model = ClimateModel
    context_object_name = 'model_list'
    template_name = 'model_list.html'


class ModelDetailView(g.DetailView):
    model = ClimateModel
    context_object_name = 'model_detail'
    template_name = 'model_detail.html'

def experimentdetailview(request, pk):
    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        raise Http404("Job does not exist")

    jobs = Job.objects.all().filter(experiment=pk)
    times = []
    for job in jobs :
        runtime = job.stop_date - job.start_date
        times.append(runtime.total_seconds()/60)

    print(times)
    print(jobs)
    job_names = json.dumps([j.job_name for j in jobs])
    return render(
        request,
        'experiment_detail.html',
        context={'experiment_detail': experiment, 'times': times, 'job_names': job_names,'mean':sum(times)/len(times)}
    )


class ExperimentDetailView(g.DetailView):
    model = Experiment
    context_object_name = 'experiment_detail'
    template_name = 'experiment_detail.html'

#class JobDetailView(g.DetailView):
#    model = Job
    #context_object_name = 'job_detail'
#    template_name = 'job_detail.html'

def jobdetailview(request, pk):
    t1 = datetime.now()
    try:
        job_id = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    timingset = timing.objects.all().select_related('timer').filter(job=job_id)
    timer_tuple_list = u.getDataFromTiming(timingset)
    timer_names = [i[0] for i in timer_tuple_list]
    avgData = [i[3] for i in timer_tuple_list]
    minData = [i[2] for i in timer_tuple_list]
    maxData = [i[1] for i in timer_tuple_list]
    json_timer_names = json.dumps(timer_names)
    radialavgData =" { \"year\": 1910,\"data\": { "
    radialmaxData ="[ { \"year\": 1910,\"data\": { "
    radialminData =" { \"year\": 1910,\"data\": { "

    for name,ma,mi,av in timer_tuple_list:
        radialavgData = radialavgData + "\"" + name + "\" :" + str(av) + ","
        radialminData = radialminData + "\"" + name + "\" :" + str(mi) + ","
        radialmaxData = radialmaxData + "\"" + name + "\" :" + str(ma) + ","
    #strip the last comma
    radialavgData=radialavgData[:-1]
    radialminData=radialminData[:-1]
    radialmaxData=radialmaxData[:-1]
    radialavgData+="}},"
    radialmaxData += "}},"
    radialminData += "}}]"
    delta = datetime.now() - t1
    print("time = " + str(delta.seconds))

    return render(
        request,
        'job_detail.html',
        context={'job': job_id,'avg':avgData,'min':minData,'max':maxData,'timer_names':json_timer_names,'radialmaxData':radialmaxData,'radialavgData':radialavgData,'radialminData':radialminData}
    )

def jobcompareview(request, pk, pk2):
    try:
        job_id = Job.objects.get(pk=pk)
        job2_id = Job.objects.get(pk=pk2)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(
        request,
        'job_compare.html',
        context={'job': job_id,'job2':job2_id}
    )
def jobcompareview2(request):
    try:
        job_id = Job.objects.get(pk=request.GET.get('job1',''))
        job2_id = Job.objects.get(pk=request.GET.get('job2',''))
    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    timingset = timing.objects.all().select_related('timer').filter(job=job_id)
    timer_tuple_list = u.getDataFromTiming(timingset)
    timer_names = [i[0] for i in timer_tuple_list]
    avgData = [i[3] for i in timer_tuple_list]
    minData = [i[2] for i in timer_tuple_list]
    maxData = [i[1] for i in timer_tuple_list]
    json_timer_names = json.dumps(timer_names)
    radialavgData = " { \"year\": 1910,\"data\": { "
    radialmaxData = "[ { \"year\": 1910,\"data\": { "
    radialminData = " { \"year\": 1910,\"data\": { "

    for name, ma, mi, av in timer_tuple_list:
        radialavgData = radialavgData + "\"" + name + "\" :" + str(av) + ","
        radialminData = radialminData + "\"" + name + "\" :" + str(mi) + ","
        radialmaxData = radialmaxData + "\"" + name + "\" :" + str(ma) + ","
    # strip the last comma
    radialavgData = radialavgData[:-1]
    radialminData = radialminData[:-1]
    radialmaxData = radialmaxData[:-1]
    radialavgData += "}},"
    radialmaxData += "}},"
    radialminData += "}}]"

    timingset2 = timing.objects.all().select_related('timer').filter(job=job2_id)
    timer_tuple_list2 = u.getDataFromTiming(timingset2)
    timer_names2 = [i[0] for i in timer_tuple_list2]
    avgData2 = [i[3] for i in timer_tuple_list2]
    minData2 = [i[2] for i in timer_tuple_list2]
    maxData2 = [i[1] for i in timer_tuple_list2]
    json_timer_names2 = json.dumps(timer_names2)
    radialavgData2 = " { \"year\": 1910,\"data\": { "
    radialmaxData2 = "[ { \"year\": 1910,\"data\": { "
    radialminData2 = " { \"year\": 1910,\"data\": { "
    for name, ma, mi, av in timer_tuple_list:
        radialavgData2 = radialavgData2 + "\"" + name + "\" :" + str(av) + ","
        radialminData2 = radialminData2 + "\"" + name + "\" :" + str(mi) + ","
        radialmaxData2 = radialmaxData2 + "\"" + name + "\" :" + str(ma) + ","
    # strip the last comma
    radialavgData2 = radialavgData2[:-1]
    radialminData2 = radialminData2[:-1]
    radialmaxData2 = radialmaxData2[:-1]
    radialavgData2 += "}},"
    radialmaxData2 += "}},"
    radialminData2 += "}}]"




    return render(
        request,
        'job_compare.html',
        context={'job': job_id,'job2':job2_id, \
                'avg':avgData,'min':minData,'max':maxData,'timer_names':json_timer_names,'radialmaxData':radialmaxData,'radialavgData':radialavgData,'radialminData':radialminData \
        ,'avg2':avgData2, 'min2': minData2, 'max2': maxData2, 'timer_names2': json_timer_names2, 'radialmaxData2': radialmaxData2, 'radialavgData2': radialavgData2, 'radialminData2': radialminData2
                 }
    )

def timerdetailview(request, name):
    try:
        timer_id = timer.objects.get(timer_name=name)
        job_id = Job.objects.get(pk=request.GET.get('job',''))
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    except timer.DoesNotExist:
        raise Http404("Timer does not exist")

    timingset = timing.objects.all().select_related('timer').filter(job=job_id,timer=timer_id)
    rank_timing_dictionary = {}
    for timing_instance in timingset:
        rank = timing_instance.i_mpi_rank
        if rank in rank_timing_dictionary:
            rank_timing_dictionary[rank].append(timing_instance.tsum)
        else:
            rank_timing_dictionary[rank] = [timing_instance.tsum]

    data = []
    labels = []
    for rank in rank_timing_dictionary:
        data.append(sum(rank_timing_dictionary[rank])/float(len(rank_timing_dictionary[rank])))
        labels.append(rank)

    return render(
        request,
        'timer_detail.html',
        context={'timer': timer_id,'job':job_id,'timings':data,'labels':labels}
    )