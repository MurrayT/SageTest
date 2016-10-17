"""
This module holds the functionality for generating an assignment
"""

from __future__ import print_function, absolute_import
import types
import random
import logging
from .misc import lambda_re, ensure_path, GRADING, REVEALED
from . import templates


class PreTestCase(object):
    """This holds input, handler, and show value for each test case"""

    def __init__(self, input_value, handler, show=True):
        self.input_value = input_value
        self.handler = handler
        self.show = show

    def input_string(self):
        return "%s" % repr(self.input_value)

    def expected_string(self):
        if isinstance(self.handler, types.StringType) and lambda_re.match(self.handler):  # pylint: disable=E1101
            return self.handler
        else:
            return "%s" % repr(self.handler)


class Problem(object):
    """This holds a single problem with generator and handler"""

    def __init__(self, function_name, input_vars, help_text, default, show_threshold, timeout):
        self.function_name = function_name
        self.input_vars = input_vars
        self.help_text = help_text
        self.default = default
        self.cases = []
        self.show_threshold = show_threshold
        self.timeout = timeout

    def add_case(self, input_value, handler):
        self.cases.append(PreTestCase(input_value, handler,
                                      random.random() < self.show_threshold))

    def inputs_strings(self):
        all_str = "\t'%s': {\n" % self.function_name
        revealed_str = all_str
        for index, case in enumerate(self.cases, 1):
            if case.show:
                revealed_str += "\t\t%d: " % index + case.input_string() + ",\n"
            all_str += "\t\t%d: " % index + case.input_string() + ",\n"
        all_str += "\t},\n"
        revealed_str += "\t},\n"
        return all_str, revealed_str

    def expected_strings(self):
        all_str = "\t'%s': {\n" % self.function_name
        revealed_str = all_str
        for index, case in enumerate(self.cases, 1):
            if case.show:
                revealed_str += "\t\t%d: " % index + case.expected_string() + ",\n"
            all_str += "\t\t%d: " % index + case.expected_string() + ",\n"
        all_str += "\t},\n"
        revealed_str += "\t},\n"
        return all_str, revealed_str

    def timeout_str(self):
        return ("\t'%s': %d,\n" % (self.function_name, self.timeout),)

    def get_template(self):
        args = ", ".join(self.input_vars)
        return templates.function_template.format(function_name=self.function_name,
                                                  args=args,
                                                  help_string=self.help_text,
                                                  default_val=self.default)


class ProblemSet(object):
    """Main class for creating the problem set.
    This class does all the outer heavy lifting."""

    def __init__(self, name):
        self.name = name
        self.problems = []

    def add_problem(self, problem):
        self.problems.append(problem)

    def name_strings(self):
        return "functions = {\n\t" + ",\n\t".join('"{fn}": {fn}'.format(fn=problem.function_name) for problem in self.problems) + "\n}\n\n"

    def method_writer(self, file, name, method, index, end="\n\n"):
        """
        Writes a specific piece of information for each of the test cases to the given file handle
        calling a method.
        """
        logging.info("Writing %s.", name)
        # print("%s = {\n" % name, end="")
        file.write("%s = {\n" % name)
        for problem in self.problems:
            logging.info("Writing %s for %s", name, problem.function_name)
            # print(method(problem)[index],end="")
            file.write(method(problem)[index])
        # print("}\n\n",end="")
        file.write("}%s" % end)

    def testcase_file_writer(self, filet, vis, output_location):
        logging.info("Writing %s testcases to: %s/%s_%s.sage",
                     filet, output_location, self.name, filet)
        with open("%s/%s_%s.sage" % (output_location, self.name, filet), 'w') as thisfile:
            logging.info("Writing function names.")
            # print(self.name_strings(), end="")
            thisfile.write(self.name_strings())
            self.method_writer(thisfile, "inputs", Problem.inputs_strings, vis)
            self.method_writer(thisfile, "expected_values",
                               Problem.expected_strings, vis)
            self.method_writer(thisfile, "timeouts",
                               Problem.timeout_str, 0, end="")

    def solutions_file_writer(self, output_location):
        logging.info("Writing solutions to: %s/%s_solutions.sage",
                     output_location, self.name)
        with open("%s/%s_solutions.sage" % (output_location, self.name), 'w') as thisfile:
            # print(templates.top_stub, end="")
            thisfile.write(templates.top_stub)
            thisfile.write("\n\n".join(problem.get_template()
                                       for problem in self.problems))

    def write_problem_set(self, output_location="output", secondary_location="../../Assignments"):
        logging.basicConfig(level=logging.INFO)
        output_dir = ensure_path(output_location)
        self.testcase_file_writer("grading", GRADING, output_dir)
        self.testcase_file_writer("revealed", REVEALED, output_dir)
        self.solutions_file_writer(output_location)
