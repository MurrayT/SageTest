"""
This module hold the things that don't fit into the other categories
"""
import re
import os
import errno


class OvertimeError(Exception):
    """Exception raised by test runner on test timeout"""
    pass


def timeout_handler(signum, frame):
    """Handler called on alarm signal from test timeout"""
    raise OvertimeError()

lambda_re = re.compile(r"^lambda")

def ensure_path(path):
    '''
    Check if the directory at path exists,
    if not, create it
    Source: http://stackoverflow.com/questions/273192/in-python-check-if-a-\
            directory-exists-and-create-it-if-necessary
    '''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return path

GRADING=0
REVEALED=1