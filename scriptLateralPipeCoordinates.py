#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checks if Laterals are connected to their pipe shapefile
#
# Author:      sa-sbm
#
# Created:     24-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings
import math

def CoordinateCheck(errtype,inDB1,inDB2,inDB3,inDB4,outDB,logDB):

    #inDB1 is Pipe
    #inDB2 is MainPipe
    #inDB3 is Node
    #inDB4 is Lateral

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2") #NetworkCategoryCode = 4  gives the laterals themselvs, not the mains they sit on
    view3 = arcpy.MakeTableView_management(inDB3,"tempview3")
    view4 = arcpy.MakeTableView_management(inDB4,"tempview4")

    joinres = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "MainPipeID" in x.name][0],view2,[x.name for x in arcpy.ListFields(view2) if "ObjectID" in x.name][0],"KEEP_COMMON")

    joinfields = [x.name for x in arcpy.ListFields(joinres) if "MainPipeID" in x.name]
    joinfields.append("SHAPE@")
#[u'GIS_VCS_DD_TEST.DANDAS.WW_Pipe.MainPipeID', 'SHAPE@']

    Pipecursor = arcpy.da.SearchCursor(joinres,joinfields)

    count = 0
    LateralDict = {}
    # mainID : [geometry,]
    for row in Pipecursor:
        count += 1
        if LateralDict.has_key(row[0]):
            pointlist = LateralDict.pop(row[0])
            pointlist.append(row[1])
            LateralDict[row[0]] = pointlist
        else:
            LateralDict[row[0]] = [row[1]]

    joinres2 = arcpy.AddJoin_management(view3,[x.name for x in arcpy.ListFields(view3) if "ObjectID" in x.name][0],view4,[x.name for x in arcpy.ListFields(view4) if "NodeID" in x.name][0],"KEEP_COMMON")

    joinfields2 = [x.name for x in arcpy.ListFields(joinres2) if "NodeID" in x.name or "MainPipeID" in x.name]
    joinfields2.append("SHAPE@")
#[u'GIS_DD_Tom_TEST.DANDAS.WW_LateralConnection.NodeID', u'GIS_DD_Tom_TEST.DANDAS.WW_LateralConnection.MainPipeID', u'GIS_DD_Tom_TEST.DANDAS.WW_LateralConnection.MeasuredFromNodeID', 'SHAPE@']

    Pointscursor = arcpy.da.SearchCursor(joinres2,joinfields2)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])
    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for (nodeID,pipeID,measure,point) in Pointscursor:
        if LateralDict.has_key(pipeID):
            mindistance = 999999
            for lateral in LateralDict.get(pipeID):
                distance = point.distanceTo(lateral)
                if distance < mindistance:
                    mindistance = distance
            if mindistance > 0.002:
                cursorI.insertRow(["LateralConnection and MainPipe","Pipe and Node","",globalScriptSettings.getErrID(),pipeID,nodeID,float(mindistance)])
                errcount += 1

    del cursorI
    del Pointscursor
    del Pipecursor
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.Delete_management(joinres)
    arcpy.Delete_management(joinres2)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)
    arcpy.Delete_management(view3)
    arcpy.Delete_management(view4)

    returnValue = errcount
    return returnValue