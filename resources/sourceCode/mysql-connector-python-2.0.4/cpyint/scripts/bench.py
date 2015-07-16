#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, 2014 Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function

import datetime
import inspect
from optparse import OptionParser
import os
import sys

sys.path.insert(0, 'lib')
sys.path.insert(0, '.')

try:
    from cpyint.benchmark.errors import BenchmarkError
    from cpyint.benchmark import benchmarking
    from cpyint.benchmark.storage import CSVStorage
except ImportError:
    raise
    print("Failed importing Benchmark modules. Execute this script from the "
          "main Connector/Python repository.")
    sys.exit(1)

__MYSQL_DEBUG__ = 1

_PY_DBI_ = ['mysql.connector', 'MySQLdb', 'oursql', 'pymysql', ]


def _opt_parser():
    p = OptionParser()

    # General options
    p.add_option('', '--threads', dest='threads', metavar='NUMBER',
                 type='int',
                 help='Number of threads')
    p.add_option('', '--runs', dest='runs', metavar='NUMBER',
                 type='int',
                 help='Number of total runs')
    p.add_option('', '--duration', dest='duration', metavar='NUMBER',
                 type='int',
                 help='How long to run in seconds for calculating TPS')
    p.add_option('', '--dbi', dest='dbi', metavar='NAME',
                 help='Database interface to use (e.g. mysql.connector, MySQLdb, ..)')
    p.add_option('-g', '--group', dest='group', metavar='NAME',
                 help='Benchmark group')
    p.add_option('-b', '--benchmark', dest='benchmark', metavar='NAME',
                 help='Execute a particular benchmark')
    p.add_option('', '--note', dest='note', metavar='NAME',
                 help='A note describing this particular execution')

    p.add_option('-O', '--output', dest='output', metavar='NAME',
                 help="URI describing where to save data, for example, "
                      "bench.csv, or "
                      "mysql://root:secret@localhost:3306/dbname")

    # MySQL options
    p.add_option('-S', '--socket', dest='socket', metavar='NAME',
                 default=None,
                 help='MySQL UNIX Socket')
    p.add_option('-H', '--hostname', dest='hostname', metavar='NAME',
                 help='MySQL hostname or IP')
    p.add_option('', '--port', dest='port', metavar='PORT',
                 default='3306', type="int",
                 help='MySQL TCP port number')
    p.add_option('-u', '--user', dest='username', metavar='NAME',
                 help='User for login into MySQL')
    p.add_option('-p', '--password', dest='password', metavar='PASSWORD',
                 help='Password to login into MySQL')
    p.add_option('-D', '--database', dest='database', metavar='NAME',
                 help='Database to use')

    p.set_defaults(
        threads=1,
        runs=1,
        duration=60,
        throttle=0,
        dbi=None,
        group=None,
        benchmark=None,
        note=None
    )
    (options, args) = p.parse_args()
    return options


class Report(object):
    def __init__(self, nrWorkers, dbiName, dbiVersion=None):
        self.nrWorkers = nrWorkers
        self.reports = {}
        self.dbiVersion = dbiVersion
        self.dbiName = dbiName

        if isinstance(self.dbiVersion, tuple):
            self.dbiVersion = '.'.join(map(str, ver[0:3]))
        elif not dbiVersion:
            self.dbiVersion = ''

    def add_report(self, sender, report, report_type='averages'):
        self.reports.setdefault(report_type, {})
        self.reports[report_type][sender] = report

        #if len(self.reports) == self.nrWorkers:
        #    self.process_reports()

    def show_average(self, total, runs):
        if not runs:
            return
        print("{dbi} {version}: {average:.7f} (runs={runs})".format(
            dbi=self.dbiName,
            version=self.dbiVersion,
            average=total / runs,
            runs=runs, )
        )

    def sumup_report(self, report_items):
        total = 0
        nrdata = 0
        for sender, rep in report_items.items():
            total += sum(rep)
            nrdata += len(rep)

        return (total, nrdata)

    def show(self, benchmark):
        total = 0
        nrdata = 0

        if not self.reports:
            return

        print('-' * 78)
        print(benchmark.description)

        if 'averages' in self.reports:
            self.show_average(*self.sumup_report(self.reports['averages']))

        if 'tps' in self.reports:
            run = 1
            for sender, report in self.reports['tps'].items():
                for tpsdata in report:
                    print("{dbi} {version}: run {run} {tps} TPS".format(
                        dbi=self.dbiName,
                        version=self.dbiVersion,
                        run=run,
                        tps=tpsdata,
                    ))
                    run += 1

            self.show_average(*self.sumup_report(self.reports['tps']))

    def save(self, benchmark, note=None):
        if 'averages' in self.reports:
            fmt = ("{type},{ts},{tag},{dbi},{version},"
                   "{data:.7f},{runs},{note}\n")
            total, runs = self.sumup_report(self.reports['averages'])
            data = total / runs
        elif 'tps' in self.reports:
            fmt = ("{type},{ts},{tag},{dbi},{version},"
                   "{data},{runs},{note}\n")
            total, runs = self.sumup_report(self.reports['tps'])
            data = total / runs

        with open("benchmark_report.csv", "a+") as fp:
            fp.write(fmt.format(
                type='average',
                ts=datetime.datetime.now(),
                tag=benchmark.tag,
                dbi=self.dbiName,
                version=self.dbiVersion,
                data=data,
                runs=runs,
                note=note or '')
            )


