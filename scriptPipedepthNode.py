#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checking pipe connection is between the nodes ground and invert
#
# Author:      sa-sbm
#
# Created:     27-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings
import math

def PipeDepthCheck(errtype,inDB1,inDB2,outDB,logDB):

    #inDB1 is Pipe
    #inDB2 is Node

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    joinres = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "UpstreamNodeID" in x.name][0],view2,[x.name for x in arcpy.ListFields(view2) if "ObjectID" in x.name][0],"KEEP_COMMON")

    fields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "InvertLevel" in x.name or "GroundLevel" in x.name]
#[u'GIS_VCS_DD_TEST.DANDAS.WW_Pipe.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_Pipe.UpstreamInvertLevel', u'GIS_VCS_DD_TEST.DANDAS.WW_Pipe.DownstreamInvertLevel', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.InvertLevel', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.InvertLevelOriginID', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.GroundLevel', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.GroundLevelOriginID']

    cursorS = arcpy.da.SearchCursor(joinres,fields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    #UpstreamDict = {}
    for row in cursorS:
        if (isinstance(row[1],float) or isinstance(row[1],int)) and (isinstance(row[4],float) or isinstance(row[4],int) ) and (isinstance(row[6],float) or isinstance(row[6],int) ):
            if row[1] < row[4] or row[1] > row[6]:
                cursorI.insertRow(["Join with Node","Pipe","Upstream",globalScriptSettings.getErrID(),row[0],row[3],row[6],row[1],row[4]])
                errcount += 1
        else:
            cursorI.insertRow(["Join with Node","Pipe","Upstream",globalScriptSettings.getErrID(),row[0],row[3],row[6],row[1],row[4]])
            errcount += 1

    arcpy.RemoveJoin_management(joinres)
    del cursorS

    joinres2 = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "DownstreamNodeID" in x.name][0],view2,[x.name for x in arcpy.ListFields(view2) if "ObjectID" in x.name][0],"KEEP_COMMON")

    cursorSearch = arcpy.da.SearchCursor(joinres2,fields)

    #caughtlist = set()
    for row in cursorSearch:
        if (isinstance(row[2],float) or isinstance(row[2],int)) and (isinstance(row[4],float) or isinstance(row[4],int) ) and (isinstance(row[6],float) or isinstance(row[6],int) ):
            if row[2] < row[4] or row[2] > row[6]:
                cursorI.insertRow(["Join with Node","Pipe","Downstream",globalScriptSettings.getErrID(),row[0],row[3],row[6],row[2],row[4]])
                errcount += 1
        else:
            cursorI.insertRow(["Join with Node","Pipe","Downstream",globalScriptSettings.getErrID(),row[0],row[3],row[6],row[2],row[4]])
            errcount += 1

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    del cursorSearch
    arcpy.RemoveJoin_management(joinres2)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)
    del cursorI
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI

    returnValue = errcount
    return returnValue
