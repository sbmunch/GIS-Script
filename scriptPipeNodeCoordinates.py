#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Comparing Pipe and Node shapefiles to check if they are connected
#
# Author:      sa-sbm
#
# Created:     17-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings
import math

def CoordinateCheck(errtype,inDB1,inDB2,outDB,logDB):

    #inDB1 is pipe
    #inDB2 is Node

    returnValue = 0
    errcount = 0
    dateofrun = datetime.datetime.now()

    view = arcpy.MakeTableView_management(inDB1,"tempview")

    fields = [x.name for x in arcpy.ListFields(inDB1) if "ObjectID" in x.name or "PipeID" in x.name or "NodeID" in x.name or "XCoordinate" in x.name or "YCoordinate" in x.name]
    fields.append("SHAPE@")

    cursorS = arcpy.da.SearchCursor(view,fields)

#[u'ObjectID', u'MainPipeID', u'UpstreamNodeID', u'DownstreamNodeID', 'SHAPE@']

    # NodeID : [(pipeID,firstX,firstY,lastX,lastY)..] from pipe
    nodeDict = {}
    for row in cursorS:
        firstcord = row[4].firstPoint
        lastcord = row[4].lastPoint
        if nodeDict.has_key(row[2]):
            nodeList = nodeDict.pop(row[2])
            nodeList.append((row[0],round(firstcord.X,4),round(firstcord.Y,4),round(lastcord.X,4),round(lastcord.Y,4)))
            nodeDict[row[2]] = nodeList
        else:
            nodeDict[row[2]] = [(row[0],round(firstcord.X,4),round(firstcord.Y,4),round(lastcord.X,4),round(lastcord.Y,4))]

        if nodeDict.has_key(row[3]):
            nodeList = nodeDict.pop(row[3])
            nodeList.append((row[0],round(firstcord.X,4),round(firstcord.Y,4),round(lastcord.X,4),round(lastcord.Y,4)))
            nodeDict[row[3]] = nodeList
        else:
            nodeDict[row[3]] = [(row[0],round(firstcord.X,4),round(firstcord.Y,4),round(lastcord.X,4),round(lastcord.Y,4))]

    del cursorS
    arcpy.Delete_management(view)

    view2 = arcpy.MakeTableView_management(inDB2,"tempview2")

    Sfields = [x.name for x in arcpy.ListFields(inDB2) if "ObjectID" in x.name or "XCoordinate" in x.name or "YCoordinate" in x.name]
    Sfields.append("SHAPE@XY")

#[u'ObjectID', u'XCoordinate', u'YCoordinate', 'SHAPE@XY']

    cursorS = arcpy.da.SearchCursor(view2,Sfields)

    cursorI = arcpy.da.InsertCursor(outDB,[x.name for x in arcpy.ListFields(outDB)[1:]])

    logcursorI = arcpy.da.InsertCursor(logDB,[x.name for x in arcpy.ListFields(logDB)[1:]])

    # pipeID : (X,Y)  already spent point
    pipeDict = {}
    for row in cursorS:

        nodeList = nodeDict.pop(row[0],[])
        for (ID,firstXcoord,firstYcoord,lastXcoord,lastYcoord) in nodeList:

            distance1 = abs( math.sqrt( round( math.pow(row[3][0] - firstXcoord,2) + math.pow(row[3][1] - firstYcoord,2) ,4) ) )
            distance2 = abs( math.sqrt( round( math.pow(row[3][0] - lastXcoord,2) + math.pow(row[3][1] - lastYcoord,2) ,4) ) )

            if distance1 < distance2:
                if distance1 > 0.002 and (firstXcoord,firstYcoord) != pipeDict.get(ID,(0,0)):
                    pipeDict[ID] = (firstXcoord,firstYcoord)
                    cursorI.insertRow(["Node Shapefile X and Y coordinates","Pipe","",globalScriptSettings.getErrID(),ID,row[0],float(distance1)])
                    errcount += 1

            else:
                if distance2 > 0.002 and (lastXcoord,lastYcoord) != pipeDict.get(ID,(0,0)):
                    pipeDict[ID] = (lastXcoord,lastYcoord)
                    cursorI.insertRow(["Node Shapefile X and Y coordinates","Pipe","",globalScriptSettings.getErrID(),ID,row[0],float(distance2)])
                    errcount += 1

    del cursorI
    del cursorS
    logcursorI.insertRow([dateofrun,errtype,errcount,globalScriptSettings.getRunCount()])
    del logcursorI
    arcpy.Delete_management(view2)

    returnValue = errcount
    return returnValue