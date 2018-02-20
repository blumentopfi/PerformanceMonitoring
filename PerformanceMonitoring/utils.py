import numpy as np
import h5py
import datetime
from django.db import models
from django.db import connection
from PerformanceMonitoring import models as m
_SCT_H5_TL_GROUP = '/'
_SCT_H5_DEFAULT_CTX = 'default context'
_SCT_H5_SCT_INTERNAL_ATTRS_GROUP = 'sct_internal_attributes'
_SCT_H5_REPORT_ATTRS_GROUP = 'report_attributes'
def _raise_inv_format(msg):
    raise ValueError('h5 file has invalid format: ' + msg)
def _db_get_timer_idx(model, timer):

    set = m.timer.objects.all().filter(model=model).filter(timer_name=timer.decode('UTF-8'))
    if not set:
        new_timer = m.timer.objects.create(model=model,timer_name=timer.decode('UTF-8'))
        return new_timer.id
    return set[0].id

def ProcessHDFToDatabase(hdf5File):
    try:
        tl_h5_grp = hdf5File[_SCT_H5_TL_GROUP]
        h5_sct_int_attrs_grp = tl_h5_grp[_SCT_H5_SCT_INTERNAL_ATTRS_GROUP]
        h5_report_attrs_grp = tl_h5_grp[_SCT_H5_REPORT_ATTRS_GROUP]

        model = h5_report_attrs_grp.attrs['model'].decode('UTF-8')
        if not isinstance(model, str):
            _raise_inv_format('\'model\' is not of type string')
        else:
            print("Model " + model)
        experiment = h5_report_attrs_grp.attrs['experiment name'].decode('UTF-8')
        if not isinstance(experiment, str):
            _raise_inv_format('\'experiment\' is not of type string')
        else:
            print("Experiment " + experiment)

        compiler_version = h5_report_attrs_grp.attrs['compiler version'].decode('UTF-8')
        if not isinstance(compiler_version, str):
            _raise_inv_format('\'compiler_version\' is not of type string')
        else:
            print("Compiler version " + compiler_version)

        compiler_options = h5_report_attrs_grp.attrs['compiler options'].decode('UTF-8')
        if not isinstance(compiler_options, str):
            _raise_inv_format('\'compiler_options\' is not of type string')
        else:
            print("Compiler options " + compiler_options)

        executable = h5_report_attrs_grp.attrs['executable'].decode('UTF-8')
        if not isinstance(executable, str):
            _raise_inv_format('\'executable\' is not of type string')
        else:
            print("Executable " + executable)

        job_name = h5_report_attrs_grp.attrs['job name'].decode('UTF-8')
        if not isinstance(job_name, str):
            _raise_inv_format('\'job_name\' is not of type string')
        else:
            print("Job name " + job_name)

        job = h5_report_attrs_grp.attrs['job id'].decode('UTF-8')
        if not isinstance(job, str):
            _raise_inv_format('\'job\' is not of type string')
        else:
            print("Job id " + job)

        user_name = h5_report_attrs_grp.attrs['user name'].decode('UTF-8')
        if not isinstance(user_name, str):
            _raise_inv_format('\'user_name\' is not of type string')
        else:
            print("User name " + user_name)

        os_name = h5_report_attrs_grp.attrs['operating system name'].decode('UTF-8')
        if not isinstance(os_name, str):
            _raise_inv_format('\'os_name\' is not of type string')
        else:
            print("Operating system name " + os_name)

        repo = h5_report_attrs_grp.attrs['repository'].decode('UTF-8')
        if not isinstance(repo, str):
            _raise_inv_format('\'repo\' is not of type string')
        else:
            print("Repository " + repo)

        rev = h5_report_attrs_grp.attrs['revision'].decode('UTF-8')
        if not isinstance(rev, str):
            _raise_inv_format('\'rev\' is not of type string')
        else:
            print("Revision " + rev)

        branch = h5_report_attrs_grp.attrs['branch'].decode('UTF-8')
        if not isinstance(branch, str):
            _raise_inv_format('\'branch\' is not of type string')
        else:
            print("Branch " + branch)

        simulated_time = h5_report_attrs_grp.attrs['run length'].decode('UTF-8')
        if not isinstance(simulated_time, str):
            _raise_inv_format('\'simulated_time\' is not of type string')
        else:
            print("Run length " + simulated_time)
        submit_time = h5_report_attrs_grp.attrs['submit date'].decode('UTF-8')
        if not isinstance(submit_time, str):
            _raise_inv_format('\'submit_time\' is not of type string')
        try:
            submit_time = datetime.datetime.strptime(submit_time,
                                                     '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            _raise_inv_format('\'submit_time\' format not recognized')
        print("Submit time " + str(submit_time))

        start_time = h5_sct_int_attrs_grp.attrs['sct start time'].decode('UTF-8')
        if not isinstance(start_time, str):
            _raise_inv_format('\'start_time\' is not of type string')
        try:
            start_time = datetime.datetime.strptime(start_time,
                                                    '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            _raise_inv_format('\'start_time\' format not recognized')
        print("Start time " + str(start_time))

        stop_time = h5_sct_int_attrs_grp.attrs['sct stop time'].decode('UTF-8')
        if not isinstance(stop_time, str):
            _raise_inv_format('\'stop_time\' is not of type string')
        try:
            stop_time = datetime.datetime.strptime(stop_time,
                                                   '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            _raise_inv_format('\'stop_time\' format not recognized')
        print("Stop time " + str(stop_time))

        hgrid = h5_report_attrs_grp.attrs['horizontal grid'].decode('UTF-8')
        if not isinstance(repo, str):
            _raise_inv_format('\'hgrid\' is not of type string')
        else:
            print("Horizontal grid " + hgrid)

        nlev = h5_report_attrs_grp.attrs['vertical levels']
        if not isinstance(nlev, np.signedinteger):
            _raise_inv_format('\'nlev\' ' +
                              'is not of type integer')
        print("Vertical levels " + str(nlev))

        nproma = h5_report_attrs_grp.attrs['nproma']
        if not isinstance(nproma, np.signedinteger):
            _raise_inv_format('\'nproma\' ' +
                              'is not of type integer')
        print("nproma " + str(nproma))

        nranks = tl_h5_grp.attrs['number of MPI tasks']
        if not isinstance(nranks, np.signedinteger):
            _raise_inv_format('\'number of MPI tasks\' ' +
                              'is not of type integer')
        print("MPI tasks " + str(nranks))

        nthreads = tl_h5_grp.attrs['number of OpenMP threads']
        if not isinstance(nthreads, np.signedinteger):
            _raise_inv_format('\'number of OpenMP threads\' ' +
                              'is not of type integer')
        print("OpenMP threads " + str(nthreads))

        hosts = tl_h5_grp.attrs['hosts']
        if not isinstance(hosts, np.ndarray) or hosts.dtype.kind != 'S':
            _raise_inv_format('\'hosts\' is not of type list of strings')
        elif hosts.ndim != 1 or hosts.shape[0] != nranks:
            _raise_inv_format('dimension mismatch for \'hosts\'')
        print("Hosts " + str(hosts))

        ctx_h5_grp = tl_h5_grp[_SCT_H5_DEFAULT_CTX]
        timer_names = ctx_h5_grp['timer_names']
        if not isinstance(timer_names, h5py.Dataset) or \
                timer_names.dtype.kind != 'S':
            _raise_inv_format('\'timer_names\' is not a h5 dataset of strings')
        elif len(timer_names.shape) != 2 or timer_names.shape[0] != nranks:
            _raise_inv_format('dimension mismatch for \'timer_names\'')

        ntimers = timer_names.shape[1]

        timer_cnum = ctx_h5_grp['time/timer_cnum']
        if not isinstance(timer_cnum, h5py.Dataset) or \
                timer_cnum.dtype.kind != 'i':
            _raise_inv_format('\'timer_cnum\' is not a h5 dataset of integers')
        elif len(timer_cnum.shape) != 3 or timer_cnum.shape[0] != nranks or \
                timer_cnum.shape[1] != nthreads + 1 or \
                timer_cnum.shape[2] != ntimers:
            _raise_inv_format('dimension mismatch for \'timer_cnum\'')

        timer_tsum = ctx_h5_grp['time/timer_tsum']
        if not isinstance(timer_cnum, h5py.Dataset) or \
                timer_tsum.dtype.kind != 'f':
            _raise_inv_format('\'timer_tsum\' is not a h5 dataset of floats')
        elif len(timer_tsum.shape) != 3 or timer_tsum.shape[0] != nranks or \
                timer_tsum.shape[1] != nthreads + 1 or \
                timer_tsum.shape[2] != ntimers:
            _raise_inv_format('dimension mismatch for \'timer_tsum\'')
    except KeyError as e:
        _raise_inv_format(str(e))

    #Now that we have read all values we put them into our database#

    #first get our model
    model_db_entry = m.ClimateModel.objects.all().filter(model_name=model)
    if not model_db_entry:
         m.ClimateModel.objects.create(model_name=model)
    model_db_entry = m.ClimateModel.objects.all().filter(model_name=model)[0]

    timer_ids = np.zeros((nranks, ntimers), dtype=np.int16)
    timer_id_cache = dict()
    for i in range(0, nranks):
        for j in range(0, ntimers):
            timer_name = timer_names[i, j]
            if timer_name in timer_id_cache:
                timer_ids[i, j] = timer_id_cache[timer_name]
            else:
                timer_id = _db_get_timer_idx(model_db_entry, timer_name)
                timer_id_cache[timer_name] = timer_id
                timer_ids[i, j] = timer_id
    del timer_names, timer_id_cache

    set = m.Experiment.objects.all().filter(model=model_db_entry).filter(experiment_name=experiment)
    if not set:
        m.Experiment.objects.create(model=model_db_entry,experiment_name=experiment)
        print("Saved " + experiment + "into DB")
    experiment_db_entry = m.Experiment.objects.all().filter(model=model_db_entry).filter(experiment_name=experiment)[0]
    #TODO Ask what simulated_time is
    job_id = m.Job.objects.all().filter(job_name=job)
    if not job_id:
        job_id = m.Job.objects.create(experiment=experiment_db_entry,job_name=job,user_name=user_name,repository=repo,revision=rev,branch=branch,submitted=submit_time,start_date=start_time,stop_date=stop_time,\
                                 n_mpi_ranks=int(nranks),n_omp_threads=int(nthreads))
    print("created the job")
    job_db_instance = m.Job.objects.all().filter(job_name=job)[0]
    #cursor = connection.cursor
    #cursor.executemany('INSERT INTO job_ranks (job,i_mpi_rank,hostname) VALUES (%s,%s,%s);',
                    #    zip([job_id] * nranks, range(0, nranks), hosts))

    #print(len([job_db_instance.id]*nranks))
    for j,impi,hostname in zip([job_db_instance.job_name] * nranks, range(0, nranks), hosts):
        m.job_rank.objects.create(job=job_db_instance,i_mpi_rank=impi,hostname=hostname.decode('UTF-8'))
        print(impi)

    Counter = 0
    print(nranks*(nthreads+1)*ntimers)

    for i in range(0, nranks):
        for j in range(0, nthreads + 1):
            for k in range(0, ntimers):
                Counter = Counter+1
                print(Counter)
                if not timer_cnum[i, j, k]:
                    continue
                timer_db_instance = m.timer.objects.filter(id=int(timer_ids[i, k]))[0]
                if not(m.timing.objects.all().filter(job_id=job_db_instance).filter(timer=timer_db_instance).filter(i_mpi_rank=i).filter(i_omp_thread=j)):
                    m.timing.objects.create(job=job_db_instance,timer=timer_db_instance,i_mpi_rank=i,i_omp_thread=j,cnum=int(timer_cnum[i, j, k]),tsum=float(timer_tsum[i, j, k]))

    return


