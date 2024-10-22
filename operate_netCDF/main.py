import netCDF4 as nc
import csv, math
import numpy as np

netcdf_file_path = 'GFED5_Beta_daily_200201.nc' # Path to the netCDF file

ndata  = nc.Dataset(netcdf_file_path, 'r') # Open the netCDF file in read mode

# Get the dimensions in the netCDF file
ndata_dim = ndata.dimensions.keys()
# print(ndata_dim) # Print the dimensions in the netCDF file

# Get the variables in the netCDF file
ndata_var = ndata.variables.keys()
# print(ndata_var) # Print the variables in the netCDF file

lon = ndata.dimensions['lon']
XNUM = len(lon) # 経度/1440
lat = ndata.dimensions['lat']
YNUM = len(lat) # 緯度/720
time = ndata.dimensions['time']
TNUM = len(time) # 時間/366


print("(XNUM(lon/経度), YNUM(lat/緯度), TNUM(time)) = (",XNUM,", ",YNUM,", ",TNUM,")") 

csv_file_path_Total = 'output/Total.csv'
f = open(csv_file_path_Total, 'w')
writer = csv.writer(f, delimiter=",")
writer.writerow(['day', 'C'])
sum = 0
list = []
for t in range(TNUM):
    for x in range(XNUM):
        for y in range(YNUM):
            sum = sum + ndata['C'][t][y][x]
    writer.writerow([t + 1, sum])
    list.append([t + 1, sum])
    print(t + 1,", ",sum)
    print(list)
    sum = 0
f.close()


# 1日ごとのCの量を横：経度，縦：緯度でCSVを書き出す．
# ファイル名は，output/LONxLAT_n.csv (n = day(1-31))
for x in range(TNUM):
    csv_file_path_LxL = 'output/LONxLAT_'+ str(x+1) +'.csv' # Path to the CSV file
    f = open(csv_file_path_LxL, 'w')
    writer = csv.writer(f, delimiter=",")
    writer.writerows(ndata.variables['C'][x][:][:])
    f.close()