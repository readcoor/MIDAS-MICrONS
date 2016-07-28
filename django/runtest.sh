#!/bin/bash

# run just one test
# python3 manage.py test nada.tests.test_nda_icd.NdaIcdTestCase.test_S9_voxel_list

# run just one test class
# python3 manage.py test nada.tests.test_boss.TheBossTestCase

# run all tests in module nada.tests
python3 manage.py test nada.tests

