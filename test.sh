#!/bin/sh -e

source ./venv/bin/activate
coverage erase
if [ "${1}" = "tox" ] ; then
  tox
else
  detox
fi

coverage combine *.coverage
coverage report -m
deactivate
