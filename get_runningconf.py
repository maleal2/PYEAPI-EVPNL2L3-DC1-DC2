#!/usr/bin/env python
from __future__ import print_function
import pyeapi

# Connect to the device specified in ~/.eapi.conf under [connection:leaf1-DC1]
node = pyeapi.connect_to('spine1-DC1')

# Fetch the running configuration as a list of lines
running_config = node.get_config('running-config')

# Join the lines into a single string with newlines
formatted_config = '\n'.join(running_config)

# Print the formatted running configuration
print('Show running-config for leaf1-DC1')
print('-' * 30)
print(formatted_config)
print()
