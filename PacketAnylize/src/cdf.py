from scapy.utils import RawPcapReader
import numpy as np
import matplotlib.pyplot as plt

file_path = 'inbound.dump'
packet_size = [] # to store packet sizes

# RawPcapReader(file) -> packet_data, packet_metadata
# packet_data is the raw bytes of the packet
# packet_metadata is a named tuple with sec and usec attributes

for pkt_data, pkt_metadata in RawPcapReader(file_path):
    # get the timestamp from the packet metadata
    packet_size.append(len(pkt_data))
    
packet_size = np.array(packet_size) # NDArray

# Calculate the CDF
sorted_size = np.sort(packet_size)
cdf = []
n = len(sorted_size)
for i in range(n):
	cdf.append((i + 1) / n)