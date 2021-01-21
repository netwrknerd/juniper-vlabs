from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks.napalm_get import napalm_get
from nornir_utils.plugins.functions import print_result
import os

nr = InitNornir(config_file="_config.yaml")
core = nr.filter(F(role="core"))
print(core.inventory.hosts.keys())

cwd = os.getcwd()

backup_directory = os.path.dirname(cwd + "/backup/")
if not os.path.exists(backup_directory):
     os.makedirs(backup_directory)

for dev in core.inventory.hosts: 
  device_backup_directory = backup_directory + "/" + dev 
  if not os.path.exists(device_backup_directory):
    os.makedirs(device_backup_directory)

result = core.run(task=napalm_get, getters=["config"], retrieve="all")
# print_result(result)
# print(result['vMX1'][0].result['config']['running'])
# print(result['vMX1'][0].result['config']['candidate'])

for dev in core.inventory.hosts:
  running_configuration=open(backup_directory + '/' + dev  + '/' + 'running_configuration.txt','w')
  running_configuration.write(result[dev][0].result['config']['running'])
  running_configuration.close()
  candidate_configuration=open(backup_directory + '/' + dev + '/' + 'candidate_configuration.txt','w')
  candidate_configuration.write(result[dev][0].result['config']['candidate'])
  candidate_configuration.close()