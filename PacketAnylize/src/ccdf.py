from scapy.utils import RawPcapReader
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import math

from utils import quick_sort, get_max, get_min, get_mean

file_path = 'inbound.dump'
time_stamp = []

link_hdr_len = 14  # Ethernet header length
min_ihl = 20  # Minimum IP header length
flag_syn = 0x02  # TCP SYN flag


# RawPcapReader(file) -> packet_data, packet_metadata
# packet_data is the raw bytes of the packet
# packet_metadata is a named tuple with sec and usec attributes


# Ethernet header format (IEEE 802.3)
# 0                   1                   2                   3  
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                 Destination MAC Address (6 bytes)            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                 Source MAC Address (6 bytes)                 |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |       EtherType (2 bytes)       |  
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

# IP header format (RFC 791)
# 0                   1                   2                   3  
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |Version|  IHL  |Type of Service|        Total Length           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Identification         |Flags|     Fragment Offset     |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  Time to Live |    Protocol   |       Header Checksum         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                       Source Address                          |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Destination Address                        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


for pkt_data, pkt_metadata in RawPcapReader(file_path):
	if (len(pkt_data) < min_ihl + link_hdr_len):
		continue

	data = pkt_data[link_hdr_len:] # remove the link layer header

	# get IP header (IP header length is stored in the first byte of the IP header)
	ip_header_length = (data[0] & 0x0F) # get the IP header length (in 32-bit words)
	ip_header_length *= 4 # convert to bytes

	# protcol number (ONLY FOR TCP)
	if data[9] != 6:
		continue
	
	
	# get the TCP header (TCP header length is stored in the first byte of the TCP header)
	if (len(data) < ip_header_length + 14):
		continue

	tcp_flags = data[ip_header_length + 13] # TCP flags are stored in the 14th byte of the TCP header
	if (tcp_flags & flag_syn) == 0: # check if the SYN flag is set
		continue
	
	ts = pkt_metadata.sec + (pkt_metadata.usec / 1_000_000) # get the timestamp from the packet metadata
	time_stamp.append(ts) # append the timestamp to the list



inter_arrival_time = [0] * (len(time_stamp) - 1)
for i in range(len(time_stamp)):
	if i == 0:
		continue
	else:
		inter_arrival_time[i - 1] = time_stamp[i] - time_stamp[i - 1]

# Calculate CCDF
sorted_inter_arrival_time = quick_sort(inter_arrival_time)
n = len(sorted_inter_arrival_time)

ccdf_log = [0] * n
for i in range(n):
	if sorted_inter_arrival_time[i] > 0:
		ccdf_log[i] = math.log10((n - i) / n)
	else:
		raise ValueError("Inter-arrival time must be greater than 0 for log transformation.")


sorted_inter_arrival_time_square = [0] * n # x^2
for i in range(n):
	sorted_inter_arrival_time_square[i] = sorted_inter_arrival_time[i] ** 2

MEAN_sorted_inter_arrival_time_square = get_mean(sorted_inter_arrival_time_square) # \bar{x^2}
MEAN_sorted_inter_arrival_time = get_mean(sorted_inter_arrival_time) # \bar{x}
SQUARED_MEAN_sorted_inter_arrival_time = MEAN_sorted_inter_arrival_time ** 2 # \bar{x}^2
MEAN_ccdf_log = get_mean(ccdf_log) # \bar{y}
sorted_inter_arrival_time_and_ccdf_log = [0] * n # \bar{x} * \bar{y}
for i in range(n):
	sorted_inter_arrival_time_and_ccdf_log[i] = sorted_inter_arrival_time[i] * ccdf_log[i]
MEAN_sorted_inter_arrival_time_and_ccdf_log_mean = get_mean(sorted_inter_arrival_time_and_ccdf_log) # \bar{x*y}
MEAN_sorted_inter_arrival_time_and_MEAN_ccdf_log = MEAN_sorted_inter_arrival_time * MEAN_ccdf_log # \bar{x} * \bar{y}

a = (MEAN_sorted_inter_arrival_time_and_ccdf_log_mean - MEAN_sorted_inter_arrival_time_and_MEAN_ccdf_log) / MEAN_sorted_inter_arrival_time_square - SQUARED_MEAN_sorted_inter_arrival_time
b = -a * MEAN_sorted_inter_arrival_time + MEAN_ccdf_log

y = [0] * n
for i in range(n):
	y[i] = a * sorted_inter_arrival_time[i] + b

# Plotting the CCDF

y_axis_width = 1
x_axis_width = 0.01  # 10ms
def format_times(x, pos):
	"""
	Format the x-axis labels to milliseconds.
	"""
	return f'{x * 1000:.0f} '

plt.figure(figsize=(10, 5))
plt.plot(sorted_inter_arrival_time, ccdf_log, linestyle='-', label='CCDF of Inter-Arrival Times', drawstyle='default', linewidth=1.5, color='#1f77b4')
plt.plot(sorted_inter_arrival_time, y, linestyle='--', label = f'Linear Fit $y={a:.3f}x + {b:.3f}$', drawstyle='default', linewidth=1.5, color='#ff7f0e')
plt.title('CCDF of Inter-Arrival Times of TCP SYN Packets')
plt.xlabel('Inter-Arrival Time (ms) [x]')
plt.ylabel('CCDF (log scale) [y]')

plt.xlim(0, (get_max(sorted_inter_arrival_time) // x_axis_width + 1) * x_axis_width)
plt.ylim((get_min(ccdf_log) // y_axis_width) * y_axis_width ,0)
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_times))
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(x_axis_width))
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig('plot_ccdf.pdf')