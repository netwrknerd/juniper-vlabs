from nornir import InitNornir
from nornir_pyez.plugins.tasks import pyez_commit, pyez_diff, pyez_rollback
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/_config.yaml")

junos_devices = nr.filter(F(node_type="MX"))

def rollback(task):
    task.run(task=pyez_rollback, rb_id=1, name='Rollback Candidate Config')
    task.run(task=pyez_diff, name='Compare Candidate to Active')
    task.run(task=pyez_commit, name='Commit Candidate to Active')

send_result = junos_devices.run(
    task=rollback)
print_result(send_result)