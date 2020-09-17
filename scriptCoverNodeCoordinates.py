#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checks if a cover is within 1m of its associated node
#
# Author:      sa-sbm
#
# Created:     17-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings
import math

def CoordinateCheck(errtype,inDB1,inDB2,outDB,logDB):

    #inDB1 is Cover
    #inDB2 is Node

    returnValue = 0
    errcount = 0
    coverDict = {}
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview","NOT NodeID IS NULL")

    fields = [x.name for x in arcpy.ListFields(inDB1) if "ObjectID" in x.name or "NodeID" in x.name or "XCoordinate" in x.name or "YCoordinate" in x.name]

    #[u'ObjectID', u'NodeID', u'XCoordinate', u'YCoordinate']

    cursorS = arcpy.da.SearchCursor(view,fields,"NOT " + [x.name for x in arcpy.ListFields(view) if "XCoordinate" in x.name][0] + " IS NULL AND NOT " + [x.name for x in arcpy.ListFields(view) if "YCoordinate" in x.name][0] + " IS NULL")

    # NodeID : [(coverID,X,Y),..] from Cover
    for row in cursorS:
        num1 = round(row[2],4)
        num2 = round(row[3],4)
        if coverDict.has_key(row[1]):
            coverList = coverDict.pop(row[1])
            coverList.append((row[0],num1,num2))
            coverDict[row[1]] = coverList
        else:
            coverDict[row[1]] = [(row[0],num1,num2)]

    del cursorS
    arcpy.Delete_management(view)

    Sfields = [x.name for x in arcpy.ListFields(inDB2) if "ObjectID" in x.name or "XCoordinate" in x.name or "YCoordinate" in x.name]
    Sfields.append("SHAPE@XY")

    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    cursorS = arcpy.da.SearchCursor(view2,Sfields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorS:

        coverList = coverDict.get(row[0],[])
        for (ID,Xcoord,Ycoord) in coverList:
            distance = math.sqrt( round( math.pow(row[3][0] - Xcoord,2) + math.pow(row[3][1] - Ycoord,2) ,4) )
            if abs(distance) > 1:
                cursorI.insertRow(["Node Shapefile X and Y coordinates","Cover","",globalScriptSettings.getErrID(),ID,row[0],float(distance)])
                errcount += 1
    del cursorI
    del cursorS
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.Delete_management(view2)

    returnValue = errcount
    return returnValue

