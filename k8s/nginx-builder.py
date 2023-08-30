#! /usr/bin/env python3
#james rogers|james.levi.rogers@gmail.com
"""
Simple script to capture data from a k8s cluster and write it to a formatted file
"""

import subprocess
import os
import json  

#Generates the contents of the nginx file template copied from lab 77
def generate_file(port):
    file = '''# Create a group of targets called "k8nodes"
upstream k8nodes {\n'''
    file += f'  server node-1:{port};\n'
    file += f'  server node-2:{port};\n'
    file += '''}

server {

  listen 2224 default_server;
  listen [::]:2224 default_server;

  location / {
    # map the entire root path to "k8nodes"
    proxy_pass https://k8nodes;  # IMPORTANT, this selects HTTPS protocol
    proxy_set_header Host $http_host;
  }
}
    '''
    return file

def main():
    # Run the kubectl command and capture the output
    command = "kubectl get service ingress-nginx-controller -n ingress-nginx -o json"
    output = subprocess.check_output(command, shell=True, text=True)

    # Parse the JSON output
    data = json.loads(output)

    # Find the https port and extract the nodePort
    https_port = next((port for port in data['spec']['ports'] if port['appProtocol'] == 'https'), None)
    if https_port:
        https_node_port = str(https_port.get('nodePort'))
        if https_node_port:
            #If the data is sucessfully captured and filtered write it to a file
            file = generate_file(https_node_port)
            with open(os.path.expanduser(os.path.normpath('./nginx-ingress')), 'w') as nginx_file:
                nginx_file.write(file)
        else:
            print("Node Port for https not found.")
    else:
        print("https port not found.")


if __name__ == '__main__':
    main()
