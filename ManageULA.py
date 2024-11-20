import os
import ipaddress
import random
import subprocess

def generate_ula_prefix():
    # Generate a 40-bit random Global ID
    global_id = ''.join(f"{random.randint(0, 255):02x}" for _ in range(4))
    prefix = f"fd{global_id[:2]}:{global_id[4:]}::/48"
    return prefix

def assign_ula_prefix(interface, prefix):
    # Assign ULA prefix to the interface
    subprocess.run(["ip", "addr", "add", f"{prefix[:-3]}1/48", "dev", interface], check=True)

def check_prefix_conflict(prefix, other_prefixes):
    # Check if the generated prefix conflicts with others
    new_net = ipaddress.IPv6Network(prefix)
    for oprefix in other_prefixes:
        other_net = ipaddress.IPv6Network(oprefix)
        if new_net.overlaps(other_net):
            return True
    return False

def main():
    interface = "bat0"  # Replace with your interface name
    other_prefixes = []  # Populate with prefixes from other nodes
    prefix = generate_ula_prefix()
    
    while check_prefix_conflict(prefix, other_prefixes):
        print(f"Conflict detected for {prefix}. Regenerating...")
        prefix = generate_ula_prefix()
    
    print(f"Assigning ULA prefix: {prefix}")
    assign_ula_prefix(interface, prefix)

if __name__ == "__main__":
    main()