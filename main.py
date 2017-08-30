#plugin Geodesic2Shape

from __future__ import division
import sys
from PyQt4 import QtCore, QtGui, uic
import numpy as np
import math as m
from osgeo import ogr
import osgeo.osr as osr
import os

from how_works import How_works
from input_ins import Input_instructions
from solve_fow import solve_fow
from solve_inv import solve_inv
from deg2dms import deg2dms
from export_shp_line import export_shp_line
from export_shp_point import export_shp_point



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'main.ui')) 

        
class MyApp(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)              
        self.button_restore.clicked.connect(self.restore_default)  
        self.button_how_works.clicked.connect(self.how_works)
        self.button_input_instr.clicked.connect(self.input_instructions)
        self.button_foward.clicked.connect(self.foward)
        self.button_inverse.clicked.connect(self.inverse)
        self.button_fow_export_point.clicked.connect(self.shp_fow_pt)
        self.button_fow_export_line.clicked.connect(self.shp_fow_ln)
        self.button_inv_export_point.clicked.connect(self.shp_inv_pt)
        self.button_inv_export_line.clicked.connect(self.shp_inv_ln)
        self.button_exit.clicked.connect(self.close_application)
        
                    
    def restore_default(self):
        self.radio_fowepsg1.setChecked(True)
        self.radio_fowinterval1.setChecked(True)
        self.radio_invepsg1.setChecked(True)
        self.radio_invinterval1.setChecked(True)
        self.comboBox_fow_lat1.setCurrentIndex(0)
        self.comboBox_fow_long1.setCurrentIndex(0)
        self.comboBox_inv_lat1.setCurrentIndex(0)
        self.comboBox_inv_long1.setCurrentIndex(0)
        self.comboBox_inv_lat2.setCurrentIndex(0)
        self.comboBox_inv_long2.setCurrentIndex(0)
        self.comboBox_fow_epsg.setCurrentIndex(0)
        self.comboBox_inv_epsg.setCurrentIndex(0)
        self.fow_epsg.setText('0000')
        self.fow_elip_a.setText('0000000')
        self.fow_elip_a_2.setText('00000')
        self.fow_elip_b.setText('0000000')
        self.fow_elip_b_2.setText('00000')
        self.fow_int.setText('0')
        self.fow_int2.setText('0000')
        self.fow_lat1_deg.setText('0')
        self.fow_lat1_min.setText('0')
        self.fow_lat1_sec.setText('0')
        self.fow_lat1_sec_2.setText('0000')
        self.fow_long1_deg.setText('0')
        self.fow_long1_min.setText('0')
        self.fow_long1_sec.setText('0')
        self.fow_long1_sec_2.setText('0000')
        self.fow_az1_deg.setText('0')
        self.fow_az1_min.setText('0')
        self.fow_az1_sec.setText('0')
        self.fow_az1_sec_2.setText('0000')
        self.fow_s.setText('0')
        self.fow_s_2.setText('0000')
        self.inv_epsg.setText('0000')
        self.inv_elip_a.setText('0000000')
        self.inv_elip_a_2.setText('00000')
        self.inv_elip_b.setText('0000000')
        self.inv_elip_b_2.setText('00000')
        self.inv_int.setText('0')
        self.inv_int2.setText('0000')
        self.inv_lat1_deg.setText('0')
        self.inv_lat1_min.setText('0')
        self.inv_lat1_sec.setText('0')
        self.inv_lat1_sec_2.setText('0000')
        self.inv_long1_deg.setText('0')
        self.inv_long1_min.setText('0')
        self.inv_long1_sec.setText('0')
        self.inv_long1_sec_2.setText('0000')
        self.inv_lat2_deg.setText('0')
        self.inv_lat2_min.setText('0')
        self.inv_lat2_sec.setText('0')
        self.inv_lat2_sec_2.setText('0000')
        self.inv_long2_deg.setText('0')
        self.inv_long2_min.setText('0')
        self.inv_long2_sec.setText('0')
        self.inv_long2_sec_2.setText('0000')
        self.fow_result.setText('')
        self.inv_result.setText('')

    def how_works(self):
        dlg = How_works()
        dlg.exec_()

    def input_instructions(self):
        dlg = Input_instructions()
        dlg.exec_()

    def msg_to_fill(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("There is/are mandatory field(s) not filled.")
        msgBox.exec_()
                

    def get_fow(self):
        msgBox = QtGui.QMessageBox()
        aux=1
        try: lat1_d = float(self.fow_lat1_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat1_d>90:
            msgBox.setText("Maximum Latitude (degrees) is 90.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat1_m = float(self.fow_lat1_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat1_m>59:
            msgBox.setText("Maximum Latitude (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat1_s = int(self.fow_lat1_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat1_s>59:
            msgBox.setText("Maximum Latitude (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat1_s_2 = int(self.fow_lat1_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        lat1_s=float(str(lat1_s)+"."+str(lat1_s_2))
        lat1_h_str = str(self.comboBox_fow_lat1.currentText())
        
        try: long1_d = float(self.fow_long1_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long1_d>180:
            msgBox.setText("Maximum Longitude (degrees) is 180.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long1_m = float(self.fow_long1_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long1_m>59:
            msgBox.setText("Maximum Longitude (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long1_s = int(self.fow_long1_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long1_s>59:
            msgBox.setText("Maximum Longitude (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long1_s_2 = int(self.fow_long1_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        long1_s=float(str(long1_s)+"."+str(long1_s_2))
        long1_h_str = str(self.comboBox_fow_long1.currentText())
        
        try: az1_d = float(self.fow_az1_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if az1_d>360:
            msgBox.setText("Maximum Azimuth (degrees) is 360.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: az1_m = float(self.fow_az1_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if az1_m>59:
            msgBox.setText("Maximum Azimuth (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: az1_s = int(self.fow_az1_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if az1_s>59:
            msgBox.setText("Maximum Azimuth (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: az1_s_2 = int(self.fow_az1_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        az1_s=float(str(az1_s)+"."+str(az1_s_2))
        
        try: s = int(self.fow_s.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        try: s_2 = int(self.fow_s_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        s=float(str(s)+"."+str(s_2))
        if s>18000000:
            msgBox.setText("Maximum ellipsoidal distance is 18,000,000 meters.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)

        if self.radio_fowepsg1.isChecked() == True:
            str_epsg = str(self.comboBox_fow_epsg.currentText())
            if str_epsg == "4326: WGS 84": epsg=4326
            if str_epsg == "4674: SIRGAS 2000": epsg=4674
            if str_epsg == "4618: SAD 69": epsg=4618
            if str_epsg == "4225: Corrego Alegre": epsg=4225
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(epsg)
            a=srs.GetSemiMajor()
            try: b=srs.GetSemiMinor()
            except: e=srs.GetInvFlattening(); b=a*(e-1)/e; 
        elif self.radio_fowepsg2.isChecked() == True:
            try: epsg = int(self.fow_epsg.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            srs = osr.SpatialReference()
            try: srs.ImportFromEPSG(epsg)
            except:
                msgBox.setText("EPSG not found.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            if srs.IsGeographic():
                a=srs.GetSemiMajor()
                try: b=srs.GetSemiMinor()
                except: e=srs.GetInvFlattening(); b=a*(e-1)/e;
            else:
                msgBox.setText("EPSG is not from a GRS.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        else:
            try: a = int(self.fow_elip_a.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            if a<=999999:
                msgBox.setText("Semi-major axis (a) must be equal or bigger than 1,000,000.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            try: a_2 = int(self.fow_elip_a_2.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            a=float(str(a)+"."+str(a_2))
            try: b = int(self.fow_elip_b.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            if b<=999999:
                msgBox.setText("Semi-minor axis (b) must be equal or bigger than 1,000,000.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            try: b_2 = int(self.fow_elip_b_2.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            b=float(str(b)+"."+str(b_2))
            if b>a:
                msgBox.setText("Ellipsoid restriction: (a) must be equal or bigger than (b).")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            if a>1.5*b:
                msgBox.setText("Ellipsoid restriction: (a) must be equal or less than (1.5*b).")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            epsg="none"
                        
        if lat1_h_str == "North":
            lat1_h = 1
        if lat1_h_str == "South":
            lat1_h = -1
        if long1_h_str == "East":
            long1_h = 1
        if long1_h_str == "West":
            long1_h = -1
        lat1=lat1_h*(lat1_d+(lat1_m/60)+(lat1_s/3600))
        if abs(lat1)>90:
            msgBox.setText("Maximum Latitude is 90:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        long1=long1_h*(long1_d+(long1_m/60)+(long1_s/3600))
        if abs(long1)>180:
            msgBox.setText("Maximum Longitude is 180:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        az1=az1_d+(az1_m/60)+(az1_s/3600)
        if az1>360:
            msgBox.setText("Maximum Azimuth is 360:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        return (a,b,lat1, long1, az1, s,epsg,aux)
        
    def foward(self):
        getfow=self.get_fow()
        if getfow[7]==0: return
        a=getfow[0];b=getfow[1];lat1=getfow[2];long1=getfow[3];az1=getfow[4];s=getfow[5];
        result = solve_fow (a,b,lat1, long1, az1, s)
        lat2=str(deg2dms("lat",result[0]))
        long2=str(deg2dms("long",result[1]))
        az2=str(deg2dms("az",result[2]))
        result_string = 'Latitude P2:   '+lat2+'\nLongitude P2:   '+long2+'\nAzimuth 2:   '+az2
        self.fow_result.setText(result_string)
        

    def get_inv(self):
        msgBox = QtGui.QMessageBox()
        aux=1
        try: lat1_d = float(self.inv_lat1_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat1_d>90:
            msgBox.setText("Maximum Latitude (degrees) is 90.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat1_m = float(self.inv_lat1_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat1_m>59:
            msgBox.setText("Maximum Latitude (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat1_s = int(self.inv_lat1_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat1_s>59:
            msgBox.setText("Maximum Latitude (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat1_s_2 = int(self.inv_lat1_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        lat1_s=float(str(lat1_s)+"."+str(lat1_s_2))
        lat1_h_str = str(self.comboBox_inv_lat1.currentText())
        
        try: long1_d = float(self.inv_long1_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long1_d>180:
            msgBox.setText("Maximum Longitude (degrees) is 180.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long1_m = float(self.inv_long1_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long1_m>59:
            msgBox.setText("Maximum Longitude (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long1_s = int(self.inv_long1_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long1_s>59:
            msgBox.setText("Maximum Longitude (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long1_s_2 = int(self.inv_long1_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        long1_s=float(str(long1_s)+"."+str(long1_s_2))
        long1_h_str = str(self.comboBox_inv_long1.currentText())

        try: lat2_d = float(self.inv_lat2_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat2_d>90:
            msgBox.setText("Maximum Latitude (degrees) is 90.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat2_m = float(self.inv_lat2_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if lat2_m>59:
            msgBox.setText("Maximum Latitude (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat2_s = int(self.inv_lat2_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        lat1_h_str = str(self.comboBox_inv_lat1.currentText())
        if lat2_s>59:
            msgBox.setText("Maximum Latitude (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: lat2_s_2 = int(self.inv_lat2_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        lat2_s=float(str(lat2_s)+"."+str(lat2_s_2))
        lat2_h_str = str(self.comboBox_inv_lat2.currentText())
        
        try: long2_d = float(self.inv_long2_deg.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long2_d>180:
            msgBox.setText("Maximum Longitude (degrees) is 180.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long2_m = float(self.inv_long2_min.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        if long2_m>59:
            msgBox.setText("Maximum Longitude (minutes) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long2_s = int(self.inv_long2_sec.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        long2_h_str = str(self.comboBox_inv_long2.currentText())
        if long2_s>59:
            msgBox.setText("Maximum Longitude (seconds) is 59.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        try: long2_s_2 = int(self.inv_long2_sec_2.text())
        except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
        long2_s=float(str(long2_s)+"."+str(long2_s_2))
        long2_h_str = str(self.comboBox_inv_long2.currentText())
        
        if self.radio_invepsg1.isChecked() == True:
            str_epsg = str(self.comboBox_inv_epsg.currentText())
            if str_epsg == "4326: WGS 84": epsg=4326
            if str_epsg == "4674: SIRGAS 2000": epsg=4674
            if str_epsg == "5332: ITRF 2008": epsg=5332
            if str_epsg == "7789: ITRF 2014": epsg=7789
            if str_epsg == "4258: ETRS 89": epsg=4258
            if str_epsg == "6318: NAD 83 (2011)": epsg=6318
            if str_epsg == "4618: SAD 69": epsg=4618
            if str_epsg == "4225: Corrego Alegre": epsg=4225
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(epsg)
            a=srs.GetSemiMajor()
            try: b=srs.GetSemiMinor()
            except: e=srs.GetInvFlattening(); b=a*(e-1)/e; 
        elif self.radio_invepsg2.isChecked() == True:
            try: epsg = int(self.inv_epsg.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            srs = osr.SpatialReference()
            try: srs.ImportFromEPSG(epsg)
            except:
                msgBox.setText("EPSG not found.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            if srs.IsGeographic():
                a=srs.GetSemiMajor()
                try: b=srs.GetSemiMinor()
                except: e=srs.GetInvFlattening(); b=a*(e-1)/e;
            else:
                msgBox.setText("EPSG is not from a GRS.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        else:
            try: a = int(self.inv_elip_a.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            if a<=999999:
                msgBox.setText("Semi-major axis (a) must be equal or bigger than 1,000,000.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            try: a_2 = int(self.inv_elip_a_2.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            a=float(str(a)+"."+str(a_2))
            try: b = int(self.inv_elip_b.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            if b<=999999:
                msgBox.setText("Semi-minor axis (b) must be equal or bigger than 1,000,000.")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            try: b_2 = int(self.inv_elip_b_2.text())
            except: self.msg_to_fill(); return (0,0,0,0,0,0,0,0)
            b=float(str(b)+"."+str(b_2))
            if b>a:
                msgBox.setText("Ellipsoid restriction: (a) must be equal or bigger than (b).")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            if a>1.5*b:
                msgBox.setText("Ellipsoid restriction: (a) must be equal or less than (1.5*b).")
                msgBox.exec_(); return (0,0,0,0,0,0,0,0)
            epsg="none"
            
        if lat1_h_str == "North": lat1_h = 1
        if lat1_h_str == "South": lat1_h = -1
        lat1=lat1_h*(lat1_d+(lat1_m/60)+(lat1_s/3600))
        if abs(lat1)>90:
            msgBox.setText("Maximum Latitude is 90:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        if long1_h_str == "East": long1_h = 1
        if long1_h_str == "West": long1_h = -1
        long1=long1_h*(long1_d+(long1_m/60)+(long1_s/3600))
        if abs(long1)>180:
            msgBox.setText("Maximum Longitude is 180:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        if lat2_h_str == "North": lat2_h = 1
        if lat2_h_str == "South": lat2_h = -1
        lat2=lat2_h*(lat2_d+(lat2_m/60)+(lat2_s/3600))
        if abs(lat2)>90:
            msgBox.setText("Maximum Latitude is 90:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        if long2_h_str == "East": long2_h = 1
        if long2_h_str == "West": long2_h = -1
        long2=long2_h*(long2_d+(long2_m/60)+(long2_s/3600))
        if abs(long2)>180:
            msgBox.setText("Maximum Longitude is 180:0:0.")
            msgBox.exec_(); return (0,0,0,0,0,0,0,0)
        return (a,b,lat1, long1, lat2, long2,epsg,aux)

    def inverse(self):
        getinv=self.get_inv()
        if getinv[7]==0: return
        a=getinv[0];b=getinv[1];lat1=getinv[2];long1=getinv[3];lat2=getinv[4];long2=getinv[5];
        result = solve_inv(a,b,lat1, long1, lat2, long2)
        az12=str(deg2dms("az",result[0]))
        az21=str(deg2dms("az",result[1]))
        s=str(round(result[2],4))
        if float(s)>18000000:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Maximum ellipsoidal distance is 18,000,000 meters.")
            msgBox.exec_(); return
        result_string = 'Foward Azimuth:   '+az12+'\nBackward Azimuth:   '+az21+'\nEllipsoidal distance:   '+s+' meters'
        self.inv_result.setText(result_string)
        

        
    def shp_fow_pt (self):
        msgBox = QtGui.QMessageBox()
        getfow=self.get_fow()
        if getfow[7]==0: return
        a=getfow[0];b=getfow[1];lat1=getfow[2];long1=getfow[3];az1=getfow[4];s=getfow[5];epsg=getfow[6];

        if self.radio_fowelip.isChecked() == True:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Export SHP is not available if no GRS is provided above.")
            msgBox.exec_(); return
            
        if self.radio_fowinterval1.isChecked() == True:
            interval=1000
        else:
            try: interval = int(self.fow_int.text())
            except: self.msg_to_fill(); return; 
            try: interval_2 = int(self.fow_int2.text())
            except: self.msg_to_fill(); return; 
            interval=float(str(interval)+"."+str(interval_2))
            if interval<100:
                msgBox.setText("Minimum interval between solution points is 100 meters.")
                msgBox.exec_(); return;
                    
        filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.shp"))
        if filename=="": return

        if os.path.exists(filename):
            try: os.rename(filename, filename) #can't rename an open file so an error will be thrown
            except:
                msgBox.setText("Unable to overwrite the file. Close it and try again.")
                msgBox.exec_(); return
       
        result = solve_fow (a,b,lat1, long1, az1, s)
        lat2=str(deg2dms("lat",result[0]))
        long2=str(deg2dms("long",result[1]))
        az2=str(deg2dms("az",result[2]))
        result_string = 'Latitude P2:   '+lat2+'\nLongitude P2:   '+long2+'\nAzimuth 2:   '+az2
        self.fow_result.setText(result_string)

        try: export_shp_point (a,b,lat1,long1,az1,s,epsg,interval,filename)
        except:
            msgBox.setText("Unable to export the file.")
            msgBox.exec_(); return
        msgBox.setText("SHP sucessfully exported.")
        msgBox.exec_();

    def shp_fow_ln (self):
        msgBox = QtGui.QMessageBox()
        getfow=self.get_fow()
        if getfow[7]==0: return
        a=getfow[0];b=getfow[1];lat1=getfow[2];long1=getfow[3];az1=getfow[4];s=getfow[5];epsg=getfow[6];

        if self.radio_fowelip.isChecked() == True:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Export SHP is not available if no GRS is provided above.")
            msgBox.exec_(); return
            
        if self.radio_fowinterval1.isChecked() == True:
            interval=1000
        else:
            try: interval = int(self.fow_int.text())
            except: self.msg_to_fill(); return 
            try: interval_2 = int(self.fow_int2.text())
            except: self.msg_to_fill(); return 
            interval=float(str(interval)+"."+str(interval_2))
            if interval<100:
                msgBox.setText("Minimum interval between solution points is 100 meters.")
                msgBox.exec_(); return;
        
        filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.shp"))
        if filename=="": return

        if os.path.exists(filename):
            try: os.rename(filename, filename) #can't rename an open file so an error will be thrown
            except:
                msgBox.setText("Unable to overwrite the file. Close it and try again.")
                msgBox.exec_(); return
       
        result = solve_fow (a,b,lat1, long1, az1, s)
        lat2=str(deg2dms("lat",result[0]))
        long2=str(deg2dms("long",result[1]))
        az2=str(deg2dms("az",result[2]))
        result_string = 'Latitude P2:   '+lat2+'\nLongitude P2:   '+long2+'\nAzimuth 2:   '+az2
        self.fow_result.setText(result_string)

        try: export_shp_line (a,b,lat1,long1,az1,s,epsg,interval,filename)
        except:
            msgBox.setText("Unable to export the file.")
            msgBox.exec_(); return
        msgBox.setText("SHP sucessfully exported.")
        msgBox.exec_();

    def shp_inv_pt(self):
        msgBox = QtGui.QMessageBox()
        getinv=self.get_inv()
        if getinv[7]==0: return
        a=getinv[0];b=getinv[1];lat1=getinv[2];long1=getinv[3];lat2=getinv[4];long2=getinv[5];epsg=getinv[6];

        if self.radio_invelip.isChecked() == True:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Export SHP is not available if no GRS is provided above.")
            msgBox.exec_(); return
            
        result = solve_inv(a,b,lat1, long1, lat2, long2)
        az12=str(deg2dms("az",result[0]))
        az21=str(deg2dms("az",result[1]))
        s=str(round(result[2],4))
        if float(s)>18000000:
            msgBox.setText("Maximum ellipsoidal distance is 18,000,000 meters.")
            msgBox.exec_(); return

        if self.radio_invinterval1.isChecked() == True:
            interval=1000
        else:
            try: interval = int(self.inv_int.text())
            except: self.msg_to_fill(); return 
            try: interval_2 = int(self.inv_int2.text())
            except: self.msg_to_fill(); return 
            interval=float(str(interval)+"."+str(interval_2))
            if interval<100:
                msgBox.setText("Minimum interval between solution points is 100 meters.")
                msgBox.exec_(); return;

        filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.shp"))
        if filename=="": return

        if os.path.exists(filename):
            try: os.rename(filename, filename) #can't rename an open file so an error will be thrown
            except:
                msgBox.setText("Unable to overwrite the file. Close it and try again.")
                msgBox.exec_(); return
        
        result_string = 'Foward Azimuth:   '+az12+'\nBackward Azimuth:   '+az21+'\nEllipsoidal distance:   '+s+' meters'
        self.inv_result.setText(result_string)

        try: export_shp_point(a,b,lat1, long1, result[0], result[2],epsg,interval,filename)
        except:
            msgBox.setText("Unable to export the file.")
            msgBox.exec_(); return
        msgBox.setText("SHP sucessfully exported.")
        msgBox.exec_();

    def shp_inv_ln(self):
        msgBox = QtGui.QMessageBox()
        getinv=self.get_inv()
        if getinv[7]==0: return
        a=getinv[0];b=getinv[1];lat1=getinv[2];long1=getinv[3];lat2=getinv[4];long2=getinv[5];epsg=getinv[6];

        if self.radio_invelip.isChecked() == True:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Export SHP is not available if no GRS is provided above.")
            msgBox.exec_(); return
            
        result = solve_inv(a,b,lat1, long1, lat2, long2)
        az12=str(deg2dms("az",result[0]))
        az21=str(deg2dms("az",result[1]))
        s=str(round(result[2],4))
        if float(s)>18000000:
            msgBox.setText("Maximum ellipsoidal distance is 18,000,000 meters.")
            msgBox.exec_(); return

        if self.radio_invinterval1.isChecked() == True:
            interval=1000
        else:
            try: interval = int(self.inv_int.text())
            except: self.msg_to_fill(); return 
            try: interval_2 = int(self.inv_int2.text())
            except: self.msg_to_fill(); return 
            interval=float(str(interval)+"."+str(interval_2))
            if interval<100:
                msgBox.setText("Minimum interval between solution points is 100 meters.")
                msgBox.exec_(); return;

        filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.shp"))
        if filename=="": return

        if os.path.exists(filename):
            try: os.rename(filename, filename) #can't rename an open file so an error will be thrown
            except:
                msgBox.setText("Unable to overwrite the file. Close it and try again.")
                msgBox.exec_(); return
        
        result_string = 'Foward Azimuth:   '+az12+'\nBackward Azimuth:   '+az21+'\nEllipsoidal distance:   '+s+' meters'
        self.inv_result.setText(result_string)

        try: export_shp_line(a,b,lat1, long1, result[0], result[2],epsg,interval,filename)
        except:
            msgBox.setText("Unable to export the file.")
            msgBox.exec_(); return
        msgBox.setText("SHP sucessfully exported.")
        msgBox.exec_();

    def close_application(self):     
        #sys.exit()
        self.close()
        
if __name__ == "__main__":            
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
