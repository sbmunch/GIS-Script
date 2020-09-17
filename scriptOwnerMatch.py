#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Makes sure owner and owner code match
#
# Author:      sa-sbm
#
# Created:     12-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings

def Ownercheck(errtype,inDB1,inDB2,outDB,logDB):

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    ownerandcode = []

    fields = [x.name for x in arcpy.ListFields(inDB1) if "ObjectID" in x.name or "OwnerID" in x.name or "OwnerCode" in x.name]

    cursorS = arcpy.da.SearchCursor(inDB2,[x.name for x in arcpy.ListFields(inDB2) if "ObjectID" in x.name or "OwnerCode" in x.name])

    for row in cursorS:
        ownerandcode.append((row[0],row[1]))

    del cursorS

    #ownerandcode = ownerandcode + [(y,x) for (x,y) in ownerandcode]

    cursorS = arcpy.da.SearchCursor(inDB1,fields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorS:
        #if (row[2],row[3]) in ownerandcode and (row[3],row[2]) in ownerandcode:
        if (row[2],row[3]) in ownerandcode:
            pass
        else:
            cursorI.insertRow(["Comparing with Ejer","MainPipe","",globalScriptSettings.getErrID(),row[0],row[2],row[3]])
            errcount += 1

    del cursorI
    del cursorS
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI

    returnValue = errcount
    return returnValue