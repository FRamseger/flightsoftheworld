# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 20:52:38 2017
@author: @framseger
"""

#impoprt packages:
from geographiclib.geodesic import Geodesic
import pandas as pd
from lxml import etree as ET

#set up kml structure:
kml = ET.Element('kml')
document = ET.SubElement(kml, 'Document')

#read data
df = pd.read_csv('flightsoftheworld.csv')

#loop through routes, calculate waypoints:

for x in (df.index):
    olat = df.iloc[x,1]
    olon = df.iloc[x,2]
    dlat = df.iloc[x,3]
    dlon = df.iloc[x,4]
    route = df.iloc[x,5]
       

    p=Geodesic.WGS84.Inverse(olat, olon, dlat, dlon)
    l=Geodesic.WGS84.Line(p['lat1'],p['lon1'],p['azi1'])
    if (p['s12'] >= 1000000):
        num = int (p['s12']/100000)  #number of waypoints depending on length
    else:
        num=10
    output=''
    for i in range(num+1):
        b=l.Position(i*p['s12']/num, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        output += repr(b['lon2']) + "," + repr(b['lat2']) + ",0 "
    #print(str(x)+"/"+str(len(df))) #progess counter
    
    # inner part of kml file:
     placemark = ET.SubElement(document, 'Placemark')
    name = ET.SubElement(placemark, 'name')
    name.text = route
    description = ET.SubElement(placemark, 'description')
    description.text = 'route ID: '+str(x)+'; distance: '+str(p['s12'])
    linestring = ET.SubElement(placemark, 'LineString')
    coordinates = ET.SubElement(linestring, 'coordinates')
    coordinates.text = output
    

#complete kml file and save:
tree = ET.ElementTree(kml)
tree.write('greatcircleflightsoftheworld.kml', pretty_print=True, xml_declaration=True,   encoding="utf-8")