"""
This module holds all the models, and main functionality for the testing component of
the system for testing in SageMathCloud
"""
from __future__ import print_function, absolute_import
import sys
import types
import signal
import datetime
from .misc import timeout_handler, OvertimeError


class TestCase(object):
    """A test case holds the input and output expected values for a
    single test."""

    def __init__(self, input_value, expected_value):
        self.input_value = input_value
        self.expected = expected_value

    def __repr__(self):
        return "TestCase(%s, %s)" % (repr(self.input_value), repr(self.expected))

    def __str__(self):
        return "Input: %s" % str(self.input_value)

    @property
    def expected_is_func(self):
        """Returns whether the expected value is a function, or whether it
        has some other value"""
        return isinstance(self.expected, types.FunctionType)

    @property
    def input_type(self):
        """Returns a different int value for each possible input type
        tuple: 1
        empty input: -1
        any other input: 0
        """
        return (int(isinstance(self.input_value, tuple))
                if self.input_value else -1)

    def run_case(self, function):
        """Runs the provided function on the particular testcase"""
        if self.input_type == 1:
            return function(*self.input_value)
        elif self.input_type == -1:
            return function()
        else:
            return function(self.input_value)

    def check_case(self, function, fuzzy):
        """Checks the specific testcase with the function provided and the fuzzy value"""
        output = self.run_case(function)
        if self.expected_is_func:
            assert self.expected(output)
        elif fuzzy:
            assert abs(self.expected - output) <= fuzzy
        else:
            assert output == self.expected


class TestSet(object):
    """This holds a test Set. This is replaces the old testcase class in
    order to abstract the functionality"""

    def __init__(self, function, cases, maxtime, fuzzy=None):
        self.function = function
        self.cases = cases
        self._fuzzy_value = fuzzy
        self.maxtime = maxtime

    @property
    def fuzzy(self):
        """This property either returns the fuzzy limit (error) or False
        if the TestSet is looking for either exact values or has a function"""
        if self._fuzzy_value is not None:
            return self._fuzzy_value
        else:
            return False

    def __len__(self):
        return len(self.cases)

    def __iter__(self):
        return iter(self.cases)

    def test(self, case, casenum=0, verb=0, grading=False):
        """Runs a specific test case, casenum is only there for output"""
        timeout_time = datetime.timedelta()
        try:
            time_start = datetime.datetime.now()
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.maxtime)
            case.check_case(self.function, self.fuzzy)
        except AssertionError:
            fail = 1
            timeout = 0
            if verb:
                print("Test %d failed." % casenum, end="")
                if verb > 1:
                    print(str(case), end="")
                print("")
        except (KeyboardInterrupt, OvertimeError):
            fail = 1
            timeout = 1
            time_end = datetime.datetime.now()
            timeout_time = time_end - time_start
            if verb:
                interp = (casenum,
                          timeout_time.seconds +
                          timeout_time.microseconds / 10 ^ 6)
                print("Test %d interrupted after %.4f s" % interp)
        except Exception:  # pylint: disable=broad-except
            fail = 1
            timeout = 0
            if not grading:
                raise
        finally:
            fail = 0
            signal.alarm(0)
            time_total = datetime.datetime.now()-time_start
            time = time_total.seconds + time_total.microseconds / 10 ^ 6
            if timeout_time != 0:
                timeout_time += (timeout_time.seconds +
                                 timeout_time.microseconds / 10 ^ 6)
            else:
                timeout = 0
        return (fail, timeout, time, timeout_time)


class TestRun(object):
    """
    Class to hold the test sets.

    It records the number of tests, failures, timeouts, and the total time
    spent testing"""

    def __init__(self, test_set):
        self.test_set = test_set
        self.tests = 0
        self.failures = 0
        self.timeouts = 0
        self.time = 0
        self.timeout_time = 0

    def test(self, verb=1, showfails=5, grading=False):
        """
        Runs a specific test set, and prints results to stdout
        verb flag can be used to suppress output.
        """
        self.tests = 0
        self.failures = 0
        self.timeouts = 0
        self.time = 0
        self.timeout_time = 0
        if verb:
            print("---")
            print("Testing %s:" % self.test_set.function.__name__)
            sys.stdout.flush()
        for casenum, case in enumerate(self.test_set):
            modverb = (0 if self.failures > showfails else verb)
            fail, timeout, time, timeout_time = self.test_set.test(
                case, casenum, modverb, grading)
            self.tests += 1
            self.failures += fail
            self.timeouts += timeout
            self.time += time
            self.timeout_time += timeout_time
        if verb:
            results = (self.tests - self.failures, self.tests, self.failures)
            print("Tests complete: %d of %d passed (%d failure(s))" % results)
            if not self.tests-self.timeouts == 0:
                timeoutresults = ((self.time - self.timeout_time) * 1000,
                                  (self.time - self.timeout_time) /
                                  (self.tests - self.timeouts) * 1000)
                print("Time taken for non-timeout tests: %.4f ms"
                      "(%.4f ms average)" % timeoutresults)
            if self.timeouts > 0:
                print("Timeouts: %d" % self.timeouts)
            sys.stdout.flush()
        if grading:
            return {self.test_set.function.__name__: (int(self.tests - self.failures),
                                                      int(self.tests))}
