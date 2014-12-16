#!/usr/bin/env python
# encoding: utf-8

from fabric.api import local, cd, run, put, env

# env.hosts = [ '114.215.209.188' ]
env.hosts = [ '115.29.241.227' ]
env.user = 'sim'
env.key_filename = '~/.ssh/id_rsa.pub'

def deploy():
    local('python setup.py bdist_egg', capture=False)
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s-py2.6.egg'%dist, '/home/sim/tmp/%s-py2.6.egg'%dist)
    run('/home/sim/opt/simenv/bin/easy_install /home/sim/tmp/%s-py2.6.egg'%dist)
    run('rm -rf /home/sim/tmp/%s-py2.6.egg'%dist)
