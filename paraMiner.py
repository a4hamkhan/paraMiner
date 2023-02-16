import argparse
import re
import subprocess
import json

# Create argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help='URL to crawl')
parser.add_argument('--verbose', action='store_true', help='Print parameter names')
parser.add_argument('--json', action='store_true', help='Output parameters in JSON format')

# Parse arguments
args = parser.parse_args()

# Run curl command and capture output
curl_output = subprocess.check_output(['curl', '-s', args.url, '--insecure'])

# Decode output to string
curl_output_str = curl_output.decode()

# Use regular expression to extract name attributes
name_values = re.findall('<input[^>]*\sname=[\'"]?([^\'" >]+)[^>]*>', curl_output_str)

# Print name values if verbose flag is set
if args.verbose:
    for name in name_values:
        print(f'Parameter found: {name}')

# Otherwise, just print the number of parameters found, or output in JSON format if --json flag is set
else:
    if args.json:
        parameter_dict = {f'parameter_{i}': name for i, name in enumerate(name_values)}
        print(json.dumps(parameter_dict))
    else:
        print(f'Found {len(name_values)} parameters')
