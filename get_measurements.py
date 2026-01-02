import os
import requests

energy_tags = [
    'timestamp',
    'energy_import_kwh',
    'energy_import_t1_kwh',
    'energy_import_t2_kwh',
    'energy_export_kwh',
    'energy_export_t1_kwh',
    'energy_export_t2_kwh',
    'power_w',
    'power_l1_w',
    'power_l2_w',
    'power_l3_w',
    'voltage_l1_v',
    'voltage_l2_v',
    'voltage_l3_v',
    'current_a',
    'current_l1_a',
    'current_l2_a',
    'current_l3_a',
    'any_power_fail_count',
    'long_power_fail_count'
]

gas_tags = [
    'timestamp',
    'value',
    'unit'
]

def get_measurements():

    homewizard_ip = None
    access_token = None
    with open('.env', 'r') as f:
        env_content = f.readlines()
        homewizard_ip = [line for line in env_content if line.startswith('HOMEWIZARD_IP=')][0].strip().split('=')[1]
        access_token = [line for line in env_content if line.startswith('ACCESS_TOKEN=')][0].strip().split('=')[1]
    api_url = f"https://{homewizard_ip}/api/measurement"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'X-Api-Version': '2'
    }

    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        write_measurements_to_file('energy.csv', energy_tags, data)
        write_measurements_to_file('gas.csv', gas_tags, data.get('external')[0])
    else:
        print(f"Failed to get data: {response.status_code} - {response.text}")

def write_measurements_to_file(filename, tags, data):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            line = ','.join(tags) + '\n'
            f.write(line)

    with open(filename, 'a') as f:
        values = [data[tag] for tag in tags]
        line = ','.join(map(str, values)) + '\n'
        f.write(line)
    
if __name__ == "__main__":

    requests.packages.urllib3.disable_warnings()

    try:
        token = get_measurements()
    except Exception as e:
        print(str(e))