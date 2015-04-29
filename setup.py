#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    MULTIBOX - This program is a frontend to DropboxD that
#     enables you to access more than one Dropbox at a time.
#    Copyright (C) 2015 Paul Hofmann
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
###############################################
#                    Setup                    #
###############################################

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup
import multibox

setup(
    name='multibox',
    version=multibox.__version__,

    description='This program is a frontend to DropboxD that enables you to access more than one Dropbox at a time.',
    author='Paul Hofmann',
    author_email='p.h.o@web.de',
    license='GPLv3',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        
        'Environment :: Console',
        'Environment :: X11 Applications :: GTK',
        
        'Natural Language :: English',
        
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        
        'Topic :: System :: Archiving',
        'Topic :: Utilities',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    py_modules=['multibox'],

    entry_points={
        'console_scripts': [
            'multibox=multibox:main_wrap',
        ],
    },
)
