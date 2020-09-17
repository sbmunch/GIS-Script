#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sa-sbm
#
# Created:     25-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings

def InvalidCover(errtype,inDB1,inDB2,outDB,logDB):

    #inDB1 is Cover
    #inDB2 is Node

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    joinres = arcpy.AddJoin_management(view,"NodeID",view2,"ObjectID","KEEP_COMMON")

    joinfields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "NodeTypeCode" in x.name]
#[u'GIS_VCS_DD_TEST.DANDAS.WW_Cover.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_Node.NodeTypeCode']

    cursorSwhere = arcpy.da.SearchCursor(joinres,joinfields,"NOT " + [x.name for x in arcpy.ListFields(joinres) if "Node.ObjectID" in x.name][0] + " IS NULL")

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorSwhere:
        if row[2] != 1 and row[2] != 4 and row[2] != 7 and row[2] != 8 and row[2] != 9 and row[2] != 10 and row[2] != 11 and row[2] != 12:
            cursorI.insertRow(["Join with Node","Cover","",globalScriptSettings.getErrID(),row[0],row[1],row[2]])
            errcount += 1
    del cursorI
    del cursorSwhere
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.RemoveJoin_management(joinres)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)

    returnValue = errcount
    return returnValue
