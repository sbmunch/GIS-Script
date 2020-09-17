#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Finding Nodes with an invalid ComplexStructureID using a join
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

def NodeRefrence(errtype,inDB1,inDB2,outDB,logDB):

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    #joinres = arcpy.AddJoin_management(arcpy.SelectLayerByAttribute_management(inDB1,"NEW_SELECTION","NOT ComplexStructureID IS NULL"),"ComplexStructureID",inDB2,"ObjectID","KEEP_ALL")

    #arcpy.MakeFeatureLayer_management()
    view = arcpy.MakeTableView_management(inDB1,"tempview","NOT ComplexStructureID IS NULL")
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    joinres = arcpy.AddJoin_management(view,"ComplexStructureID",view2,"ObjectID","KEEP_ALL")

    joinfields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "ComplexStructureID" in x.name]


    cursorSwhere = arcpy.da.SearchCursor(joinres,joinfields,[x.name for x in arcpy.ListFields(joinres) if "ComplexStructure.ObjectID" in x.name][0] + " IS NULL")

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    for row in cursorSwhere:
        cursorI.insertRow(["Join on RefrenceID","Knude","",globalScriptSettings.getErrID(),row[0],row[1]])
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