def check_dbi(dbi):
    """Check if given database is valid

    Check if the given database driver dbi can be imported. It will return
    the version of the driver as a tuple.

    Raises BenchmarkError when something fails.

    Returns the loaded module.
    """
    try:
        __import__(dbi)
    except ImportError:
        raise BenchmarkError("Failed importing {0}".format(dbi))

    dbi_module = sys.modules[dbi]

    if not hasattr(dbi_module, '__version__'):
        # We probably have CPY 1.0, which has no __version__
        if dbi == 'mysql.connector':
            tmp = __import__(dbi + '.version', fromlist=['VERSION'])
            dbi_module.__version__ = '.'.join([str(i) for i in tmp.VERSION[0:3]])
        raise BenchmarkError("Failed getting version from {0}".format(dbi))

    return dbi_module


def main():
    ops = _opt_parser()

    dbConfig = {
        'db': (ops.database or 'test'),
        'user': (ops.username or 'root'),
        'passwd': (ops.password or ''),
        'host': (ops.hostname or 'localhost'),
    }

    if ops.socket is not None:
        dbConfig['unix_socket'] = ops.socket

    if ops.group and ops.benchmark:
        print("Use --group or --benchmark, not both.")
        sys.exit(1)

    runPerThr = int(ops.runs / ops.threads)
    thrs = range(ops.threads)

    storage = None
    if ops.output:
        if '://' not in ops.output:
            storage = CSVStorage(ops.output)
        else:
            print("More storage options soon; use a filename for now")

    reports = {}
    # Force including the ./lib subfolder making C/Py available
    try:
        if not os.environ['PYTHONPATH']:
            raise KeyError
        import mysql.connector
    except (KeyError, ImportError):
        sys.path.insert(0, 'lib')
    if ops.dbi:
        try:
            dbi_module = check_dbi(ops.dbi)
            dbi_version = dbi_module.__version__
        except BenchmarkError as exc:
            print(exc)
            sys.exit(1)
        reports[ops.dbi] = Report(ops.threads, ops.dbi,
                                  dbiVersion=dbi_version)
    else:
        exclude_dbi = []
        for dbi in _PY_DBI_:
            try:
                dbi_module = check_dbi(dbi)
                dbi_version = dbi_module.__version__
            except BenchmarkError as exc:
                print("Excluding {0}: import failed ({1})".format(
                    dbi, str(exc)))
                exclude_dbi.append(dbi)
            else:
                if dbi == 'mysql.connector':
                    if hasattr(dbi_module, 'HAVE_CEXT'):
                        have_cext = dbi_module.HAVE_CEXT
                    else:
                        have_cext = False
                    print("Including {0}; C/Extension {1}".format(
                        dbi, have_cext))
                else:
                    print("Including {0}")
                reports[dbi] = Report(ops.threads, dbi, dbiVersion=dbi_version)

    if not reports:
        print("No database driver found. Try using PYTHONPATH.")
        print("Use --help for more information")
        sys.exit(1)

    print("=" * 79)
    print("Python Database Driver benchmarks for MySQL")
    if ops.note:
        print(ops.note)
    print("=" * 79)

    if ops.group:
        print("Running group {0}".format(ops.group))
    else:
        print("Running all groups")

    exec_benchmarks = []
    known_benchmarks = []
    for name, benchclass in inspect.getmembers(benchmarking, inspect.isclass):
        if (not benchclass.__name__.startswith('Base') and
                issubclass(benchclass, benchmarking.BaseBenchmark)):
            if ops.group and not benchclass.group == ops.group:
                continue
            known_benchmarks.append(benchclass)

    if ops.benchmark:
        try:
            exec_benchmarks = [getattr(benchmarking, ops.benchmark)]
        except AttributeError:
            print("Benchmark '{0}' is unknown".format(ops.benchmark))
            print("Known brenchmarks:")
            for benchclass in known_benchmarks:
                print("  {0}: {1}".format(benchclass.__name__,
                                          benchclass.description))
    else:
        exec_benchmarks = known_benchmarks

    for curr_bench in exec_benchmarks:
        for dbi, report in reports.items():
            try:
                package = __import__(dbi, fromlist=[])
                dbi_module = sys.modules[dbi]
                thrs = [None] * ops.threads
                nr = 0
                for thr in thrs:
                    nr += 1
                    thr = curr_bench(dbi_module, report.add_report,
                                     runs=runPerThr, duration=ops.duration,
                                     config=dbConfig, name=str(nr))
                    thr.start()
                    thr.join()
                report.show(curr_bench)
            except (SystemExit, KeyboardInterrupt):
                print("Stopping..")
            except BenchmarkError as exc:
                print(exc)
            else:
                if storage:
                    storage.save_benchmark_report(curr_bench, report,
                                                  note=ops.note)


if __name__ == '__main__':
    main()
