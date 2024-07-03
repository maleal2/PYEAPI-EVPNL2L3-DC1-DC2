import pyeapi
from pyeapi.eapilib import CommandError

# BGP configuration parameters
bgp_configurations = {
    'leaf1-DC1': {
        'asn': 65101,
        'loopback': '192.168.101.11',
        'neighbors': ['192.168.101.101', '192.168.101.102', '192.168.101.103'],
        'spines_asn': 65100
    },
    'leaf2-DC1': {
        'asn': 65101,
        'loopback': '192.168.101.12',
        'neighbors': ['192.168.101.101', '192.168.101.102', '192.168.101.103'],
        'spines_asn': 65100
    },
    'leaf3-DC1': {
        'asn': 65102,
        'loopback': '192.168.101.13',
        'neighbors': ['192.168.101.101', '192.168.101.102', '192.168.101.103'],
        'spines_asn': 65100
    },
    'leaf4-DC1': {
        'asn': 65102,
        'loopback': '192.168.101.14',
        'neighbors': ['192.168.101.101', '192.168.101.102', '192.168.101.103'],
        'spines_asn': 65100
    },
    'leaf1-DC2': {
        'asn': 65201,
        'loopback': '192.168.201.11',
        'neighbors': ['192.168.201.101', '192.168.201.102', '192.168.201.103'],
        'spines_asn': 65200
    },
    'leaf2-DC2': {
        'asn': 65201,
        'loopback': '192.168.201.12',
        'neighbors': ['192.168.201.101', '192.168.201.102', '192.168.201.103'],
        'spines_asn': 65200
    },
    'leaf3-DC2': {
        'asn': 65202,
        'loopback': '192.168.201.13',
        'neighbors': ['192.168.201.101', '192.168.201.102', '192.168.201.103'],
        'spines_asn': 65200
    },    
    'leaf4-DC2': {
        'asn': 65202,
        'loopback': '192.168.201.14',
        'neighbors': ['192.168.201.101', '192.168.201.102', '192.168.201.103'],
        'spines_asn': 65200
    }    
}


# Function to configure BGP on a device
def configure_bgp(node_name, asn, loopback, neighbors, spines_asn):
    try:
        # Connect to the device
        connection = pyeapi.connect_to(node_name)

        # Configure BGP parameters
        commands = [
            f'router bgp {asn}',
            f'router-id {loopback}',
            'address-family evpn',
            'neighbor evpn-spine activate',
            'address-family ipv4',
            'no neighbor evpn-spine activate',
        ]

        # Configure neighbors
        for neighbor in neighbors:
            commands.append(f'neighbor {neighbor} remote-as {spines_asn}')
            commands.append(f'neighbor {neighbor} send-community')
            commands.append(f'neighbor {neighbor} maximum-routes 0')
            commands.append(f'neighbor {neighbor} ebgp-multihop')
            commands.append(f'neighbor {neighbor} peer group evpn-spine')
            commands.append(f'neighbor {neighbor} update-source Loopback0')

        # Execute configuration commands
        response = connection.config(commands)
        print(f"BGP Configuration applied successfully on {node_name}: {response}")

    except CommandError as e:
        print(f"Failed to apply BGP Configuration on {node_name}: {e}")

    except Exception as e:
        print(f"Error configuring BGP on {node_name}: {e}")

# Configure BGP for each device
for node_name, config in bgp_configurations.items():
    asn = config['asn']
    loopback = config['loopback']
    neighbors = config['neighbors']
    spines_asn = config['spines_asn']

    configure_bgp(node_name, asn, loopback, neighbors, spines_asn)
