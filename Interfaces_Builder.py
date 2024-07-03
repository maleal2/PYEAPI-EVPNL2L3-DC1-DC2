import pyeapi

# Define a function to configure IP addresses and MTU for Ethernet interfaces
def configure_interfaces(node_name, interfaces):
    node = pyeapi.connect_to(node_name)

    for interface, config in interfaces.items():
        # Configure IP address
        ip_address = config.get('ipv4')
        subnet_mask = config.get('mask')
        ip_config_commands = [
            f'interface {interface}',
            f'ip address {ip_address}/{subnet_mask}',
            'no shutdown'  # Ensure interface is enabled
        ]
        node.config(ip_config_commands)

        # Configure MTU for Ethernet interfaces
        if interface.startswith('Ethernet'):
            mtu_value = 9214  # Example MTU value for Ethernet interfaces
            mtu_commands = [
                f'interface {interface}',
                f'mtu {mtu_value}',
                'no switchport' # Add 'no swithcport' for ethernet interfaces
            ]
            node.config(mtu_commands)

# Define the configuration for each device
leafs_DC1_config = {
    'leaf1-DC1': {
        'Loopback0': {'ipv4': '192.168.101.11', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.102.11', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.103.0', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.2', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.4', 'mask': '31'}
    },
    'leaf2-DC1': {
        'Loopback0': {'ipv4': '192.168.101.12', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.102.11', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.103.6', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.8', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.10', 'mask': '31'}
    },
    'leaf3-DC1': {
        'Loopback0': {'ipv4': '192.168.101.13', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.102.13', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.103.12', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.14', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.16', 'mask': '31'}
    },
    'leaf4-DC1': {
        'Loopback0': {'ipv4': '192.168.101.14', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.102.13', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.103.18', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.20', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.22', 'mask': '31'}
    },
    'borderleaf1-DC1': {
        'Loopback0': {'ipv4': '192.168.101.21', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.102.21', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.103.24', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.26', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.28', 'mask': '31'},
        'Ethernet12': {'ipv4': '192.168.254.0', 'mask': '31'}
    }
    ,
    'borderleaf2-DC1': {
        'Loopback0': {'ipv4': '192.168.102.22', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.102.21', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.103.30', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.32', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.34', 'mask': '31'},
        'Ethernet12': {'ipv4': '192.168.254.2', 'mask': '31'}
    }
}

leafs_DC2_config = {
    'leaf1-DC2': {
        'Loopback0': {'ipv4': '192.168.201.11', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.202.11', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.203.0', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.2', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.4', 'mask': '31'}
    },
    'leaf2-DC2': {
        'Loopback0': {'ipv4': '192.168.201.12', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.202.11', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.203.6', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.8', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.10', 'mask': '31'}
    },
    'leaf3-DC2': {
        'Loopback0': {'ipv4': '192.168.201.13', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.202.13', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.203.12', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.14', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.16', 'mask': '31'}
    },
    'leaf4-DC2': {
        'Loopback0': {'ipv4': '192.168.201.14', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.202.13', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.203.18', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.20', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.22', 'mask': '31'}
    },
    'borderleaf1-DC2': {
        'Loopback0': {'ipv4': '192.168.201.21', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.202.21', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.203.24', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.26', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.28', 'mask': '31'},
        'Ethernet12': {'ipv4': '192.168.254.4', 'mask': '31'}
    }
    ,
    'borderleaf2-DC2': {
        'Loopback0': {'ipv4': '192.168.202.22', 'mask': '32'},
        'Loopback1': {'ipv4': '192.168.202.21', 'mask': '32'},
        'Ethernet3': {'ipv4': '192.168.203.30', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.32', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.34', 'mask': '31'},
        'Ethernet12': {'ipv4': '192.168.254.6', 'mask': '31'}
    }
}


spines_DC1_config = {
    'spine1-DC1': {
        'Loopback0': {'ipv4': '192.168.101.101', 'mask': '32'},
        'Ethernet2': {'ipv4': '192.168.103.1', 'mask': '31'},
        'Ethernet3': {'ipv4': '192.168.103.7', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.13', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.19', 'mask': '31'},
        'Ethernet6': {'ipv4': '192.168.103.25', 'mask': '31'},
        'Ethernet7': {'ipv4': '192.168.103.31', 'mask': '31'}
    },
    'spine2-DC1': {
        'Loopback0': {'ipv4': '192.168.101.102', 'mask': '32'},
        'Ethernet2': {'ipv4': '192.168.103.3', 'mask': '31'},
        'Ethernet3': {'ipv4': '192.168.103.9', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.15', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.21', 'mask': '31'},
        'Ethernet6': {'ipv4': '192.168.103.27', 'mask': '31'},
        'Ethernet7': {'ipv4': '192.168.103.33', 'mask': '31'}
    },
    'spine3-DC1': {
        'Loopback0': {'ipv4': '192.168.101.103', 'mask': '32'},
        'Ethernet2': {'ipv4': '192.168.103.5', 'mask': '31'},
        'Ethernet3': {'ipv4': '192.168.103.11', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.103.17', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.103.23', 'mask': '31'},
        'Ethernet6': {'ipv4': '192.168.103.29', 'mask': '31'},
        'Ethernet7': {'ipv4': '192.168.103.35', 'mask': '31'}
    }
}


spines_DC2_config = {
    'spine1-DC2': {
        'Loopback0': {'ipv4': '192.168.201.101', 'mask': '32'},
        'Ethernet2': {'ipv4': '192.168.203.1', 'mask': '31'},
        'Ethernet3': {'ipv4': '192.168.203.7', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.13', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.19', 'mask': '31'},
        'Ethernet6': {'ipv4': '192.168.203.25', 'mask': '31'},
        'Ethernet7': {'ipv4': '192.168.203.31', 'mask': '31'}
    },
    'spine2-DC2': {
        'Loopback0': {'ipv4': '192.168.201.102', 'mask': '32'},
        'Ethernet2': {'ipv4': '192.168.203.3', 'mask': '31'},
        'Ethernet3': {'ipv4': '192.168.203.9', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.15', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.21', 'mask': '31'},
        'Ethernet6': {'ipv4': '192.168.203.27', 'mask': '31'},
        'Ethernet7': {'ipv4': '192.168.203.33', 'mask': '31'}
    },
    'spine3-DC2': {
        'Loopback0': {'ipv4': '192.168.201.103', 'mask': '32'},
        'Ethernet2': {'ipv4': '192.168.203.5', 'mask': '31'},
        'Ethernet3': {'ipv4': '192.168.203.11', 'mask': '31'},
        'Ethernet4': {'ipv4': '192.168.203.17', 'mask': '31'},
        'Ethernet5': {'ipv4': '192.168.203.23', 'mask': '31'},
        'Ethernet6': {'ipv4': '192.168.203.29', 'mask': '31'},
        'Ethernet7': {'ipv4': '192.168.203.35', 'mask': '31'}
    }
}

# Iterate over each device category and configure interfaces
for node_name, interfaces in leafs_DC1_config.items():
    configure_interfaces(node_name, interfaces)

for node_name, interfaces in leafs_DC2_config.items():
    configure_interfaces(node_name, interfaces)

for node_name, interfaces in spines_DC1_config.items():
    configure_interfaces(node_name, interfaces)

for node_name, interfaces in spines_DC2_config.items():
    configure_interfaces(node_name, interfaces)    