from flask import Flask
from osgeo import ogr
import json
app = Flask(__name__)

# global vars
PATH = 'census_tracts/census_reproj4326.shp'
LAYER = 'census_reproj4326'
DRIVER = ogr.GetDriverByName ("ESRI Shapefile")
ogr_ds = DRIVER.Open(PATH)

# This is the URL pattern (where 'fid' is dynamic)
@app.route("/eq/<int:fid>")
def query_eq(fid):
    startFC = "{\"type\": \"FeatureCollection\", \"features\": ["
    endFC = "] }"
    sql = "SELECT * FROM %s WHERE OBJECTID=%s" %(LAYER, fid)
    queryLayer = ogr_ds.ExecuteSQL(sql)

    for (idx, feature) in enumerate(queryLayer):
        if idx == 0:
            startFC = startFC + feature.ExportToJson()
        else:
            startFC = startFC + "," + feature.ExportToJson()
    return startFC + endFC

@app.route("/lt/<int:fid>")
def query_lt(fid):
    startFC = "{\"type\": \"FeatureCollection\", \"features\": ["
    endFC = "] }"
    sql = "SELECT * FROM %s WHERE OBJECTID<%s LIMIT 20" %(LAYER, fid)
    queryLayer = ogr_ds.ExecuteSQL(sql)

    for (idx, feature) in enumerate(queryLayer):
        if idx == 0:
            startFC = startFC + feature.ExportToJson()
        else:
            startFC = startFC + "," + feature.ExportToJson()
    return startFC + endFC

@app.route("/gt/<int:fid>")
def query_gt(fid):
    startFC = "{\"type\": \"FeatureCollection\", \"features\": ["
    endFC = "] }"
    sql = "SELECT * FROM %s WHERE OBJECTID>%s LIMIT 20" %(LAYER, fid)
    queryLayer = ogr_ds.ExecuteSQL(sql)

    for (idx, feature) in enumerate(queryLayer):
        if idx == 0:
            startFC = startFC + feature.ExportToJson()
        else:
            startFC = startFC + "," + feature.ExportToJson()
    return startFC + endFC

