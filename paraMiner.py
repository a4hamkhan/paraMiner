import argparse
import re
import sys
import subprocess

logo = '''
                         $$\   $$\                     $$\                        
                         $$ |  $$ |                    $$ |                       
  $$$$$$\  $$$$$$\$$$$\  $$ |  $$ |$$\   $$\ $$$$$$$\$$$$$$\   $$$$$$\   $$$$$$\  
 $$  __$$\ $$  _$$  _$$\ $$$$$$$$ |$$ |  $$ |$$  __$$\_$$  _| $$  __$$\ $$  __$$\ 
 $$ /  $$ |$$ / $$ / $$ |$$  __$$ |$$ |  $$ |$$ |  $$ |$$ |   $$$$$$$$ |$$ |  \__|
 $$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$\$$   ____|$$ |      
 $$$$$$$  |$$ | $$ | $$ |$$ |  $$ |\$$$$$$  |$$ |  $$ |\$$$$  \$$$$$$$\ $$ |      
 $$  ____/ \__| \__| \__|\__|  \__| \______/ \__|  \__| \____/ \_______|\__|      
 $$ |                                                                             
 $$ | Name   : Para Hunter                                                                            
 \__| Author : github.com/pwnesec  
      
 '''

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help='URL to crawl')
parser.add_argument('--verbose', action='store_true', help='Print verbose output')
parser.add_argument('--json', action='store_true', help='Print output in JSON format')

if len(sys.argv) == 1:
    print(logo)
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if args.verbose:
    print("Verbose mode enabled")

if args.json:
    print("JSON output enabled")

curl_command = f"curl -s {args.url} --insecure"
curl_output = subprocess.check_output(curl_command, shell=True).decode('utf-8')
input_elements = [line for line in curl_output.split('\n') if '<input' in line and 'name=' in line]
parameters = []
for element in input_elements:
    matches = re.findall('name="([^"]*)"', element)
    if matches:
        parameter_name = matches[0]
        parameters.append(parameter_name)
        if args.verbose:
            print(f"Parameter found: {parameter_name}")

if not parameters:
    print("No parameters found")
else:
    if args.json:
        print({"parameters": parameters})
    else:
        print("Found parameters:")
        for parameter in parameters:
            print(f"Parameter found: {parameter}")
