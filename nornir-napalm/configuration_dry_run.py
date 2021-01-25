from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks.napalm_configure import napalm_configure
from nornir_jinja2.plugins.tasks.template_file import template_file
from nornir_utils.plugins.functions import print_title, print_result

def configuration(task):
    r = task.run(task=template_file, name="Generate configuration", template="config.j2", path=f"_templates/{task.host.platform}")
    task.host["config"] = r.result

nr = InitNornir(config_file="_config.yaml", dry_run=True)
#core = nr.filter(F(name="vMX1"))
core = nr.filter(F(platform="junos"))
print(core.inventory.hosts.keys())

# from nornir.core.filter import F
# Junos_devices = nr.filter(F(platform="junos"))

print_title("Playbook to configure the network")
result = core.run(task=configuration)
print_result(result)

'''
# to check if a task failed:
result.failed
result["vMX1"].failed
result["vMX1"][2]
result["vMX1"][2].failed
'''


