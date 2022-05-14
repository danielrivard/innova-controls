#!/bin/bash
rm ./dist/*
python setup.py build sdist bdist_wheel
twine upload dist/*