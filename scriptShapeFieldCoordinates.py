#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checks if shapefile coodinates match the field coordinates
#
# Author:      sa-sbm
#
# Created:     21-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings
import math

def CoordinateCheck(errtype,inDB1,outDB,logDB):

    #inDB1 is Node

    returnValue = 0
    errcount = 0
    coverDict = {}
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")

    fields = [x.name for x in arcpy.ListFields(inDB1) if "ObjectID" in x.name or "XCoordinate" in x.name or "YCoordinate" in x.name]
    fields.append("SHAPE@XY")

    #[u'ObjectID', u'XCoordinate', u'YCoordinate'] + SHAPE@

    cursorS = arcpy.da.SearchCursor(view,fields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorS:

        try:
            if abs(float(row[1]) - row[3][0]) > 0.05 or abs(float(row[2]) - row[3][1]) > 0.05:
                cursorI.insertRow(["Field, and Shapefile X and Y coordinates","Node","Node XY coordinate differs with shapefile",globalScriptSettings.getErrID(),row[0],max([abs(float(row[1]) - row[3][0]),abs(float(row[2]) - row[3][1])])])
                errcount += 1
        except:
            pass

    del cursorS
    arcpy.Delete_management(view)
    del cursorI
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI

    returnValue = errcount
    return returnValue
