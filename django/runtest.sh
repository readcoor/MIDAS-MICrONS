#!/bin/bash

# run just one test
# python3 manage.py test nada.tests.test_nda_icd.NdaIcdTestCase.test_SA2_neuron_celltype
# python3 manage.py test nada.tests.test_objs.FixturesTestCase.test_neuron_activity

# run just one test class
# python3 manage.py test nada.tests.test_boss.TheBossTestCase

# run all tests in module nada.tests
python3 manage.py test nada.tests

