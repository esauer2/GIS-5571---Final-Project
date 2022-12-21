import arcpy
import requests
import os
from zipfile import *

# Set source URLs
# Mississippi River Basin Boundary
boundary_url = "https://www.nrcs.usda.gov/sites/default/files/2022-06/Mississippi_River_Basin_CCA.zip"

# Carp Point Location Data from ArcGIS Online
carp_url = "https://services6.arcgis.com/Sjtjj6zwMH9eAgbl/arcgis/rest/services/All_invasive_carp_Data/FeatureServer"

# Water Features
lakes_url = 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_lakes.zip'
small_rivers_url = 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_rivers_lake_centerlines.zip'
large_rivers_url = 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/physical/ne_50m_rivers_lake_centerlines.zip'

# Attribute data
salinity_river_url = "https://hs.pangaea.de/bio/Salinity_database/Thorslund-vanVliet_2020/Rivers_database.csv"
salinity_lake_url = "https://hs.pangaea.de/bio/Salinity_database/Thorslund-vanVliet_2020/Lakes_Reservoirs_database.csv"
precipitation_url = 'https://prism.oregonstate.edu/fetchData.php?type=all_bil&kind=normals&spatial=4km&elem=ppt&temporal=annual'

# Retrieve Data
# Natural Earth Data site requires specifying user agent to avoid bots, this is a chrome
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

boundary_req = requests.get(boundary_url, verify=True)
lakes_req = requests.get(url = lakes_url, headers = headers)
small_rivers_req = requests.get(url = small_rivers_url, headers = headers)
large_rivers_req = requests.get(large_rivers_url, headers = headers)
salinity_river_req = requests.get(salinity_river_url, headers = headers)
salinity_lake_req = requests.get(salinity_lake_url, headers = headers)
precip_req = requests.get(precipitation_url, verify=True)

with open(datafolder + '\\SalinityRiver.csv', 'wb') as salinityriver_csv:
    salinityriver_csv.write(salinity_river_req.content)

# Create folder to store data
newdir = 'C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects'
os.chdir(newdir)
working_dir = os.getcwd()
datafolder = os.path.join(working_dir, r"final_project_data")
if not os.path.exists(datafolder):
   os.makedirs(datafolder)

# Store Zipped Data to Working Directory
with open(datafolder + '\\Boundary.zip', 'wb') as boundary_zip:
    boundary_zip.write(boundary_req.content)
with open(datafolder + '\\Lakes.zip', 'wb') as lakes_zip:
    lakes_zip.write(lakes_req.content)
with open(datafolder + '\\SmallRivers.zip', 'wb') as smallrivers_zip:
    smallrivers_zip.write(small_rivers_req.content)
with open(datafolder + '\\LargeRivers.zip', 'wb') as largerivers_zip:
    largerivers_zip.write(large_rivers_req.content)
with open(datafolder + '\\Precipitation.zip', 'wb') as precipitation_zip:
    precipitation_zip.write(precip_req.content)
with open(datafolder + '\\SalinityRiver.csv', 'wb') as salinityriver_csv:
    salinityriver_csv.write(salinity_river_req.content)
with open(datafolder + '\\SalinityLake.csv', 'wb') as salinitylake_csv:
    salinitylake_csv.write(salinity_lake_req.content)

# Read the created zipfiles
boundary_zipfile = ZipFile(r'C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\Boundary.zip', mode='r')
lakes_zipfile = ZipFile(r'C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\Lakes.zip', mode='r')
smallrivers_zipfile = ZipFile(r'C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\SmallRivers.zip', mode='r')
largerivers_zipfile = ZipFile(r'C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\LargeRivers.zip', mode='r')
precipitation_zipfile = ZipFile(r'C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\Precipitation.zip', mode='r')

# Extract the zipfile information
boundary_zipfile.extractall('C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\Boundary')
lakes_zipfile.extractall('C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\Lakes')
smallrivers_zipfile.extractall('C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\SmallRivers')
largerivers_zipfile.extractall('C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\LargeRivers')
precipitation_zipfile.extractall('C:\\Users\\eriks\\OneDrive\\Documents\\ArcGIS\\Projects\\final_project_data\\Precipitation')

# Set current project and map
aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps("Map")[0]

# Add Shapefile Data
boundary = arcpy.MakeFeatureLayer_management(datafolder + '\\Boundary\\Mississippi_River_Basin_CCA.shp','Study Area')
lakes = arcpy.MakeFeatureLayer_management(datafolder + '\\Lakes\\ne_10m_lakes.shp','Lakes')
smallrivers = arcpy.MakeFeatureLayer_management(datafolder + '\\SmallRivers\\ne_10m_rivers_lake_centerlines.shp','Small Rivers')
largerivers = arcpy.MakeFeatureLayer_management(datafolder + '\\LargeRivers\\ne_50m_rivers_lake_centerlines.shp','Large Rivers')