def getDataFromTiming(timingset):


    timerset = m.timer.objects.all()
    dataset = []
    for timer_instance in timerset:
        temptuple = (timer_instance,[])
        for timing_instance in timingset:
            if timing_instance.timer_id == timer_instance.id:
                a,b = temptuple
                b.append(timing_instance)
        dataset.append(temptuple)
    timer_tuple_list = []
    for timer_instance,timing_list in dataset:
        count_tsum = 0
        list_ranks = []
        max = 0
        min = 1000000000000000
        for timing_instance in timing_list:
            count_tsum = count_tsum + timing_instance.tsum
            if (timing_instance.tsum < min):
                min = timing_instance.tsum
            if (timing_instance.tsum > max):
                max = timing_instance.tsum
            #list_ranks.append(timing_instance.i_mpi_rank)
        setList = list_ranks
        if (len(setList) != len(list_ranks)):
            print(timer_instance.timer_name)
        avg = 0
        if (count_tsum > 0 ):
            avg = count_tsum/len(timing_list)
        if (max != 0 and min != 1000000000000000 and avg != 0):
            timer_tuple = (timer_instance.timer_name,max,min,avg)
            timer_tuple_list.append(timer_tuple)




    #get only the top 10
    timer_tuple_list = sorted(timer_tuple_list, key=lambda t: t[3], reverse=True)[:10]
    return timer_tuple_list
