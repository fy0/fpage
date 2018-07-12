"""
setup.py for fpage
https://github.com/fy0/fpage
"""

from setuptools import setup


def description():
    return """FPage is a tornado classic project generator(cli)."""


def long_desc():
    return """FPage is a tornado classic project generator(cli).

classic means the style before separation of front-end and backend beca me popular.

Quick start a project with tornado + mako/jinja2 + peewee/sqlalchemy。

Usage: fpage new

`more <https://github.com/fy0/fpage/blob/master/README_EN.md>`_ """

setup(
    name='fpage',
    version='1.2.1',

    description=description(),
    long_description=long_desc(),
    url="https://github.com/fy0/fpage",

    author='fy',
    author_email='fy0748@gmail.com',
    license='WTFPL',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
    
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='tornado generator cli web framework sqlalchemy peewee',
    platforms='any',

    install_requires=[],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4', 

    packages=['fpage'],
    package_dir={
        'fpage': '',
    },
    include_package_data=True,

    extras_require={
        'full': ['tornado', 'peewee', 'sqlalchemy', 'mako', 'jinja2'],
    },

    entry_points={
        'console_scripts': [
            'fpage=fpage.fpage:main',
        ],
    },
)
