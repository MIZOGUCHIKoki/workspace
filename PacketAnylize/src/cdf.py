from scapy.utils import RawPcapReader
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils import quick_sort, get_max

file_path = 'inbound.dump'
packet_size = [] # to store packet sizes

# RawPcapReader(file) -> packet_data, packet_metadata
# packet_data is the raw bytes of the packet
# packet_metadata is a named tuple with sec and usec attributes

for pkt_data, pkt_metadata in RawPcapReader(file_path):
    # get packet size
    packet_size.append(len(pkt_data))

sorted_packet_size = quick_sort(packet_size)
# verify_sorted(sorted_packet_size, packet_size)

# Calculate the comulative distribution
total = 0
for i in range(len(sorted_packet_size)):
    total += sorted_packet_size[i]

# Calculate the cumulative distribution
cumulative_distribution = [0] * len(sorted_packet_size)
for i in range(len(sorted_packet_size)):
    if (i == 0):
        cumulative_distribution[i] = sorted_packet_size[i] / total
    if (i > 0):
        cumulative_distribution[i] = sorted_packet_size[i] / total + cumulative_distribution[i - 1]

y_axis_max = get_max(cumulative_distribution)
x_axis_max = get_max(sorted_packet_size)
y_axis_width = 0.2
x_axis_width = 1e1

# Plot the cumulative distribution
plt.figure(figsize=(10, 5))
plt.plot(sorted_packet_size, cumulative_distribution, label='Cumulative Distribution', drawstyle='default', linewidth=1.5, color='#1f77b4')

plt.title('Cumulative Distribution of Packet Sizes')
plt.xlabel('Packet Size (bytes)')
plt.ylabel('Cumulative Size (MB)')
plt.ylim(0, 1)
plt.xlim(0, (x_axis_max // x_axis_width + 1) * x_axis_width)
plt.grid()
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(y_axis_width))
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(x_axis_width))
plt.legend()
plt.tight_layout()
plt.savefig('plot_cdf.pdf')