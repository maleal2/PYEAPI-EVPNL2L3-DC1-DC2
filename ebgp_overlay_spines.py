import pyeapi
from pyeapi.eapilib import CommandError

# BGP configuration parameters
bgp_configurations = {
    'spine1-DC1': {
        'asn': 65100,
        'loopback': '192.168.101.101',
        'neighbor_Left': ['192.168.101.11', '192.168.101.12'],
        'asn_Left': 65101,
        'neighbor_Right': ['192.168.101.13', '192.168.101.14'],
        'asn_Right': 65102
    },
    'spine2-DC1': {
        'asn': 65100,
        'loopback': '192.168.101.102',
        'neighbor_Left': ['192.168.101.11', '192.168.101.12'],
        'asn_Left': 65101,
        'neighbor_Right': ['192.168.101.13', '192.168.101.14'],
        'asn_Right': 65102
    },
    'spine3-DC1': {
        'asn': 65100,
        'loopback': '192.168.101.103',
        'neighbor_Left': ['192.168.101.11', '192.168.101.12'],
        'asn_Left': 65101,
        'neighbor_Right': ['192.168.101.13', '192.168.101.14'],
        'asn_Right': 65102
    },
    'spine1-DC2': {
        'asn': 65200,
        'loopback': '192.168.201.101',
        'neighbor_Left': ['192.168.201.11', '192.168.201.12'],
        'asn_Left': 65201,
        'neighbor_Right': ['192.168.201.13', '192.168.201.14'],
        'asn_Right': 65202       
    },
    'spine2-DC2': {
        'asn': 65200,
        'loopback': '192.168.201.102',
        'neighbor_Left': ['192.168.201.11', '192.168.201.12'],
        'asn_Left': 65201,
        'neighbor_Right': ['192.168.201.13', '192.168.201.14'],
        'asn_Right': 65202
    },
    'spine3-DC2': {
        'asn': 65200,
        'loopback': '192.168.201.103',
        'neighbor_Left': ['192.168.201.11', '192.168.201.12'],
        'asn_Left': 65201,
        'neighbor_Right': ['192.168.201.13', '192.168.201.14'],
        'asn_Right': 65202
    }
}


# Function to configure BGP on a device
def configure_bgp(node_name, asn, loopback, neighbor_Left, asn_Left, neighbor_Right, asn_Right):
    try:
        # Connect to the device
        connection = pyeapi.connect_to(node_name)

        # Configure BGP parameters
        commands = [
            f'router bgp {asn}',
            f'router-id {loopback}',
            'address-family evpn',
            'neighbor EVPN_LEAF activate',
            'address-family ipv4',
            'no neighbor EVPN_LEAF activate'
        ]

        # Configure neighbors
        for neighbor in neighbor_Left:
            commands.append(f'neighbor {neighbor} remote-as {asn_Left}')
            commands.append(f'neighbor {neighbor} send-community')
            commands.append(f'neighbor {neighbor} maximum-routes 0')
            commands.append(f'neighbor {neighbor} next-hop-unchanged')
            commands.append(f'neighbor {neighbor} peer group EVPN_LEAF')
            commands.append(f'neighbor {neighbor} update-source Loopback0')

        for neighbor in neighbor_Right:
            commands.append(f'neighbor {neighbor} remote-as {asn_Right}')
            commands.append(f'neighbor {neighbor} send-community')
            commands.append(f'neighbor {neighbor} maximum-routes 0')
            commands.append(f'neighbor {neighbor} next-hop-unchanged')
            commands.append(f'neighbor {neighbor} update-source Loopback0')
            
        commands.append('neighbor EVPN_LEAF peer group')

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
    neighbor_Left = config['neighbor_Left']
    asn_Left = config['asn_Left']
    neighbor_Right = config['neighbor_Right']
    asn_Right = config['asn_Right']

    configure_bgp(node_name, asn, loopback, neighbor_Left, asn_Left, neighbor_Right, asn_Right)
