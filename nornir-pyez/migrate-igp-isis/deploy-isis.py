from nornir import InitNornir
from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/_config.yaml")

junos_devices = nr.filter(F(node_type="MX"))


def deploy_isis(task):
    data = {}
    data['isis_int'] = {}
    for intf in task.host['isis_int']:
        data['isis_int'][intf] = {}
        for level in task.host['isis_int'][intf]:
            data['isis_int'][intf][level] = task.host['isis_int'][intf][level]

    candidate = task.run(task=pyez_config, template_path='isis_template.j2',
                            template_vars=data, data_format='xml', name='Configure IS-IS')
    if candidate:
        candidate_diff = task.run(task=pyez_diff, name='Compare Candidate to Active')
    if candidate_diff:
        task.run(task=pyez_commit, name='Commit Candidate to Active')


send_result = junos_devices.run(
    task=deploy_isis)
print_result(send_result)