

import datetime

class BaseStorage(object):
    def safe_report(self, report):
        raise NotImplementedError

class CSVStorage(BaseStorage):

    """Saving benchmark report to file"""

    def __init__(self, filename):
        self._filename = filename

    def save_benchmark_report(self, benchmark, report, note=None):
        fmt = None
        if 'averages' in report.reports:
            fmt = ("{type},{ts},{tag},{dbi},{version},"
                   "{data:.7f},{runs},{note}\n")
            total, runs = report.sumup_report(report.reports['averages'])
            data = total/runs
        elif 'tps' in report.reports:
            fmt = ("{type},{ts},{tag},{dbi},{version},"
                   "{data},{runs},{note}\n")

            total, runs = report.sumup_report(report.reports['tps'])
            data = total/runs

        if fmt:
            with open(self._filename, "a+") as fp:
                fp.write(fmt.format(
                    type='average',
                    ts=datetime.datetime.now(),
                    tag=benchmark.tag,
                    dbi=report.dbiName,
                    version=report.dbiVersion,
                    data=data,
                    runs=runs,
                    note=note or '')
                    )

class MySQLStorage(BaseStorage):
    pass