#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Find the TV inspections with invalid pipe refrence
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

def TVCCInRefrence(errtype,inDB1,inDB2,inDB3,outDB,logDB):

    #inDB1 is TVCCInspection
    #inDB2 is Report
    #inDB3 is PipeReport

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")
    view3 = arcpy.MakeTableView_management(inDB3,"tempview3")

    joinres = arcpy.AddJoin_management(view,"ReportID",view2,"ObjectID","KEEP_ALL")
    joinres2 = arcpy.AddJoin_management(joinres,[x.name for x in arcpy.ListFields(joinres) if "Report.ObjectID" in x.name][0],view3,"ReportID","KEEP_ALL")

    joinfields = [x.name for x in arcpy.ListFields(joinres2) if "ObjectID" in x.name or "InActive" in x.name]
#[u'GIS_VCS_DD_TEST.DANDAS.WW_CCTVInspection.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_CCTVInspection.InActive', u'GIS_VCS_DD_TEST.DANDAS.WW_Report.ObjectID', u'GIS_VCS_DD_TEST.DANDAS.WW_PipeReport.ObjectID']

    cursorSwhere = arcpy.da.SearchCursor(joinres2,joinfields,[x.name for x in arcpy.ListFields(joinres2) if "PipeReport.ObjectID" in x.name][0] + " IS NULL")

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorSwhere:
        cursorI.insertRow(["Join with Report and PipeReport","TVCCInspection","",globalScriptSettings.getErrID(),row[0],row[1]])
        errcount += 1
    del cursorI
    del cursorSwhere
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.RemoveJoin_management(joinres2)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)
    arcpy.Delete_management(view3)

    returnValue = errcount
    return returnValue
