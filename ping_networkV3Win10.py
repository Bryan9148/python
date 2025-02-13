import subprocess
import re
import platform
import socket

def scan_network(network):
    try:
        output = subprocess.check_output(["nmap", "-sn", network], stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def extract_ip_addresses(nmap_output):
    ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', nmap_output)
    return ip_addresses

def ping_address(address, count=4):
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(["ping", "-n", str(count), address], stderr=subprocess.STDOUT, universal_newlines=True)
        else:
            output = subprocess.check_output(["ping", "-c", str(count), address], stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def ping_addresses(addresses, count=4):
    results = {}
    for address in addresses:
        result = ping_address(address, count)
        results[address] = result
    return results

def get_hostname(address):
    try:
        hostname = socket.gethostbyaddr(address)[0]
    except socket.herror:
        hostname = "Unknown"
    return hostname

def main():
    network = "192.168.1.0/24"
    
    print(f"Scanning network: {network}")
    nmap_output = scan_network(network)
    ip_addresses = extract_ip_addresses(nmap_output)
    
    print(f"Found {len(ip_addresses)} devices on the network. Please wait...")
    
    results = ping_addresses(ip_addresses)
    
    for address, result in results.items():
        hostname = get_hostname(address)
        print(f'Ping to {address} ({hostname}):\n{result}\n')

if __name__ == "__main__":
    main()
