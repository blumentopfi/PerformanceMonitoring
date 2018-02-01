from django.db import models
from django.urls import reverse
# Create your models here.
class ClimateModel(models.Model):
    """
    A class defining the Climate Model
    """

    # Fields
    #Name of our model
    model_name = models.CharField(max_length=50, primary_key=True)

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.model_name)])

    def __str__(self):
        """
        String for representing the Climate Model object (in Admin site etc.)
        """
        return self.model_name
class Experiment(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    experiment_name = models.CharField(max_length=50, primary_key=True)
    model = models.ForeignKey(ClimateModel,on_delete=models.CASCADE, null=False)
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.experiment_name)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.experiment_name

class Job(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    job_name = models.CharField(max_length=50, unique=True,null=False)
    user_name = models.CharField(max_length=50)
    repository = models.CharField(max_length=256)
    revision = models.CharField(max_length=40)
    branch = models.CharField(max_length=64)
    submitted = models.DateTimeField()
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    n_mpi_ranks = models.SmallIntegerField(null=False)
    n_omp_threads = models.SmallIntegerField(null=False)
    simulated_time = models.DurationField()
    experiment = models.ForeignKey(Experiment,on_delete=models.CASCADE, null=False)
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.job_name
class job_rank(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    i_mpi_rank = models.SmallIntegerField()
    hostname= models.CharField(max_length=32)
    job = models.ForeignKey(Job,on_delete=models.CASCADE,null = False)
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.hostname
class timer(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    timer_name = models.CharField(max_length=32)
    model = models.ForeignKey(ClimateModel,on_delete=models.CASCADE,null = False)

    class Meta:
        unique_together = (('model', 'timer_name'),)
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.timer_name
class timing(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    i_mpi_rank = models.SmallIntegerField(null=False)
    i_omp_thread = models.SmallIntegerField(null=False)
    cnum = models.IntegerField()
    tsum = models.FloatField()
    job = models.ForeignKey(Job,on_delete=models.CASCADE,null=False)
    timer = models.ForeignKey(timer,on_delete=models.CASCADE,null=False)

    class Meta:
        unique_together = (('job', 'timer','i_mpi_rank','i_omp_thread'),)
    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.timer_name

