#!/bin/bash

python3 manage.py runsslserver '0.0.0.0:8000' --key localhost.key --cert localhost.crt
