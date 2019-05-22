"""
Standalone test runner script using the minimum settings required for tests to execute.
"""

import os
import sys


def run_tests():
    # Setup env to use the test settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    from django.conf import settings

    # Call django.setup() to initialize the application registry and other bits:
    import django
    django.setup()

    # Instantiate a test runner
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)

    # Run tests and return the results.
    test_runner = TestRunner(verbosity=2, interactive=False)
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    run_tests()
