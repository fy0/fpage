#!/usr/bin/env python
# coding:utf-8

import re
import os
import sys
import shutil
from sys import argv
from os.path import join
py_major_ver = sys.version_info[0]

src_dir = os.path.abspath(sys.path[0])

def help():
    print('FPage - tornado project generator')
    print('Usage:')
    print('  fpage <command>')
    print('')
    print('Commands:')
    print('  startapp')
    print('  help')
    print('')

def startapp():
    global input  # fix4py3
    if py_major_ver == 2:
        input = raw_input
    project_name = input('Project Name:')
    tmpl_engine = input('Template Engine [M/J/T]:').lower()
    db_orm = input('Database ORM [S/P]:').lower()

    if len(project_name) == 0 or ' ' in project_name:
        print('Invalid Project Name.')
        return

    if tmpl_engine in ['', 'm']:
        tmpl_engine = 'mako'
    elif tmpl_engine in ['j', 'jinja', 'jinja2']:
        tmpl_engine = 'jinja2'
    elif tmpl_engine in ['t', 'tornado']:
        tmpl_engine = 'tornado'
    else:
        print('Invalid Value.')
        return

    if db_orm in ['', 's', 'sqlalchemy']:
        db_orm = 'sqlalchemy'
    elif db_orm in ['p', 'peewee']:
        db_orm = 'peewee'
    else:
        print('Invalid Value.')
        return
        
    print('')
    print('   Project Name: %s' % project_name)
    print('Template Engine: %s' % tmpl_engine)
    print('   Database ORM: %s' % db_orm)
    print('')
    sure = input('Sure (Y/n)?')

    if sure == 'n':
        return

    project_dir = project_name
    shutil.copytree(join(src_dir, 'src'), project_dir)

    if tmpl_engine == 'mako':
        shutil.rmtree(join(project_dir, 'templates_jinja2'))
        shutil.rmtree(join(project_dir, 'templates_tornado'))
    elif tmpl_engine == 'jinja2':
        shutil.rmtree(join(project_dir, 'templates'))
        shutil.rmtree(join(project_dir, 'templates_tornado'))
        shutil.move(join(project_dir, 'templates_jinja2'), join(project_dir, 'templates'))
    elif tmpl_engine == 'tornado':
        shutil.rmtree(join(project_dir, 'templates'))
        shutil.rmtree(join(project_dir, 'templates_jinja2'))
        shutil.move(join(project_dir, 'templates_tornado'), join(project_dir, 'templates'))

    if db_orm == 'sqlalchemy':
        shutil.rmtree(join(project_dir, 'model_peewee'))
    elif db_orm == 'peewee':
        shutil.rmtree(join(project_dir, 'model'))
        shutil.move(join(project_dir, 'model_peewee'), join(project_dir, 'model'))
    
    config_file = join(project_dir, 'config.py')
    txt = open(config_file).read()
    txt = txt.replace("TITLE = 'FPage'", "TITLE = '%s'" % project_name)
    txt = txt.replace("TEMPLATE = 'mako'", "TEMPLATE = '%s'" % tmpl_engine)
    open(config_file, 'w+').write(txt)
    print('Done.')

    
if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == 'help':
            help()
        elif argv[1] == 'startapp':
            startapp()
        else:
            help()
    else:
        help()

