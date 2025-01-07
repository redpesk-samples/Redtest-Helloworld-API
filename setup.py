"""
*File:* setup.py
*Author: * Armand BENETEAU <armand.beneteau@iot.bzh>
*Date:* 06/03/2020

*Description:*
    Setup file needed for Python packaging

*License:*
    *Copyright (C) 2019-2025 IoT.bzh Company*

    *Licensed under the Apache License, Version 2.0 (the "License");\
    you may not use this file except in compliance with the License.\
    You may obtain a copy of the License at:*

    *http://www.apache.org/licenses/LICENSE-2.0*

    *Unless required by applicable law or agreed to in writing, software\
    distributed under the License is distributed on an "AS IS" BASIS,\
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or\
    implied.*
    *See the License for the specific language governing permissions and\
    limitations under the License.*
"""
from setuptools import setup

setup(name='redtest_helloworld_api',
      version='1.0',
      description='Python API project that can be used as an example on how to implement Redtests in a project',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
      ],
      url='http://git.ovh.iot/redpesk/redtest-helloword-api',
      author='Armand Bénéteau',
      author_email='armand.beneteau@iot.bzh',
      license='Apache 2.0',
      packages=['redtest_helloworld_api'],
      python_requires='>=3.6',
      install_requires=[
         'aiohttp',
      ],
      scripts=['redtesthelloworldd'],
      zip_safe=False)
