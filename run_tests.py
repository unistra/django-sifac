# -*- coding: utf-8 -*-

import sys
from django.test.utils import get_runner
from django.utils import unittest
from django.conf import settings

loader = unittest.TestLoader()
extra_suite = unittest.TestSuite(tests=loader.discover('tests/'))

test_runner = get_runner(settings)(verbosity=2, interactive=True)
failures = test_runner.run_tests(['sifac'], extra_tests=extra_suite)
sys.exit(failures)
