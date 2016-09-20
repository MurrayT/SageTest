"""
This module holds the functionality for generating an assignment
"""

from __future__ import print_function, absolute_import
import types
import random


class PreTestCase(object):
    """This holds input, handler, and show value for each test case"""

    def __init__(self, input_value, handler, show=True):
        self.input_value = input_value
        self.handler = handler
        self.show = show

    def input_string(self):
        return "%s" % self.input_value

    def expected_string(self):
        if isinstance(self.handler, types.StringType):
            return self.handler
        else:
            return "%s" % self.handler


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
        all_str = "\t%s: {\n" % self.function_name
        revealed_str = all_str
        for index, case in enumerate(self.cases, 1):
            if case.show:
                revealed_str += "\t\t %d:" % index + case.input_string() + ",\n"
            all_str += "\t\t %d:" % index + case.input_string() + ",\n"
        all_str += "\t},\n"
        revealed_str += "\t},\n"
        return all_str, revealed_str

    def expected_strings(self):
        all_str = "\t%s: {\n" % self.function_name