#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Finding laterals with invalid mainpipe refrence
#
# Author:      sa-sbm
#
# Created:     11-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings

def LateralRefrence(errtype,inDB1,inDB2,outDB,logDB):

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview","NOT MainPipeID IS NULL")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    joinres = arcpy.AddJoin_management(view,"MainPipeID",view2,"ObjectID","KEEP_ALL")

    joinfields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "MainPipeID" in x.name]

    cursorSwhere = arcpy.da.SearchCursor(joinres,joinfields,[x.name for x in arcpy.ListFields(joinres) if "MainPipe.ObjectID" in x.name][0] + " IS NULL")

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorSwhere:
        cursorI.insertRow(["Join on RefrenceID","LateralConnection","",globalScriptSettings.getErrID(),row[0],row[1]])
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
