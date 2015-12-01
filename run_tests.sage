#To import use 'runfile ('run_tests.sage')'
#Functions, inputs, expected and timeouts are dictionaries, with inputs and expected being dicts of dicts.
#'testRunner(TestCase.buildTestCases())' will build testcases and run from module level dictionaries.
"""Tests.sage: Allows testing of arbitrary functions to see if input matches expected output.
   Also fully python 2.7.8 safe.
"""

import datetime  #have to change the name of the module so as not shadow sage's time function
                        #(Who in their right mind shadows builtin module names?).
import signal
import sys

__author__ = "Murray Tannock"
__license__ = "THE BEER-WARE LICENSE"
__version__ = 1.1
__email__ = "murray14@ru.is"

# --------------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <murraytannock@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Murray Tannock
# --------------------------------------------------------------------------------



class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError

class TestCase(object):
    """ Class for each test case
    This defines a test case as a function, a dict of inputs, and a dict of expected outputs.

    It records the number of tests, failures, timeouts, and the total time spent testing

    Initialised with the function, the input dictionary, and the expected dictionary
    """
    def __init__(self, function, inputs, expected, maxtime):
        self.function = function
        self.inputs = inputs
        self.expected = expected
        self.maxtime = maxtime
        self.tests = 0
        self.failures = 0
        self.timeouts = 0
        self.time = 0
        self.timeouttime = 0

    def test(self, verb=True, showfails=5, superverb=False, grading=False):
        """
        Runs a specific test case, and prints results to stdout
        verb flag can be used to suppress output.
        """
        self.tests = 0
        self.failures = 0
        self.timeouts = 0
        self.time = 0
        self.timeouttime = 0
        time = None
        timeouttime = 0
        if verb:
            print "---"
            print "Testing %s:" % self.function.__name__
            sys.stdout.flush()
        assert(len(self.inputs)==len(self.expected))
        for k in self.expected:
            timeouttime = 0
            expected_is_func = type(self.expected[k]) == type(lambda z:z)
            has_multiple_inputs = (type(self.inputs[k]) == tuple)
            try:
                t_ = datetime.datetime.now()
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(self.maxtime)
                if expected_is_func: #allows passing a function to use for verification, instead of comparing
                                     #to expected output, passes output into a function and expects true in response
                    if has_multiple_inputs: #allows functions with multiple input
                        assert(self.expected[k](self.function(*self.inputs[k])))
                    else:
                        assert(self.expected[k](self.function(self.inputs[k])))
                else:
                    if has_multiple_inputs: #allows functions with multiple input
                        assert(self.function(*self.inputs[k])==self.expected[k])
                    else:
                        assert(self.function(self.inputs[k])==self.expected[k])
            except AssertionError:
                self.failures += 1
                if verb:
                    if self.failures <= showfails:
                        print "Test %d failed." % int(self.tests+1),
                        if superverb:
                            print "Input: " + str(self.inputs[k]),
                        print ""
            except (KeyboardInterrupt, TimeoutError):
                self.failures += 1
                self.timeouts += 1
                t2_ = datetime.datetime.now()
                timeouttime = t2_-t_
                if verb:
                    print "Test %d interrupted after %.4f s" % (self.tests+1, timeouttime.seconds+timeouttime.microseconds/10^6)
            except Exception:
                self.failures += 1
                if not grading:
                    raise
            finally:
                signal.alarm(0)
                self.tests += 1
                time = datetime.datetime.now()-t_
                self.time += time.seconds + time.microseconds / 10^6
                if not timeouttime == 0:
                    self.timeouttime += timeouttime.seconds + timeouttime.microseconds / 10^6
        if verb:
            print "Tests complete: %d of %d passed (%d failure(s))" %(self.tests - self.failures, self.tests, self.failures)
            if not self.tests-self.timeouts == 0:
                print "Time taken for non-timeout tests: %.4f ms (%.4f ms average)" % ((self.time-self.timeouttime)*1000, (self.time-self.timeouttime)/(self.tests-self.timeouts)*1000)
            if self.timeouts > 0:
                print "Timeouts: %d"% self.timeouts
            sys.stdout.flush()
        if grading:
           return {self.function.__name__: (int(self.tests - self.failures),int(test.tests))}

    @staticmethod
    def buildTestCases(usrs=None, funs=None, ins=None, expt=None, mtimes=None):
        """ Builds Test cases. Returns a generator over the test cases.

        Keyword arguments allow passing in of desired dictionaries for each values.
        Note: the three dictionaries must have identical immutable keys. (No lists)

        If no arguments are passed function will attempt to use module level variables 'functions',
        'inputs' and 'expected' for the source for test cases.

        functions with multiple arguments require arguments to be passed in the input dictionary as tuples to allow
        for unpacking when tests are run.

        """
        if not usrs:
            try:
                usrs = userids
                if len(users) < 1:
                    raise RuntimeError("Users not defined")

        if not funs and not ins and not expt and not mtimes:
            try:
                funs = functions
                ins = inputs
                expt = expected
                mtimes = maxtimes

            except NameError: #raises an error if no input is given and any of the module level
                              #variables are undefined. (Should probably catch type errors here to)
                raise

        return (TestCase(funs[i], ins[i], expt[i], mtimes[i]) for i in funs)

def testRunner(test_cases, verb=True, showfails=5, superverb=False, grading=False):
    """Runs test cases contained inside an iterable object passed in and prints result.

       verb flag can be used to suppress non-vital output.
    """
    if verb:
        print "Beginning tests"

    functions_tested = 0
    tests_completed = 0
    failures = 0
    timeouts = 0
    time = 0
    timeouttime = 0
    for case in test_cases:
        case.test(verb=verb, showfails=showfails, superverb=superverb, grading=grading)
        failures += case.failures
        tests_completed += case.tests
        timeouts += case.timeouts
        functions_tested += 1
        time += case.time
        timeouttime += case.timeouttime
    if verb:
        print "---"
    print "Results:"
    print "%d Functions tested" % functions_tested
    print "%d of %d tests passed (%d failure(s))" %(tests_completed - failures, tests_completed, failures)
    success_rate = (tests_completed-failures)/float(tests_completed)
    print "Success rate: %.2f %%" % (success_rate*100)
    if timeouts > 0:
        print "%d timeouts" % timeouts
    print "Total time: %.4f ms. (%.4f ms on timeouts, %.4f ms on completed tests)" % (time*1000, timeouttime*1000, (time-timeouttime)*1000)
