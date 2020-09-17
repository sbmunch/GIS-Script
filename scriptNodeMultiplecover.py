#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Looks for nodes with multiple covers
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

def NodeMulCover(errtype,inDB,outDB,logDB):

    #find NodeIDs from Cover with multiple occourences, can find both covers and nodes from NodeIDs

    returnValue = 0
    errcount = 0
    uniqueList = []
    duplicateList = []
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB,"tempview","NOT NodeID IS NULL")

    cursorS = arcpy.da.SearchCursor(view,[x.name for x in arcpy.ListFields(inDB)[:2]])

    for row in cursorS:
        if row[1] in uniqueList:
            duplicateList.append(row[1])
        else:
            uniqueList.append(row[1])

    setduplicateList = set(duplicateList)

    cursorS.reset()

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorS:
        if row[1] in setduplicateList:
            cursorI.insertRow(["Found duplicate NodeID","Cover","",globalScriptSettings.getErrID(),row[0],row[1]])
            errcount += 1
    del cursorI
    del cursorS
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.Delete_management(view)

    returnValue = errcount
    return returnValue
