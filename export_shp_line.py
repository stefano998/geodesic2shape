import osgeo.ogr as ogr
import osgeo.osr as osr
from solve_fow import solve_fow
from deg2dms import deg2dms
import os
from qgis.core import *

def export_shp_line (a,b,lat1,long1,az1,s,epsg,interval,filename):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(filename):
     driver.DeleteDataSource(filename)
    data_source = driver.CreateDataSource(filename)

    n=int(s/interval)
    line = ogr.Geometry(ogr.wkbLineString)
    line2 = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(long1, lat1)
    longant=long1
    k=1
    
    while k<=(n+1):
        if k<=n:
            resk = solve_fow (a,b,lat1, long1, az1,k*interval)
        else:
            resk = solve_fow (a,b,lat1,long1,az1,s)      
        latk = resk[0]
        longk = resk[1]
        azk=resk[2]
        if (longk*longant)>-10000:
            line.AddPoint(longk,latk)
        else:
            line2.AddPoint(longk,latk)
            for i in range (k+1,n+2):
                if i<=n:
                    resk = solve_fow (a,b,lat1, long1, az1,i*interval)
                else:
                    resk = solve_fow (a,b,lat1,long1,az1,s)
                lati = resk[0]
                longi = resk[1]
                azi=resk[2]
                line2.AddPoint(longi,lati)
            k=n+2
        longant=longk
        k=k+1
        
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    layer = data_source.CreateLayer(filename, srs, ogr.wkbLineString)
    feature = ogr.Feature(layer.GetLayerDefn())
    wkt = line.ExportToWkt()
    line = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(line)
    layer.CreateFeature(feature)
    feature2 = ogr.Feature(layer.GetLayerDefn())
    wkt2 = line2.ExportToWkt()
    line2 = ogr.CreateGeometryFromWkt(wkt2)
    feature2.SetGeometry(line2)
    layer.CreateFeature(feature2)
    feature = None
    data_source = None
    #show shp
    layer = QgsVectorLayer(filename, os.path.basename(filename)[:-4], "ogr")
    QgsMapLayerRegistry.instance().addMapLayer(layer)


