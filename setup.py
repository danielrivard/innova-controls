"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="innova-controls",
    version="1.0.4",
    description="Innova Air Conditioner Control API",
    license="Apache",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielrivard/innova-controls",
    author="Daniel Rivard",
    # author_email='author@example.com',  # Optional
    # https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    keywords="development, home automation, library, innova",
    package_dir={"": "src"},
    py_modules=["innova_controls"],
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.9, <4",
    install_requires=["requests>=2.27.1", "retry2>=0.9.3"],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/danielrivard/innova-controls/issues",
        "Source": "https://github.com/danielrivard/innova-controls/",
    },
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
)
