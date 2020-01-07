import os
import unittest
from coverage import Coverage

test_dir = os.path.join(os.getcwd(), 'flaskblog')
loader = unittest.TestLoader()
test_suite = loader.discover(test_dir, pattern='test_*.py', 
                            top_level_dir=os.getcwd())
runner = unittest.TextTestRunner()
cov = Coverage()
cov.set_option('run:source', ['flaskblog'])
cov.start()
runner.run(test_suite)
cov.stop()
cov.report()