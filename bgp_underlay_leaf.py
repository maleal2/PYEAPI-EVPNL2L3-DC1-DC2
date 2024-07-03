import pyeapi
from pyeapi.eapilib import CommandError

# BGP configuration parameters
bgp_configurations = {
    'leaf1-DC1': {
        'asn': 65101,
        'loopback': '192.168.101.11',
        'spines_asn': 65100,
        'neighbors': ['192.168.103.1', '192.168.103.3', '192.168.103.5'],
        'mlag_neighbor': '192.168.255.2'
    },
    'leaf2-DC1': {
        'asn': 65101,
        'loopback': '192.168.101.12',
        'spines_asn': 65100,
        'neighbors': ['192.168.103.7', '192.168.103.9', '192.168.103.11'],
        'mlag_neighbor': '192.168.255.1'
    },
    'leaf3-DC1': {
        'asn': 65102,
        'loopback': '192.168.101.13',
        'spines_asn': 65100,
        'neighbors': ['192.168.103.13', '192.168.103.15', '192.168.103.17'],
        'mlag_neighbor': '192.168.255.2'
    },
    'leaf4-DC1': {
        'asn': 65102,
        'loopback': '192.168.101.14',
        'spines_asn': 65100,
        'neighbors': ['192.168.103.19', '192.168.103.21', '192.168.103.23'],
        'mlag_neighbor': '192.168.255.1'
    },
    'leaf1-DC2': {
        'asn': 65201,
        'loopback': '192.168.201.11',
        'spines_asn': 65200,
        'neighbors': ['192.168.203.1', '192.168.203.3', '192.168.203.5'],
        'mlag_neighbor': '192.168.255.2'
    },
    'leaf2-DC2': {
        'asn': 65201,
        'loopback': '192.168.201.12',
        'spines_asn': 65200,
        'neighbors': ['192.168.203.7', '192.168.203.9', '192.168.203.11'],
        'mlag_neighbor': '192.168.255.1'
    },
    'leaf3-DC2': {
        'asn': 65202,
        'loopback': '192.168.201.13',
        'spines_asn': 65200,
        'neighbors': ['192.168.203.13', '192.168.203.15', '192.168.203.17'],
        'mlag_neighbor': '192.168.255.2'
    },
    'leaf4-DC2': {
        'asn': 65202,
        'loopback': '192.168.201.14',
        'spines_asn': 65200,
        'neighbors': ['192.168.203.19', '192.168.203.21', '192.168.203.23'],
        'mlag_neighbor': '192.168.255.1'
    }
}

# Define the service routing protocol configuration
service_routing = """
service routing protocols model multi-agent
"""

# Define the IP Prefix-list configuration
ip_prefix = """
ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 20 permit 192.168.102.0/24 eq 32
    seq 30 permit 192.168.201.0/24 eq 32
    seq 40 permit 192.168.202.0/24 eq 32
    seq 50 permit 192.168.253.0/24 eq 32
"""

# Define the Route Map configuration
route_map = """
route-map LOOPBACK permit 10
  match ip address prefix-list LOOPBACK
"""


# Function to configure BGP on a device
def configure_bgp(node_name, asn, loopback, spines_asn, neighbors):
    try:
        # Connect to the device
        connection = pyeapi.connect_to(node_name)

        # Configure BGP parameters
        commands = [
            f'router bgp {asn}',
            f'router-id {loopback}',
            'no bgp default ipv4-unicast',
            'maximum-paths 3',
            'distance bgp 20 200 200',
            'redistribute connected route-map LOOPBACK',
            'address-family ipv4',
            'neighbor SPINE_Underlay activate',
            'neighbor LEAF_Peer activate',
            'redistribute connected route-map LOOPBACK'
        ]

        # Configure neighbors
        for neighbor in neighbors:
            commands.append(f'neighbor {neighbor} remote-as {spines_asn}')
            commands.append(f'neighbor {neighbor} send-community')
            commands.append(f'neighbor {neighbor} maximum-routes 12000')
            commands.append(f'neighbor {mlag_neighbor} remote-as {asn}')
            commands.append(f'neighbor {mlag_neighbor} next-hop-self')
            commands.append(f'neighbor {mlag_neighbor} maximum-routes 12000')
            commands.append(f'neighbor {neighbor} peer group SPINE_Underlay')
            commands.append(f'neighbor {mlag_neighbor} peer group LEAF_Peer')

        # Append service routing protocol configuration
        commands.append(service_routing.strip())

        # Append IP prefix-list configuration (split into lines)
        for line in ip_prefix.strip().splitlines():
            commands.append(line.strip())

        # Append Route Map configuration (split into lines)
        for line in route_map.strip().splitlines():
            commands.append(line.strip())

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
    spines_asn = config['spines_asn']
    neighbors = config['neighbors']
    mlag_neighbor = config['mlag_neighbor']

    configure_bgp(node_name, asn, loopback, spines_asn, neighbors)
