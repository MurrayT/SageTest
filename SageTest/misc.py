"""
This module hold the things that don't fit into the other categories
"""


class OvertimeError(Exception):
    """Exception raised by test runner on test timeout"""
    pass


def timeout_handler(signum, frame):
    """Handler called on alarm signal from test timeout"""
    raise OvertimeError()
