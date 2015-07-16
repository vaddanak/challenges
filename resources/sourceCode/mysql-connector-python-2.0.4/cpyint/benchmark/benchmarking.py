

import random
import sys
import threading
import time

from .errors import BenchmarkError

class BaseBenchmark(threading.Thread):

    description = "Base Benchmark"
    tag = "base_benchmark"
    group = None
    report_type = 'averages'

    def __init__(self, dbi, callback, runs=1, duration=60,
                 name=None, config={}):
        self.dbi = dbi
        self.runs = runs
        self.duration = duration
        self.report = []
        self.config = config
        self.callback = callback
        self.exception_info = None

        if not name:
            name = self.__class__.__name__
        super(BaseBenchmark, self).__init__(name=name)

    def _get_connection(self):
        return self.dbi.connect(**self.config)

    def run(self):
        try:
            self.setup()
            self._run()
            self.teardown()
            self.callback(self.name, self.report, self.report_type)
        except:
            self.exception_info = sys.exc_info()

    def join(self):
        super(BaseBenchmark, self).join()
        if self.exception_info:
            msg = "Benchmark {tag} raised exception: {errmsg}".format(
                name=self.getName(), errmsg=self.exception_info[1],
                tag=self.tag)
            raise BenchmarkError(msg)

    def _run(self):
        pass

    def start_clock(self):
        self.timer = time.time()

    def stop_clock(self):
        diff = time.time() - self.timer
        self.report.append(diff)
        return diff

    def setup(self):
        pass

    def teardown(self):
        pass

class Connect(BaseBenchmark):

    description = "Connect Benchmark"
    tag = "basic_connect"
    group = "basic"

    def __init__(self, dbi, callback, runs=1, duration=60,
                 name=None, config={}):
        super(Connect, self).__init__(
            dbi, callback, runs=runs, name=name,
            config=config, duration=duration)

    def _run(self):
        self.report = []
        success = 0
        fail = 0
        for i in range(self.runs):
            try:
                self.start_clock()
                cnx = self.dbi.connect(**self.config)
                self.stop_clock()
            except StandardError as e:
                print("Connection failed: %s" % (e))
                fail += 1
            else:
                success += 1
                cnx.close()

class Select(BaseBenchmark):

    description = "Select Benchmark"
    tag = "basic_select"
    group = "basic"

    def __init__(self, dbi, callback, runs=1, duration=60,
                 name=None, config={}):
        super(Select, self).__init__(
            dbi, callback, runs=runs, name=name,
            config=config, duration=duration)

    def _run(self):
        self.report = []
        success = 0
        fail = 0
        for i in range(self.runs):
            try:
                self.start_clock()
                cnx = self.dbi.connect(**self.config)
                cur = cnx.cursor()
                cur.execute("SELECT * FROM mysql.time_zone_name LIMIT 1")
                cur.fetchall()
                cnx.close()
                self.stop_clock()
            except StandardError as e:
                print("Connection failed: %s" % (e))
                fail += 1
            else:
                success += 1

class ExecuteManyInsert(BaseBenchmark):

    description = "Insert using MySQLCursor.executemany()"
    tag = "cpy_executemany_insert"
    group = "cpy"

    _insert_stmt = "INSERT INTO {table} (c1,c2,c3) VALUES (%s, %s, %s)"

    def setup(self):
        cnx = self.dbi.connect(**self.config)
        cnx.cmd_query("DROP TABLE IF EXISTS {table}".format(
            table=self.tag))
        cnx.cmd_query("CREATE TABLE {table} ("
                      "  id INT UNSIGNED AUTO_INCREMENT,"
                      "  c1 VARCHAR(30),"
                      "  c2 VARCHAR(300),"
                      "  c3 INT,"
                      "  PRIMARY KEY (id)"
                      ") ENGINE=InnoDB".format(table=self.tag))
        cnx.close()

    def teardown(self):
        cnx = self.dbi.connect(**self.config)
        cnx.cmd_query("DROP TABLE IF EXISTS {table}".format(table=self.tag))
        cnx.close()

    def _run(self):
        self.report = []
        success = 0
        fail = 0
        values = (
            'c1' * 15,  # c1
            'c2' * 150,  # c2
            1234,  # c3
        )
        cnx = self._get_connection()
        cur = cnx.cursor()
        stmt = self._insert_stmt.format(table=self.tag)
        for i in range(self.runs):
            try:
                self.start_clock()
                cur.executemany(stmt, [values]*1000)
                cnx.commit()
                self.stop_clock()
            except StandardError as exc:
                print("{tag} failed: {err}".format(tag=self.tag, err=exc))
                fail += 1
            else:
                success += 1
        cnx.close()


class ExecuteManyInsertNotOptimized(ExecuteManyInsert):

    description = "Insert using MySQLCursor.executemany() w/o optimizations"
    tag = "cpy_executemany_insert_not_optimized"
    group = "cpy"

    _insert_stmt = "INSERT INTO {table} (c1,/*c2*/c2,c3) VALUES (%s, %s, %s)"

