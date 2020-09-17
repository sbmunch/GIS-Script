#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Making sure all MainPipes contains atleast 1 Pipe
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

def MainPipePipes(errtype,inDB1,inDB2,outDB,logDB):

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    #view = arcpy.MakeTableView_management(inDB1,"tempview")
    #view2 = arcpy.MakeTableView_management(inDB2,"tempview2")
    #FT2 = arcpy.MakeFeatureLayer_management(inDB2,"tempFL")

    #joinres = arcpy.AddJoin_management(view,"ObjectID",FT2,"MainPipeID","KEEP_ALL")

    #view2 loses all its entries when joining for some reason
    #joinfields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "NodeID" in x.name]

    pipesaccountedfor = []

    fields = [x.name for x in arcpy.ListFields(inDB1) if "ObjectID" in x.name or "NodeID" in x.name]

    cursorS = arcpy.da.SearchCursor(inDB2,["MainPipeID"],"NOT MainPipeID IS NULL")

    for row in cursorS:
        pipesaccountedfor.append(row[0])

    del cursorS

    setpipesaccountedfor = set(pipesaccountedfor)

    cursorS = arcpy.da.SearchCursor(inDB1,fields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorS:
        if row[0] in setpipesaccountedfor:
            pass
        else:
            cursorI.insertRow(["Loop over Delledning","MainPipe","",globalScriptSettings.getErrID(),row[0],row[1],row[2]])
            errcount += 1
    del cursorI
    del cursorS
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    #arcpy.RemoveJoin_management(joinres)
    #arcpy.Delete_management(view)
    #arcpy.Delete_management(view2)

    returnValue = errcount
    return returnValue
