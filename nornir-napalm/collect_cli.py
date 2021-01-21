from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks.napalm_cli import napalm_cli
from nornir_utils.plugins.functions import print_result
import os

nr = InitNornir(config_file="_config.yaml")
core = nr.filter(F(role="core"))
#print(core.inventory.hosts.keys())

cwd = os.getcwd()
cli_directory = os.path.dirname(cwd + "/cli/")
if not os.path.exists(cli_directory):
     os.makedirs(cli_directory)

for dev in core.inventory.hosts: 
  device_cli_directory = cli_directory + "/" + dev 
  if not os.path.exists(device_cli_directory):
    os.makedirs(device_cli_directory)

collect=["show bgp summary", "show interfaces terse"]

result = core.run(task=napalm_cli, commands=collect)  
# print_result(result)
# print(result['vMX1'][0].result['show bgp summary'])
# print(result['vMX7'][0].result['show interfaces terse'])
# print(result['vMX1'][0].result[collect[0]])
# print(result['vMX7'][0].result[collect[1]])

for dev in core.inventory.hosts:
  for command in collect: 
    cli = open(cli_directory + '/' + dev  + '/' + command, 'w') 
    cli.write(result[dev][0].result[command])
    cli.close()