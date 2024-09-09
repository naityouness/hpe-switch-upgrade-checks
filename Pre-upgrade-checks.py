from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

def run_commands(nr, commands, filename_prefix):
    for command in commands:
        results = nr.run(task=netmiko_send_command, command_string=command)
        # Replace spaces with underscores and add .txt extension to create filename
        filename = filename_prefix + command.replace(' ', '_') + '.txt'
        with open(filename, 'w') as f:
            for device_name, multi_result in results.items():
                f.write(f"\nDevice: {device_name}\n")
                f.write(f"Command: {command}\n")
                for result in multi_result:
                    f.write(result.result)
                    f.write("\n")

def main():
    nr = InitNornir(
        inventory={
            "options": {
                "host_file": "hosts.yaml",
            }
        }
    )

    pre_upgrade_commands = ["display version", "display system stable state", "display interface brief", "display stp brief", "display current-configuration"]

    run_commands(nr, pre_upgrade_commands, 'pre-upgrade_')

if __name__ == "__main__":
    main()
