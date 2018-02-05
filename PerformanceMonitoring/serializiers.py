from rest_framework import serializers
import PerformanceMonitoring.models as m


class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.timing
        fields = '__all__'

class TimerSerializer(serializers.ModelSerializer):
    #timings = TimingSerializer(many=True,read_only=True)
    timings = serializers.HyperlinkedIdentityField(view_name='timer_timings',read_only=True)
    class Meta:
        model = m.timer
        fields = '__all__'

class JobRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.job_rank
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    job_ranks = serializers.HyperlinkedIdentityField(view_name='job_jobranks',read_only=True)
    #job_ranks = JobRankSerializer(read_only=True,many=True)
    #timings = TimingSerializer(read_only=True,many=True)
    timings = serializers.HyperlinkedIdentityField(view_name='job_timings',read_only=True)
    class Meta:
        model = m.Job
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    jobs = serializers.HyperlinkedIdentityField(view_name='experiment_jobs',read_only=True)
    #jobs=JobSerializer(read_only=True,many=True)
    class Meta:
        model = m.Experiment
        fields = '__all__'


class ClimateModelSerializer(serializers.ModelSerializer):
    # Fields
    #experiments = (read_only=True,many=True)
    experiments = serializers.HyperlinkedIdentityField(view_name='model_experiments',read_only=True)
    #timers = TimerSerializer(read_only=True,many=True)
    timers = serializers.HyperlinkedIdentityField(view_name='model_timers',read_only=True)
    class Meta:
        model = m.ClimateModel
        fields = '__all__'





