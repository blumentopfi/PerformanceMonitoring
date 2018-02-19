from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from PerformanceMonitoring.utils import ProcessHDFToDatabase
from PerformanceMonitoring import models as m
import h5py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('monitor/', include('PerformanceMonitoring.urls')),
    path('', RedirectView.as_view(url='/monitor/'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#print("TESTASDASDASD")
#print(m.ClimateModel.objects.all()[0].experiment_set.all()[0])

#ProcessHDFToDatabase(h5py.File("C:/icon-timer-0001.h5", mode='r'))