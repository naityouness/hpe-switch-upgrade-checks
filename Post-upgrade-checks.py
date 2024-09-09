from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
import difflib

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

def compare_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        diff = difflib.unified_diff(
            f1.readlines(),
            f2.readlines(),
            fromfile=file1,
            tofile=file2,
        )

    for line in diff:
        print(line)

def main():
    nr = InitNornir(
        inventory={
            "options": {
                "host_file": "hosts.yaml",
            }
        }
    )

    post_upgrade_commands = ["display version", "display system stable state", "display interface brief", "display stp brief", "display current-configuration"]

    run_commands(nr, post_upgrade_commands, 'post-checks_')

    for command in post_upgrade_commands:
        pre_file = 'pre-upgrade_' + command.replace(' ', '_') + '.txt'
        post_file = 'post-checks_' + command.replace(' ', '_') + '.txt'
        print(f"\nComparing {pre_file} and {post_file}:\n")
        compare_files(pre_file, post_file)

if __name__ == "__main__":
    main()
