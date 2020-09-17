#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checks if the CCTV report node is correct according to ClockAnalogy
#
# Author:      sa-sbm
#
# Created:     13-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings

def Clockrefrence(errtype,inDB1,inDB2,inDB3,inDB4,inDB5,outDB,logDB):

    #inDB1 is CCTVInspection
    #inDB2 is Report
    #inDB3 is ReportFromToward
    #inDB4 is FraKnude
    #inDB5 is LateralConnection

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview","InActive = 0")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")
    view3 = arcpy.MakeTableView_management(inDB3,"tempview3")

    joinres = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "ID" in x.name][1],view2,[x.name for x in arcpy.ListFields(view2) if "ID" in x.name][0],"KEEP_COMMON")

    joinres2 = arcpy.AddJoin_management(joinres,[x.name for x in arcpy.ListFields(joinres) if "ReportID" in x.name][0],view3,[x.name for x in arcpy.ListFields(view3) if "ReportID" in x.name][0],"KEEP_COMMON")

    joinfields = [x.name for x in arcpy.ListFields(joinres2) if "ObjectID" in x.name or "ClockAnalog" in x.name or "ReportNumber" in x.name or "DocumentName" in x.name or "FromNodeID" in x.name or "ReportTypeCode" in x.name]

    cursorSwhere = arcpy.da.SearchCursor(joinres2,joinfields,[x.name for x in arcpy.ListFields(joinres2) if "ReportTypeCode" in x.name][0] + " = 15 OR " + [x.name for x in arcpy.ListFields(joinres2) if "ReportTypeCode" in x.name][0] + " = 17")

    #dict elements:
    #FromNodeID : [(ClockAnalog,ObjectID,ReportNumber,ReportName)]

    ReportClockDict = {}

    for row in cursorSwhere:
        if ReportClockDict.has_key(row[7]):
            ReportClock = ReportClockDict.pop(row[7])
            ReportClock.append((row[1],row[0],row[2],row[3]))
            ReportClockDict[row[7]] = ReportClock
        else:
            ReportClockDict[row[7]] = [(row[1],row[0],row[2],row[3])]

    del cursorSwhere
    arcpy.RemoveJoin_management(joinres2)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)
    arcpy.Delete_management(view3)

    view4 = arcpy.MakeTableView_management(inDB4,"tempview4")  #Knude
    view5 = arcpy.MakeTableView_management(inDB5,"tempview5") #lateralconnection

    joinres3 = arcpy.AddJoin_management(view4,"ObjectID",view5,[x.name for x in arcpy.ListFields(view5) if "NodeID" in x.name][0],"KEEP_COMMON")

    joinfields2 = [x.name for x in arcpy.ListFields(joinres3) if "ObjectID" in x.name or "NodeName" in x.name or "ClockAnalog" in x.name]

#[u'GIS_VCS_DD_TEST.DANDAS.WW_Node.ObjectID',
# u'GIS_VCS_DD_TEST.DANDAS.WW_Node.NodeName',
#  u'GIS_VCS_DD_TEST.DANDAS.WW_Node.PreviousNodeName',
#   u'GIS_VCS_DD_TEST.DANDAS.WW_LateralConnection.ObjectID',
#    u'GIS_VCS_DD_TEST.DANDAS.WW_LateralConnection.ClockAnalogy']

    cursorSwhere = arcpy.da.SearchCursor(joinres3,joinfields2,"NOT " + [x.name for x in arcpy.ListFields(joinres3) if "ClockAnalog" in x.name][0] + " IS NULL")

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])
    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorSwhere:

        checkclock = ReportClockDict.pop(row[0],[])
        #checkclocklist = [x for (x,y,z,w) in checkclock]

        for (ClockAnalog,ObjectID,ReportNumber,ReportName) in checkclock:
            #if row[4] not in checkclocklist and row[4] != ClockAnalog:

            if row[4] != ClockAnalog:
                #get Inspection ID, ReportID, ReportName, NodeID, NodeName,
                cursorI.insertRow(["Join on Report, ReportFromToward and join on LateralConnection","CCTVInspection and Knude","",globalScriptSettings.getErrID(),ObjectID,ReportNumber,ReportName,row[0],row[1]])
                errcount += 1

    del cursorSwhere
    del cursorI
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.RemoveJoin_management(joinres3)
    arcpy.Delete_management(view4)
    arcpy.Delete_management(view5)

    returnValue = errcount
    return returnValue