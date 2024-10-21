import netCDF4 as nc

netcdf_file_path = 'GFED5_Beta_daily_202012.nc' # Path to the netCDF file

ndata  = nc.Dataset(netcdf_file_path, 'r') # Open the netCDF file in read mode

# Get the dimensions in the netCDF file
ndata_dim = ndata.dimensions.keys()
# print(ndata_dim) # Print the dimensions in the netCDF file

# Get the variables in the netCDF file
ndata_var = ndata.variables.keys()
# print(ndata_var) # Print the variables in the netCDF file

lon = ndata.dimensions['lon']
XNUM = len(lon)
lat = ndata.dimensions['lat']
YNUM = len(lat)
time = ndata.dimensions['time']
TNUM = len(time)

print("(XNUM(lon/経度), YNUM(lat/緯度), TNUM(time)) = (",XNUM,", ",YNUM,", ",TNUM,")")

# print(ndata.variables['lon'][:]) # 経度
# print(ndata.variables['lat'][:]) # 緯度

# for x in ndata_var:
#     print(x, ndata.variables[x][:])
# print(ndata.variables['CO2'][:])

# for x in range(XNUM):
#     for y in range(YNUM):
#         for t in range(TNUM):
#             print("(",x,",",y,",",t,")")
#             if ndata.variables['C'][t][y][x] != 0:
#                 print("(",x,",",y,",",t,") :", ndata.variables['C'][t][y][x])

