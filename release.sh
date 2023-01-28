#!/bin/bash
rm -rf ./dist/* ./build/
python setup.py build sdist bdist_wheel
twine upload dist/*