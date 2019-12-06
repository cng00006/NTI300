#1/usr/bin/python


from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import pprint
import json

credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

project = 'nti-300-2019'
zone = 'us-central-a'
name = 'test3'

def list_instances(compute, project, zone):
    result = compute.list_instances().list(project=project, zone=zone,).execute()
    return result['items']

def create_instance(compute, project, zone, name):
    startup_script = open('startup-script.sh', 'r').read()
    image_response = compute.images().getFromFamily(
      project='centos-cloud', family='centos-7').execute()

    source_disk_image = image_response['selfLink']
    machine_type = "zones/%s/machineTypes/f1-micro" % zones

    config = {
        'name': name,
        'macineType': machine_type,

        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initalizeParms': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        'networkInterfaces': [{
            'network': 'global/network/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        "labels": {
        "http-server": "",
        "https-server"
        ]
        },
        'metadata': {
            'items': [{
            'key': 'startup_script',
            'value': startup_script
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

newinstance = create_instance(compute, project, zone, name)
instances = list_instances(compute, project, zone)

pprint.pprint(newinstance)
pprint.pprint(instances)

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

local_repo()
import os
import re
import subprocess

def setup_install():
    print('installing pip and virtualenv so we can give django its own version of python')
    os.system('yum -y install python-pip && pip install --upgrade pip')
    os.chdir('/opt')
    os.mkdir('/opt/django')
    os.system('virtualenv django-env')
    os.system('cown -R chrisng /opt/django')
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
    print("starting django')
    os.system('chown -R chrisng /opt/django')
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

    os.system('sudo -u chrisng sh -c "source /opt/django/django-env/bin/activate && python manage.py runserver 0.0.0.0:8000&"')

setup_install()
django_install()
django_start()          
