import argparse
import re
import subprocess
import json

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help='URL to crawl')
parser.add_argument('--verbose', action='store_true', help='Print parameter names')
parser.add_argument('--json', action='store_true', help='Output parameters in JSON format')

args = parser.parse_args()

curl_output = subprocess.check_output(['curl', '-s', args.url, '--insecure'])

curl_output_str = curl_output.decode()

name_values = re.findall('<input[^>]*\sname=[\'"]?([^\'" >]+)[^>]*>', curl_output_str)

if args.verbose:
    for name in name_values:
        print(f'Parameter found: {name}')

else:
    if args.json:
        parameter_dict = {f'parameter_{i}': name for i, name in enumerate(name_values)}
        print(json.dumps(parameter_dict))
    else:
        print(f'Found {len(name_values)} parameters')
