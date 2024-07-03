import pyeapi
from pyeapi.eapilib import CommandError

# BGP configuration parameters
bgp_configurations = {
    'spine1-DC1': {
        'asn': 65100,
        'loopback': '192.168.101.101',
    },
    'spine2-DC1': {
        'asn': 65100,
        'loopback': '192.168.101.102',
    },
    'spine3-DC1': {
        'asn': 65100,
        'loopback': '192.168.101.103',
    },
    'spine1-DC2': {
        'asn': 65200,
        'loopback': '192.168.201.101',
    },
    'spine2-DC2': {
        'asn': 65200,
        'loopback': '192.168.201.102',
    },
    'spine3-DC2': {
        'asn': 65200,
        'loopback': '192.168.201.103',
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

# Define the Peer-filter configuration
peer_filter = """
peer-filter LEAF-AS-RANGE
  10 match as-range 65000-65535 result accept
"""


# Function to configure BGP on a device
def configure_bgp(node_name, asn, loopback):
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
            'bgp listen range 192.168.0.0/16 peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE',
            'neighbor LEAF_Underlay send-community',
            'neighbor LEAF_Underlay maximum-routes 12000',
            'neighbor LEAF_Underlay peer group ',
            'redistribute connected route-map LOOPBACK',
            'address-family ipv4',
            'neighbor LEAF_Underlay activate',
            'redistribute connected route-map LOOPBACK'
        ]

        # Append service routing protocol configuration
        commands.append(service_routing.strip())

        # Append IP prefix-list configuration (split into lines)
        for line in ip_prefix.strip().splitlines():
            commands.append(line.strip())

        # Append Route Map configuration (split into lines)
        for line in route_map.strip().splitlines():
            commands.append(line.strip())

        # Append peer-filter configuration (split into lines)
        for line in peer_filter.strip().splitlines():
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

    configure_bgp(node_name, asn, loopback)