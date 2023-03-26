import subprocess
import json

output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(":")[1][1:-1] for i in output if "All User Profile" in i]
wifi_list = {}

for i in profiles:
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        wifi_list[i] = results[0]
    except IndexError:
        wifi_list[i] = ""

# Print the dictionary in a pretty format
print(json.dumps(wifi_list, indent=4))
