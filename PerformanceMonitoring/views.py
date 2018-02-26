from rest_framework import generics, permissions
from django.shortcuts import render
from django.views import generic as g
from PerformanceMonitoring.serializiers import *
from .models import *
from django.http import Http404
from PerformanceMonitoring import utils as u
import json
from datetime import datetime
from datetime import date
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


def experiment_filter_form_view(request):
    experiment_list = Experiment.objects.all()
    return render(
        request,
        'filter_experiment_page.html',
        context={'experiment_list': experiment_list}
    )

def experiment_filter_list(request):
    user_name = request.GET.get('user_name')
    experiment_name = request.GET.get('experiment_name')
    compiler_options = request.GET.get('compiler_options')
    n_mpi_rank = request.GET.get('n_mpi_rank')
    n_omp_thread = request.GET.get('n_omp_thread')
    submit_time_interval_start_string = request.GET.get('submit_time_interval_start')
    submit_time_interval_end_string =  request.GET.get('submit_time_interval_end')

    if experiment_name:
        experiment_set = Experiment.objects.all().filter(experiment_name=experiment_name)
    else:
        experiment_set = Experiment.objects.all()
    full_jobset = Job.objects.none()
    submit_start = datetime.min
    submit_end = datetime.max
    for experiment in experiment_set:
        jobset = experiment.job_set.prefetch_related('experiment').all()
        if (user_name):
            jobset = jobset.filter(user_name=user_name)
        if (n_mpi_rank):
            jobset = jobset.filter(n_mpi_ranks=n_mpi_rank)
        if (n_omp_thread):
            jobset = jobset.filter(n_omp_threads=n_omp_thread)
        if (submit_time_interval_start_string or submit_time_interval_end_string):
            if (submit_time_interval_start_string):
                submit_start = datetime.strptime(submit_time_interval_start_string, '%Y-%m-%dT%H:%M')
            if (submit_time_interval_end_string):
                submit_end = datetime.strptime(submit_time_interval_end_string,'%Y-%m-%dT%H:%M')



        jobset = jobset.filter(submitted__range=[submit_start,submit_end])
        full_jobset = full_jobset | jobset

    new_experiment_set = []
    for job in full_jobset:
        if (job.experiment not in new_experiment_set):
            new_experiment_set.append(job.experiment)

    new_jobset  = []
    for job in full_jobset:
        new_jobset.append(job.job_name)
    return render(
        request,
        'experiment_list.html',
        context={'experiment_set': new_experiment_set, 'job_set': json.dumps(new_jobset) ,'job_queryset':full_jobset})





class ModelDetailView(g.DetailView):
    model = ClimateModel
    context_object_name = 'model_detail'
    template_name = 'model_detail.html'

def experimentdetailview(request, pk):
    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        raise Http404("Job does not exist")

    jobs = request.GET.getlist('jobs')
    print(jobs)
    if not jobs:
        jobs = Job.objects.filter(experiment=pk)
    else:
        jobs = Job.objects.filter(job_name__in=jobs)
    run_times = []
    times_till_run = []
    for job in jobs :
        runtime = job.stop_date - job.start_date
        time_till_run = job.start_date - job.submitted
        run_times.append(round(runtime.total_seconds()/60,2))
        times_till_run.append(round(time_till_run.total_seconds()/60,2))
    job_names = json.dumps([j.job_name for j in jobs])

    return render(
        request,
        'experiment_detail.html',
        context={'experiment_detail': experiment,'job_set':jobs, 'run_times': run_times, 'job_names': job_names,'mean':sum(run_times)/len(run_times),'times_till_run':times_till_run}
    )

def jobdetailview(request, pk):
    t1 = datetime.now()
    try:
        job_id = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    timingset = timing.objects.all().select_related('timer').filter(job=job_id)
    timer_names, maxData, avgData, minData, radialmaxData, radialavgData, radialminData = u.getDataFromTiming(timingset)
    joblist = Job.objects.all()
    return render(
        request,
        'job_detail.html',
        context={'joblist':joblist,'job': job_id,'avg':avgData,'min':minData,'max':maxData,'timer_names':json.dumps(timer_names),'radialmaxData':radialmaxData,'radialavgData':radialavgData,'radialminData':radialminData,\
                 'simulated_time':round(u.getSimulatedTime(job_id),2)}
    )

def jobcompareview2(request):
    try:
        job_id = Job.objects.get(pk=request.GET.get('job1',''))
        job2_id = Job.objects.get(pk=request.GET.get('job2',''))
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    timingset = timing.objects.all().select_related('timer').filter(job=job_id)
    timer_names,maxData,avgData,minData,radialmaxData,radialavgData,radialminData = u.getDataFromTiming(timingset)
    timingset2 = timing.objects.all().select_related('timer').filter(job=job2_id)
    timer_names2, maxData2, avgData2, minData2, radialmaxData2, radialavgData2, radialminData2 = u.getDataFromTiming(timingset2)
    joblist = Job.objects.all()
    tupleList1 = []
    tupleList2 = []
    print(timer_names[1])
    for i in range(0,len(timer_names)):
        tupleList1.append((timer_names[i],maxData[i],avgData[i],minData[i]))
        tupleList2.append((timer_names2[i], maxData2[i], avgData2[i], minData2[i]))
    mergeSet = []
    print(tupleList1)
    print(tupleList2)
    for t1 in tupleList1:
        for t2 in tupleList1:
                if t1[0] == t2[0] :
                    mergeSet.append((t1[0],t1[1],t2[1],t1[2],t2[2],t1[3],t2[3]))



    print(mergeSet)
    return render(
        request,
        'job_compare.html',
        context={'joblist':joblist,'job': job_id,'job2':job2_id, \
                'avg':avgData,'min':minData,'max':maxData,'timer_names':json.dumps(timer_names),'radialmaxData':radialmaxData,'radialavgData':radialavgData,'radialminData':radialminData \
        ,'avg2':avgData2, 'min2': minData2, 'max2': maxData2, 'timer_names2': json.dumps(timer_names2), 'radialmaxData2': radialmaxData2, 'radialavgData2': radialavgData2, 'radialminData2': radialminData2 \
                 ,'simulated_time': round(u.getSimulatedTime(job_id),2), 'simulated_time2':u.getSimulatedTime(job2_id) \
                 ,'merge_timer_names':json.dumps([i[0] for i in mergeSet]),'merge_avg_data':[i[3] for i in mergeSet],'merge_avg_data2':[i[4] for i in mergeSet], \
                 'merge_max_data':[i[1] for i in mergeSet] ,'merge_max_data2':[i[2] for i in mergeSet], \
                 'merge_min_data':[i[5] for i in mergeSet],'merge_min_data2':[i[6] for i in mergeSet]
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