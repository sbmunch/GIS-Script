#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Makes sure only valid nodes are connected to more than 2 pipes
#
# Author:      sa-sbm
#
# Created:     26-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings
import math

def NodePipeCounting(errtype,inDB1,inDB2,outDB,logDB):

    #inDB1 is Pipe
    #inDB2 is Node

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    joinres = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "UpstreamNodeID" in x.name][0],view2,[x.name for x in arcpy.ListFields(view2) if "ObjectID" in x.name][0],"KEEP_COMMON")

    fields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "NodeTypeCode" in x.name]
    #[u'GIS_VCS_DD_TEST.DANDAS.WW_Pipe.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.NodeTypeCode']

    cursorS = arcpy.da.SearchCursor(joinres,fields)

    UpstreamDict = {}
    for row in cursorS:
        if UpstreamDict.has_key(row[1]):
            nodelist = UpstreamDict.pop(row[1])
            nodelist.append((row[0],row[2]))
            UpstreamDict[row[1]] = nodelist
        else:
            UpstreamDict[row[1]] = [(row[0],row[2])]

    arcpy.RemoveJoin_management(joinres)
    del cursorS

    joinres2 = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "DownstreamNodeID" in x.name][0],view2,[x.name for x in arcpy.ListFields(view2) if "ObjectID" in x.name][0],"KEEP_COMMON")

    cursorSearch = arcpy.da.SearchCursor(joinres2,fields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])
    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    caughtlist = set()
    for row in cursorSearch:

        #check here if Pipe only has 1 upstream and 1 downstream node. All Upstreams in dict. when typecode = 45, check list only contains 2.
        if row[2] == 45 and len(UpstreamDict.get(row[1],[])) != 1 and row[1] not in caughtlist:
            caughtlist.add(row[1])
            cursorI.insertRow(["Join with Node","Pipe","Typecode 45 with not exactly 1 upstream and downstream pipe",globalScriptSettings.getErrID(),row[1],row[2]])
            errcount += 1

        if UpstreamDict.has_key(row[1]):
            nodelist = UpstreamDict.pop(row[1])
            nodelist.append((row[0],row[2]))
            UpstreamDict[row[1]] = nodelist
        else:
            UpstreamDict[row[1]] = [(row[0],row[2])]

    for ID,pipelist in UpstreamDict.iteritems():
        if len(pipelist) > 2:
            if pipelist[0][1] != 1 and pipelist[0][1] != 20 and ID not in caughtlist:
                cursorI.insertRow(["Join with Node","Pipe","",globalScriptSettings.getErrID(),ID,pipelist[0][1]])
                errcount += 1

    del cursorSearch
    arcpy.RemoveJoin_management(joinres2)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)
    del cursorI
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI

    returnValue = errcount
    return returnValue