# Create Raster for Precipitation BIL file
precipitation = arcpy.management.MakeRasterLayer(r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\Precipitation\PRISM_ppt_30yr_normal_4kmM4_annual_bil.bil", "Precipitation", '', '-99.8680067759214 28.3259831310803 -79.0621613897864 47.7865588240753 GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]', None)

# Use Copy Rows to create OIDs for Table to Table
arcpy.management.CopyRows("SalinityRiver.csv", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\SalinityRiver_OIDs", '')
arcpy.management.CopyRows("SalinityLake.csv", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\SalinityLake_OIDs", '')

# Salinity Data - Use Table to Table to Query for US, 2018 data
arcpy.conversion.TableToTable("SalinityRiver_OIDs", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb", "SalinityRiver", "Country = 'USA' And Date >= timestamp '2018-01-01 00:00:00' And Date <= timestamp '2018-5-1 00:00:00'", r'Station_ID "Station_ID" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Station_ID,0,8000;Station_ID_X "Station_ID_X" true true false 8 Double 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Station_ID_X,-1,-1;Station_ID_Y "Station_ID_Y" true true false 8 Double 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Station_ID_Y,-1,-1;Lat "Lat" true true false 8 Double 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Lat,-1,-1;Lon "Lon" true true false 8 Double 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Lon,-1,-1;Country "Country" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Country,0,8000;Continent "Continent" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Continent,0,8000;Date "Date" true true false 8 Date 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Date,-1,-1;EC "EC" true true false 4 Long 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,EC,-1,-1,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,EC,-1,-1,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,EC,0,8000;Source "Source" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Source,0,8000;Field10 "Field10" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityRiver.csv,Field10,0,8000', '')
arcpy.conversion.TableToTable("SalinityLake_OIDs", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb", "SalinityLake", "Country = 'USA' And Date >= timestamp '2018-01-01 00:00:00' And Date <= timestamp '2018-5-1 00:00:00'", r'Station_ID "Station_ID" true true false 4 Long 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Station_ID,-1,-1;Lat "Lat" true true false 8 Double 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Lat,-1,-1;Lon "Lon" true true false 8 Double 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Lon,-1,-1;Country "Country" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Country,0,8000;Continent "Continent" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Continent,0,8000;Date "Date" true true false 8 Date 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Date,-1,-1;EC "EC" true true false 4 Long 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,EC,-1,-1;Source "Source" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Source,0,8000;Water_type "Water_type" true true false 8000 Text 0 0,First,#,C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\final_project_data\SalinityLake.csv,Water_type,0,8000', '')

# Salinity Data - XY Table to Point
arcpy.management.XYTableToPoint("SalinityRiver", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\SalinityRiver_Point", "Lon", "Lat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')
arcpy.management.XYTableToPoint("SalinityLake", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Salinitylake_Point", "Lon", "Lat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

# Remove extraneous data
arcpy.analysis.Clip("Salinitylake_Point", "Study Area", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\SalinityLake_Point_Clip", None)
arcpy.analysis.Clip("SalinityRiver_Point", "Study Area", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\SalinityRiver_Point_Clip", None)
arcpy.analysis.Clip("All_invasive_carp_Data", "Mississippi_River_Basin_CCA", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Carp_loc_clip", None)
arcpy.analysis.Clip("Large Rivers", "Study Area", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Large_Rivers_clip", None)
arcpy.analysis.Clip("Small Rivers", "Study Area", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Small_Rivers_clip", None)
arcpy.analysis.Clip("Lakes", "Study Area", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Lakes_clip", None)
Precip_mask = arcpy.sa.ExtractByMask("Precipitation", "Study Area", "INSIDE", '-99.8680067759214 28.3259831310803 -79.0624999996325 47.7865588240753 GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'); Precip_mask.save(r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Precipitation_mask")

# Kriging Using Salinity Data
arcpy.ddd.Kriging("SalinityRiver_Point_Clip", "EC", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Kriging_RiverSal", "Spherical # # # #", 0.0711615200000001, "VARIABLE 12", None)
arcpy.ddd.Kriging("SalinityLake_Point_Clip", "EC", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Kriging_LakeSal", "Spherical # # # #", 0.02517806668, "VARIABLE 12", None)

# River Data - Polyline to Raster
arcpy.conversion.PolylineToRaster("Small_Rivers_clip", "scalerank", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Small_Rivers_clip_PolylineToRaster", "MAXIMUM_LENGTH", "NONE", .1, "BUILD")

# Prescence only prediction
arcpy.stats.PresenceOnlyPrediction("Carp_loc_clip", "PRESENCE_ONLY_POINTS", None, None, None, "Small_Rivers_clip_PolylineToRaster #;Kriging_RiverSal #;Precip_mask #", "LINEAR", 10, "CONVEX_HULL", None, "NO_THINNING", None, 10, 100, "CLOGLOG", 0.5, None, None, None, None, None, r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Carp_prediction", r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\carp_raster", None, None, "Small_Rivers_clip_PolylineToRaster Small_Rivers_clip_PolylineToRaster;Kriging_RiverSal Kriging_RiverSal;Precip_mask Precip_mask", "ALLOWED", "NONE", 3)

# Clip prediction raster
out_raster = arcpy.sa.ExtractByMask("Carp_raster", "Small_Rivers_clip_PolylineToRaster", "INSIDE", '-98.4987792971268 29.6572392400002 -80.5601461999999 47.5187807600002 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'); out_raster.save(r"C:\Users\eriks\OneDrive\Documents\ArcGIS\Projects\ArcGIS 1 Final Project\ArcGIS 1 Final Project.gdb\Carp_predic")


