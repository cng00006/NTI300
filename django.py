#!/bin/python

import os
import re
import subprocess

def local_repo():
    repo="""[local-epel]
name=NTI300 EPEL
baseurl=http:/35.192.217.88/epel/
gpgcheck=0
enabled=1"""
    print(repo)
    with open("/etc/yum.repos.d/local-repo.repo","w+") as f:
      f.write(repo)
    f.close()

    on="enabled=1"
    off="enabled=0"

    with open('/etc/yum.repos.d/epel.repo') as f:
      dissablerepo=f.read().replace(on, off)
    f.close()

    with open('/etc/yum.repos.d/epel.repo', "w") as f:
      f.write(dissablerepo)
    f.close()

import os
import re
import subprocess

def setup_install():
    print('installing pip and virtualenv so we can give django its own version of python')
    os.system('yum -y install python-pip && pip install --upgrade pip')
    os.chdir('/opt')
    os.mkdir('/opt/django')
    os.system('virtualenv django-env')
    os.system('cown -R cng00006 /opt/django')
    # Using shell because python chown does not work as well

def django_install():
    print('activating virtualenv and installing django after pre-requirements have been met')
    #Must activate virtualenv shell every time you use a command for it to work from python
    os.system('source /opt/django/django-env/bin/activate && pip install django')
    # Confirms install and starts a django project
    os.chdir('/opt/django')
    os.system('source /opt/django/django-env/bin/activate ' + \
              '&& django-admin --version ' + \
              '&& django-admin startproject project1')

def django_start():
    print('starting django')
    os.system('chown -R cng00006 /opt/django')
    os.chdir('/optdjango/project1')
    os.system('source /opt/django/django-env/bin/activate ' + \
              '&& python manage.py migrate')

    os.sytem('source /opt/django/django-env/bin/activate && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'admin\',\"admin@newproject.com\',\'NTI300NTI300\')" | python manage.py shell')

    outputwithnewline = subprocess.check_output('curl -s checkip.dyndns.org | sed -e \'s/.*Current IP Adress: //\' -e \'s/<.*$//\' ', shell=True)
    print outputwithnewline
    output = outputwithnewline.replace("\n", "")
    old_string = "ALLOWED_HOSTS = []"
    new_string = 'ALLOWED_HOSTS = [\'{}\']'.format(output)
    print (new_string)
    print (old_string)

    with open('project1/settings.py') as f:
      newText=f.read().replace(old_string, new_string)
    with open('project1/settings.py', "w") as f:
      f.write(newText)

    os.system('sudo -u cng00006 sh -c "source /opt/django/django-env/bin/activate && python manage.py runserver 0.0.0.0:8000&"')

local_repo()          
setup_install()
django_install()
django_start()  
