#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checks for Nodes that are closer than 2cm to eachother
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
import math

def ClosenesCheck(errtype,inDB1,outDB,logDB):

    #inDB1 is Node

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")

    fields = [x.name for x in arcpy.ListFields(view) if "ObjectID" in x.name or "NodeTypeCode" in x.name]
    fields.append("SHAPE@XY")
    #[u'ObjectID', u'NodeTypeCode', 'SHAPE@XY']

    closenesDictX = {}

    cursorS = arcpy.da.SearchCursor(view,fields)

    for (ID,typecode,(X,Y)) in cursorS:
        coordkey = ((round(X,2),round(Y,2)))

        if closenesDictX.has_key(coordkey):
            coordlist = closenesDictX.pop(coordkey)
            coordlist.append((ID,typecode,coordkey))
            closenesDictX[coordkey] = coordlist
        else:
            closenesDictX[coordkey] = [(ID,typecode,coordkey)]

    cursorS.reset()

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])
    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    caughtlist = set()
    for (ID,typecode,(X,Y)) in cursorS:
        coordkey = ((round(X,2),round(Y,2)))
        for i in range(5):
            for j in range(5):
                Xcoordround = round(round(X,2)-0.02+i*0.01,2)
                Ycoordround = round(round(Y,2)-0.02+j*0.01,2)
                if closenesDictX.has_key((Xcoordround,Ycoordround)):
                    closelist = closenesDictX.get((Xcoordround,Ycoordround))
                    for (IDclose,typecodeclose,(Xclose,Yclose)) in closelist:
                        distance = math.sqrt(pow(round(X,2)-Xclose,2)+pow(round(Y,2)-Yclose,2))
                        if distance <= 0.02 and ID != IDclose and (ID,IDclose) not in caughtlist:
                            caughtlist.add((IDclose,ID))
                            cursorI.insertRow(["","Node","",globalScriptSettings.getErrID(),ID,typecode,IDclose,typecodeclose])
                            errcount += 1

    del cursorS
    arcpy.Delete_management(view)
    del cursorI
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI

    returnValue = errcount
    return returnValue
