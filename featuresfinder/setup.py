
"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Sachin Limbachiya",
    author_email="sachinlimbachiya10@gmail.com",
    name='featuresfinder',
    license="MIT",
    description='featuresfinder is a python package for feature extration using nearly 6 different algorithsm.',
    version='v0.0.1',
    long_description=README,
    url='https://github.com/sachinL/featuresfinder',
    packages=setuptools.find_packages(),
    python_requires=">=3",
    install_requires=['sklearn','lightgbm','numpy'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)