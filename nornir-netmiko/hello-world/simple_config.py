from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def commit_netmiko():
    result = nr.run(netmiko_send_config, config_file='_config.conf', delay_factor=16)
    
    print_result(result)

def main():
    commit_netmiko()

if __name__ == "__main__":
    main()