class EmployeesCachedSelect(BaseBenchmark):

    description = "Employees Cached Select Benchmark"
    tag = "employees_cached_select"
    group = "employees"

    def __init__(self, dbi, callback, runs=1, duration=60,
                 name=None, config={}):
        super(EmployeesCachedSelect, self).__init__(
            dbi, callback, runs=runs, name=name,
            config=config, duration=duration)

    def _run(self):
        self.report = []
        success = 0
        fail = 0
        cnx = self.dbi.connect(**self.config)
        cur = cnx.cursor()
        query = ("SELECT * FROM employees.employees "
                 "WHERE emp_no BETWEEN 10000 AND 11000")
        for i in range(self.runs):
            try:
                self.start_clock()
                cur.execute(query)
                cur.fetchall()
                self.stop_clock()
            except StandardError as exc:
                print("SELECT failed: {0}".format(exc))
                fail += 1
            else:
                success += 1


class EmployeesRandomSelect(BaseBenchmark):

    description = "Employees Random Select Benchmark"
    tag = "employees_random_select"
    group = "employees"

    def __init__(self, dbi, callback, runs=1, duration=60,
                 name=None, config={}):
        super(EmployeesRandomSelect, self).__init__(
            dbi, callback, runs=runs, name=name,
            config=config, duration=duration)

    def _run(self):
        self.report = []
        success = 0
        fail = 0
        cnx = self.dbi.connect(**self.config)
        cur = cnx.cursor()
        query = "SELECT * FROM employees.employees WHERE emp_no = %s"
        for i in range(self.runs):
            try:
                emp_no = random.randint(10000, 499999)
                self.start_clock()
                cur.execute(query, (emp_no,))
                cur.fetchone()
                self.stop_clock()
            except StandardError as exc:
                print("SELECT failed: {0}".format(exc))
                fail += 1
            else:
                success += 1

class BaseSysQABenchmarks(BaseBenchmark):

    database = "cpy_bench_sysqa"
    tag = "sysqa_benchmarks"
    engine = "InnoDB"

    tables = {
        'account': (
            "CREATE TABLE IF NOT EXISTS {database}.{table} ( "
            "aid INT, bid INT, balance DECIMAL(8,2), "
            "filler CHAR(80)"
            ") ENGINE={engine}"
            ),
        'history': (
            "CREATE TABLE IF NOT EXISTS {database}.{table} ("
            "id BIGINT NOT NULL AUTO_INCREMENT, "
            "aid INT, tid INT, bid INT, filler CHAR(80), "
            "PRIMARY KEY (id))ENGINE={engine}"
            ),
        }

    def setup_ddl(self):
        self.cnx.cmd_query("CREATE DATABASE IF NOT EXISTS {database}".format(
            database=self.database))

        for tablename, sql in self.tables.items():
            self.cnx.cmd_query(sql.format(
                table=tablename,
                database=self.database,
                engine=self.engine)
                )

    def populate_account(self, cur):
        # Populate account table
        sql = (
            "INSERT INTO {database}.account "
            "VALUES (%s, %s, 0.0, 'linkin')").format(database=self.database)
        i = 1
        while i <= 1000:
            cur.execute(sql, (i, i,))
            i += 1

    def setup(self):
        if self.duration < 10 or self.duration > 2 * 60:
            raise BenchmarkError("Duration should be between 10 and 120 sec")
        config = self.config
        self.cnx = self.dbi.connect(**config)
        try:
            self.cnx.database = self.database
        except self.dbi.ProgrammingError as exc:
            self.setup_ddl()
        else:
            for tablename, _ in self.tables.items():
                self.cnx.cmd_query("TRUNCATE {database}.{table}".format(
                    table=tablename,
                    database=self.database)
                    )

        self.populate_account(self.cnx.cursor())
        self.cnx.commit()

    def teardown(self):
        pass
        #self.cnx.cmd_query("DROP DATABASE {database}".format(
        #    database=self.database))


class SysQASelectCached(BaseSysQABenchmarks):

    description = "SysQA Cached Select (TPS)"
    tag = "sysqa_select_cached"
    group = "sysqa"
    report_type = 'tps'

    def _run(self):
        self.report = []
        runs = self.runs
        aid = random.randint(1, 1000)
        sql = "SELECT balance FROM {database}.account WHERE aid = {aid}"
        cur = self.cnx.cursor()

        query = sql.format(database=self.database, aid=aid)

        for i in range(self.runs):
            sys.stdout.write('.')
            sys.stdout.flush()
            stop_time = time.time() + self.duration
            query_count = 0
            while time.time() < stop_time:
                cur.execute(query)
                cur.fetchone()
                query_count += 1
            self.report.append(round(query_count/self.duration, 0))
        sys.stdout.write('\n')
        sys.stdout.flush()


class SysQASelectRandom(BaseSysQABenchmarks):

    description = "SysQA Random Select (TPS)"
    tag = "sysqa_select_random"
    group = "sysqa"
    report_type = 'tps'

    def _run(self):
        self.report = []
        runs = self.runs
        sql = "SELECT balance FROM {database}.account WHERE aid = %s"
        cur = self.cnx.cursor()

        query = sql.format(database=self.database)

        for i in range(self.runs):
            sys.stdout.write('.')
            sys.stdout.flush()
            stop_time = time.time() + self.duration
            query_count = 0
            while time.time() < stop_time:
                cur.execute(query, (random.randint(1, 1000),))
                cur.fetchone()
                query_count += 1
            self.report.append(round(query_count/self.duration, 0))
        sys.stdout.write('\n')
        sys.stdout.flush()
