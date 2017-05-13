#!/usr/bin/env bash

coverage run --source='.' manage.py test --junitxml results.xml
coverage report
coverage html