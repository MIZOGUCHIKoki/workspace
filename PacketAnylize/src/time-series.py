from scapy.utils import RawPcapReader
import matplotlib.pyplot as plt

import numpy as np
from utils import get_min, get_max, get_mean, get_median

file_path = 'inbound.dump'
bin_width = 0.1 #(100ms)

size = []
timestamp = []

# RawPcapReader(file) -> packet_data, packet_metadata
# packet_data is the raw bytes of the packet
# packet_metadata is a named tuple with sec and usec attributes

for pkt_data, pkt_metadata in RawPcapReader(file_path):
    # get the timestamp from the packet metadata
    ts:float = pkt_metadata.sec + (pkt_metadata.usec / 1_000_000)
    size.append(len(pkt_data))
    timestamp.append(ts)

# Set the timestamps to start from 0
start_time = get_min(timestamp)
for i in range(len(timestamp)):
    timestamp[i] -= start_time

# Calculate the number of bins
number_of_bins = int(get_max(timestamp) // bin_width) + 1
trafic_volume = [0] * number_of_bins # List

for i in range(len(timestamp)):
    # Get the bin number for each timestamp
    bin_number = int(timestamp[i] // bin_width)
    # Add the size of the packet to the bin
    trafic_volume[bin_number] += size[i]

# Calculate the time axis for the plot
time_axis = [0] * number_of_bins
for i in range(len(time_axis)):
    # Get the bin number for each timestamp
    bin_number = int(timestamp[i] // bin_width)
    # Add the size of the packet to the bin
    time_axis[i] = i * bin_width

plt.figure(figsize=(10, 5))
plt.plot(time_axis, trafic_volume, label='Traffic Volume', drawstyle='steps-post')
plt.axhline(y=get_mean(trafic_volume), color='red', linestyle='-.', label=f'Average ({get_mean(trafic_volume):.2f})')
plt.axhline(y=get_median(trafic_volume), color='red', linestyle='-', label=f'Median ({get_median(trafic_volume):.2f})')
plt.xlabel('Time (s)')
plt.ylabel('Traffic Volume (bytes)')
plt.title('Traffic Volume over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('time_series.png')