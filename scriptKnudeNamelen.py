#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Using len() to find all Node names longer than 30 chars
#
# Author:      sa-sbm
#
# Created:     10-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings

def NamelenTest(errtype,inDB,outDB,logDB):

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    cursorS = arcpy.da.SearchCursor(inDB,"*","len(" + arcpy.ListFields(inDB)[1].name + ") > 30")
    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])
    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])
    for row in cursorS:
        cursorI.insertRow(["len(name)","Knude","",globalScriptSettings.getErrID(),row[0],row[1]])
        errcount += 1
    del cursorI
    del cursorS
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI

    returnValue = errcount
    return returnValue
