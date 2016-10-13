#!/usr/bin/env python

"""
Runs test from tests directory
"""

import coverage
COV = coverage.coverage(branch=True, include='app/*')
COV.start()

import unittest
suite = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(suite)

COV.stop()
COV.report()
