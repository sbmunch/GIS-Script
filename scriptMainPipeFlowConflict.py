#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Checks if a mainpipe contains a pipe with conflicting flow
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

def MainpipeFlow(errtype,inDB1,inDB2,outDB,logDB):

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview","NOT MainPipeID IS NULL") #pipe
    view2 = arcpy.MakeTableView_management(inDB2,"tempview2") #mainpipe

    joinres = arcpy.AddJoin_management(view,"MainPipeID",view2,"ObjectID","KEEP_COMMON")

    joinfields = [x.name for x in arcpy.ListFields(joinres) if "ObjectID" in x.name or "UpstreamNodeID" in x.name or "DownstreamNodeID" in x.name]

#[u'GIS_DD_Tom_TEST.DANDAS.WW_Pipe.ObjectID', u'GIS_DD_Tom_TEST.DANDAS.WW_Pipe.UpstreamNodeID', u'GIS_DD_Tom_TEST.DANDAS.WW_Pipe.DownstreamNodeID',
# u'GIS_DD_Tom_TEST.DANDAS.WW_MainPipe.ObjectID', u'GIS_DD_Tom_TEST.DANDAS.WW_MainPipe.UpstreamNodeID', u'GIS_DD_Tom_TEST.DANDAS.WW_MainPipe.DownstreamNodeID']

    cursorSwhere = arcpy.da.SearchCursor(joinres,joinfields)

    UpDownNodeDict = {}

    #MainPipeflow = (MainUP,MainDown,[(PipeID,pipeUD,pipeDown)...])
    # key is main pipe ID
    for row in cursorSwhere:
        if UpDownNodeDict.has_key(row[3]):
            MainPipeflow = UpDownNodeDict.pop(row[3])
            MainPipeflow[2].append((row[0],row[1],row[2]))
            UpDownNodeDict[row[3]] = MainPipeflow
        else:
            MainPipeflow = (row[4],row[5],[(row[0],row[1],row[2])])
            UpDownNodeDict[row[3]] = MainPipeflow

    del cursorSwhere

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])
    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    CurrentNode = 0
    for MainID,(mainUP,mainDOWN,nodeList) in UpDownNodeDict.items():

        res = CheckifFlow(MainID,mainUP,mainDOWN,nodeList)

        if res[0] == 1: # 1=YES, there is an error
            cursorI.insertRow(["Join on MainPipe","Delledning","PipeObjID is 0 if it couldnt be determined",globalScriptSettings.getErrID(),res[1],res[2],res[3]])
            errcount += 1
        elif res[0] == 2: # 2=YES, there is an dangling pipe error
            danglinglist = res[3]
            cursorI.insertRow(["Join on MainPipe","Delledning","Dangling pipe(s) on main pipe, only giving one PipeObjID",globalScriptSettings.getErrID(),res[1],danglinglist[0][0],danglinglist[0][1]])
            errcount += 1

    del cursorI
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.RemoveJoin_management(joinres)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)

    returnValue = errcount
    return returnValue

def CheckifFlow(MainID,CurrentNode,mainDOWN,nodeList):

    thislist = []
    #check that I can get from mainUP to mainDown, following the up->down paths in the nodeList
    #if cannot, save the MainID, PipeID and the NodeID which gave the conflict.
    if (CurrentNode == mainDOWN):
        #can also check for "dangling pipes" here, if any pipes remain in nodeList.
        if not nodeList:
            return (0,0,0,0)
        else:
            return (2,MainID,0,nodeList)

    for (ID,UP,DOWN) in nodeList:
        if UP == CurrentNode:
            nodeList.remove((ID,UP,DOWN))
            return CheckifFlow(MainID,DOWN,mainDOWN,nodeList)

    #if I reach this spot, no flow
    for (ID,UP,DOWN) in nodeList:
        if DOWN == CurrentNode:
            return (1,MainID,ID,CurrentNode)

    return (1,MainID,0,CurrentNode)
