import osgeo.ogr as ogr
import osgeo.osr as osr
from solve_fow import solve_fow
from deg2dms import deg2dms
import os
from qgis.core import *


def export_shp_point (a,b,lat1,long1,az1,s, epsg,interval,filename):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(filename):
        driver.DeleteDataSource(filename)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(filename)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    layer = data_source.CreateLayer(filename, srs, ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTString))
    layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTString))
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("ID", int(0))
    feature.SetField("Latitude", str(deg2dms("lat",lat1)))
    feature.SetField("Longitude", str(deg2dms("long",long1)))
    wkt = "POINT(%f %f)" %  (float(long1) , float(lat1))
    point = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(point)
    layer.CreateFeature(feature)
    feature = None
    n=int(s/interval)

    for k in range(1,n+2):
        if k<=n:
            resk = solve_fow (a,b,lat1, long1, az1,k*interval)
        else:
            resk = solve_fow (a,b,lat1,long1,az1,s)
        latk = resk[0]
        longk = resk[1]
        azk=resk[2]
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("ID", int(k))
        feature.SetField("Latitude", str(deg2dms("lat",latk)))
        feature.SetField("Longitude", str(deg2dms("long",longk)))
        wkt = "POINT(%f %f)" %  (float(longk) , float(latk))
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        feature = None
    data_source = None
    #show shp
    layer = QgsVectorLayer(filename, os.path.basename(filename)[:-4], "ogr")
    QgsMapLayerRegistry.instance().addMapLayer(layer)

