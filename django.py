#!/usr/bin/python

import os
import subprocess
import re

print ('********** Setting up user django')
os.system ('adduser -M django' + \
    '&& usermod -L django' + \
    '&& chown - R django')

def local_repo():
    repo="""[local-epel]
name=NTI300 EPEL
baseurl=http://35.192.217.88/epel/
gpgcheck=0
enabled=1"""
    os.system('for file in $( ls /etc/yum.repos.d/ ); do mv /etc/yum.repos.d/$file /etc/yum.repos.d/$file.bak; done')
    print(repo)
    with open("/etc/yum.repos.d/local-repo.repo","w+") as f:
      f.write(repo)
    f.close()
local_repo()

def setup_install():
    print ('********** installing pip & virtualenv so we can give django its own ver of python')
    os.system('yum -y install python-pip httpd mod_wsgi && pip install --upgrade pip')
    os.system('pip install virtualenv')
    os.chdir('/opt')
    os.mkdir('/opt/django')
    os.chdir('/opt/django')
    os.system('virtualenv django-env')
    os.system('chown -R django /opt/django')

def django_install():
    print ('********** activating virtualenv; installing django aftr pre-requrmnts met')
    os.system('source /opt/django/django-env/bin/activate ' + \
        '&& pip install django')
    os.chdir('/opt/django')
    os.system('source /opt/django/django-env/bin/activate ' + \
        '&& django-admin --version ' + \
        '&& django-admin startproject project1')

def django_start():
    print('**********starting django')
    os.system('chown -R django /opt/django')
    os.chdir('/opt/django/project1')
    os.system('source /opt/django/django-env/bin/activate ' + \
        '&& python manage.py migrate')
    os.system('source /opt/django/django-env/bin/activate ' + \
        '&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'admin\', \'admin@newproject.com\', \'pw123456\')" | python manage.py shell')

    outputwithnewline = subprocess.check_output('curl -s checkip.dyndns.org | sed -e \'s/.*Current IP Address: //\' -e \'s/<.*$//\'',shell=True)

    print('**********')
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
    with open('project1/settings.py') as f:
        f.close()
    os.system('sudo -u django sh -c "source /opt/django/django-env/bin/activate && python manage.py runserver 0.0.0.0:8000&"')

 
setup_install()
django_install()
django_start()
print ('********** django.py complete')
