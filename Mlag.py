import pyeapi

def configure_device(node_name, vlan4094_ip, peer_address):
    connection = pyeapi.client.connect_to(node_name)
    
    # Build configuration commands
    commands = [
        'spanning-tree mode mstp',
        'no spanning-tree vlan-id 4094',
        'vlan 4094',
        '  trunk group MLAGPEER',
        f'interface Vlan4094',
        f'  description MLAG PEER LINK',
        f'  ip address {vlan4094_ip}',
        f'interface Port-Channel10',
        f'  description MLAG PEER LINK - LEAF',
        f'  switchport mode trunk',
        f'  switchport trunk group MLAGPEER',
        'mlag configuration',
        '  domain-id MLAG',
        '  local-interface Vlan4094',
        f'  peer-address {peer_address}',
        f'  peer-link Port-Channel10'
    ]
    
    # Loop to configure Ethernet interfaces 1 and 2
    for interface in range(1, 3):
        commands.extend([
            f'interface Ethernet{interface}',
            f'  description MLAG PEER LINK - LEAF',
            f'  switchport mode trunk',
            f'  channel-group 10 mode active'
        ])
    
    # Send configuration commands
    try:
        response = connection.config(commands)
        print(f"Configuration applied successfully on {node_name}")
        return response
    except pyeapi.eapilib.CommandError as e:
        print(f"Failed to configure on {node_name}: {str(e)}")
        return None

# Define the VLAN and MLAG parameters for each device
mlag_configurations = {
    'leaf1-DC1': {
        'vlan4094_ip': '192.168.255.1/30',
        'peer_address': '192.168.255.2'
    },
    'leaf2-DC1': {
        'vlan4094_ip': '192.168.255.2/30',
        'peer_address': '192.168.255.1'
    },
       'leaf3-DC1': {
        'vlan4094_ip': '192.168.255.1/30',
        'peer_address': '192.168.255.2'
    },
    'leaf4-DC1': {
        'vlan4094_ip': '192.168.255.2/30',
        'peer_address': '192.168.255.1'
    },
    'leaf1-DC2': {
        'vlan4094_ip': '192.168.255.1/30',
        'peer_address': '192.168.255.2'
    },
    'leaf2-DC2': {
        'vlan4094_ip': '192.168.255.2/30',
        'peer_address': '192.168.255.1'
    },
    'leaf3-DC2': {
        'vlan4094_ip': '192.168.255.1/30',
        'peer_address': '192.168.255.2'
    },
    'leaf4-DC2': {
        'vlan4094_ip': '192.168.255.2/30',
        'peer_address': '192.168.255.1'
    },
    'borderleaf1-DC1': {
        'vlan4094_ip': '192.168.255.1/30',
        'peer_address': '192.168.255.2'
    },
    'borderleaf2-DC1': {
        'vlan4094_ip': '192.168.255.2/30',
        'peer_address': '192.168.255.1'
    },
    'borderleaf1-DC2': {
        'vlan4094_ip': '192.168.255.1/30',
        'peer_address': '192.168.255.2'
    },
    'borderleaf2-DC2': {
        'vlan4094_ip': '192.168.255.2/30',
        'peer_address': '192.168.255.1'
    }
}

# Configure each device
for node_name, config in mlag_configurations.items():
    configure_device(node_name,
                     config['vlan4094_ip'],
                     config['peer_address'])
