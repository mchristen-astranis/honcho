import os
import re
import unittest
from honcho.procfile import Procfile
from subprocess import Popen, PIPE

TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
FIXTURE_ROOT = os.path.join(TEST_ROOT, 'fixtures')


class TestCase(unittest.TestCase):

    if not hasattr(unittest.TestCase, 'assertRegexpMatches'):
        def assertRegexpMatches(self, text, expected_regex, msg=None):  # noqa
            """Fail the test unless the text matches the regular expression."""
            if isinstance(expected_regex, (str, bytes)):
                assert expected_regex, "expected_regex must not be empty."
                expected_regex = re.compile(expected_regex)
            if not expected_regex.search(text):
                msg = msg or "Regex didn't match"
                msg = '%s: %r not found in %r' % (
                    msg,
                    expected_regex.pattern,
                    text)
                raise self.failureException(msg)

    if not hasattr(unittest.TestCase, 'assertNotRegexpMatches'):
        def assertNotRegexpMatches(self, text, unexpected_regex, msg=None):  # noqa
            """Fail the test if the text matches the regular expression."""
            if isinstance(unexpected_regex, (str, bytes)):
                unexpected_regex = re.compile(unexpected_regex)
            match = unexpected_regex.search(text)
            if match:
                msg = msg or "Regex matched"
                msg = '%s: %r matches %r in %r' % (
                    msg,
                    text[match.start():match.end()],
                    unexpected_regex.pattern,
                    text)
                raise self.failureException(msg)


def get_honcho_output(args):
    os.chdir(FIXTURE_ROOT)
    cmd = ['honcho']
    cmd.extend(args)

    # The below is mostly copy-pasted from subprocess.py's check_output (to
    # support python 2.6)

    process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output, error = process.communicate()
    retcode = process.returncode

    return retcode, output, error


def get_procfile(name):
    with open(os.path.join(FIXTURE_ROOT, name)) as f:
        return Procfile(f.read())
