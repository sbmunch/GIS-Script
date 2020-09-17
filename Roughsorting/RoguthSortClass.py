#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Locating pipes with a K4 (some K3 and K2) critical class
#
# Author:      sa-sbm
#
# Created:     18-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys

def main():

    CCTVObs = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WW_CCTVObs'
    PipeEvent = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WW_PipeEvent'
    Report = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WW_Report'
    PipeReport = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WW_PipeReport'

    CCTVInspection = 'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WasteWater\WW_CCTVInspection'

    Pipe = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WasteWater\WW_Pipe'
    MainPipe = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WW_MainPipe'
    Node = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\WasteWater\WW_Node'

    OutputDB = r'K:\GIS\CKL\Til SBM\DataTilHELLE\GIS_VCS_DD_15012020.gdb\RoughSortingFeatureClass'

    #view = arcpy.MakeTableView_management(CCTVObs,"CCTVview","CCTVObsClass = 4 OR ( CCTVObsClass = 3 AND (CCTVObsCode = 17 OR CCTVObsCode = 9 OR CCTVObsCode = 4 )) OR ( CCTVObsClass = 2 AND CCTVObsCode = 4 )")
    # arcpy refusing to run above SQL, so I have to check them in the insertion

    view = arcpy.MakeTableView_management(CCTVObs,"CCTVview","CCTVObsClass <= 4")
    view2 = arcpy.MakeTableView_management(PipeEvent,"PipeEventview2")
    view3 = arcpy.MakeTableView_management(Report,"Reportview3")
    view4 = arcpy.MakeTableView_management(PipeReport,"PipeReportview4")
    view5 = arcpy.MakeTableView_management(CCTVInspection,"CCTVInspectionview5")

    joinres = arcpy.AddJoin_management(view,[x.name for x in arcpy.ListFields(view) if "PipeEventID" in x.name][0],view2,[x.name for x in arcpy.ListFields(view2) if "ObjectID" in x.name][0],"KEEP_COMMON")
    joinres2 = arcpy.AddJoin_management(joinres,[x.name for x in arcpy.ListFields(joinres) if "ReportID" in x.name][0],view3,[x.name for x in arcpy.ListFields(view3) if "ObjectID" in x.name][0],"KEEP_COMMON")
    joinres3 = arcpy.AddJoin_management(joinres2,[x.name for x in arcpy.ListFields(joinres2) if "Report.ObjectID" in x.name][0],view4,[x.name for x in arcpy.ListFields(view4) if "ReportID" in x.name][0],"KEEP_COMMON")
    joinres4 = arcpy.AddJoin_management(joinres3,[x.name for x in arcpy.ListFields(joinres2) if "Report.ObjectID" in x.name][0],view5,[x.name for x in arcpy.ListFields(view5) if "ReportID" in x.name][0],"KEEP_ALL")

    joinfields = [x.name for x in arcpy.ListFields(joinres4) if "ReportNumber" in x.name or "MainPipeID" in x.name or "DateConducted" in x.name or "CCTVObsClass" in x.name or "CCTVObsCode" in x.name or "PhysicalIndex" in x.name]

#[u'WW_CCTVObs.CCTVObsCode', u'WW_CCTVObs.CCTVObsClass', u'WW_Report.ReportNumber', u'WW_Report.DateConducted', u'WW_PipeReport.MainPipeID', u'WW_CCTVInspection.PhysicalIndex']

    SearchCursor = arcpy.da.SearchCursor(joinres4,joinfields,"NOT " + [x.name for x in arcpy.ListFields(joinres4) if "DateConducted" in x.name][0] + " IS NULL")

    # MainPipeID : [(Code,Class,ReportNumber,Date,index),..] from join
    ObsReportDict = {}
    for row in SearchCursor:
        if row[1] == 4 or (row[1] == 3 and (row[0] == 4 or row[0] == 9 or row[0] == 17)) or (row[1] == 2 and row[0] == 4): #SQL compare
            if row[3] >= datetime.datetime(2018,01,01) and row[3] < datetime.datetime(2020,01,01):
                if ObsReportDict.has_key(row[4]):
                    reportList = ObsReportDict.pop(row[4])
                    reportList.append((row[0],row[1],row[2],row[3],row[5]))
                    ObsReportDict[row[4]] = reportList
                else:
                    ObsReportDict[row[4]] = [(row[0],row[1],row[2],row[3],row[5])]

    del SearchCursor
    arcpy.RemoveJoin_management(joinres4)
    arcpy.Delete_management(view)
    arcpy.Delete_management(view2)
    arcpy.Delete_management(view3)
    arcpy.Delete_management(view4)
    arcpy.Delete_management(view5)

    #Only keep most recent report observation pr mainpipe.
    ObsReportDictDone = {}
    for key,reportlist in ObsReportDict.iteritems():
        recentdate = (0,0,"",datetime.datetime(1,1,1),0.0)
        for (obscode,obsclass,reportnr,condate,index) in reportlist:
            if recentdate[3] < condate:
                recentdate = (obscode,obsclass,reportnr,condate,index)

        ObsReportDictDone[key] = recentdate

    del ObsReportDict

    view6 = arcpy.MakeTableView_management(Pipe,"Pipeview","NOT " + [x.name for x in arcpy.ListFields(Pipe) if "MainPipeID" in x.name][0] + " IS NULL")
    view7 = arcpy.MakeTableView_management(MainPipe,"MainPipeview")
    view8 = arcpy.MakeTableView_management(Node,"Nodeview")

    #Need to join twice, as I cannot join with node (upstream and downstream node) twice on the same table.

    joinres5 = arcpy.AddJoin_management(view7,[x.name for x in arcpy.ListFields(view7) if "UpstreamNodeID" in x.name][0],view8,[x.name for x in arcpy.ListFields(view8) if "ObjectID" in x.name][0],"KEEP_ALL")

    joinfields2 = [x.name for x in arcpy.ListFields(joinres5) if "MainPipe.ObjectID" in x.name or "Node.NodeName" in x.name or "Node.InvertLevel" in x.name or "Node.GroundLevel" in x.name]

#[u'WW_MainPipe.ObjectID', u'WW_Node.NodeName', u'WW_Node.InvertLevel', u'WW_Node.InvertLevelOriginID', u'WW_Node.GroundLevel', u'WW_Node.GroundLevelOriginID']

    CursorS = arcpy.da.SearchCursor(joinres5,joinfields2)

    # MainPipeID : (obscode,obsclass,reportnr,condate,index,NodeName,InvertLevel,GroundLevel) from join
    UpstreamNodeDict = {}
    for row in CursorS:
        if ObsReportDictDone.has_key(row[0]):
            ObsReportElement = ObsReportDictDone.pop(row[0])
            UpstreamNodeDict[row[0]] = (ObsReportElement[0],ObsReportElement[1],ObsReportElement[2],ObsReportElement[3],ObsReportElement[4],row[1],row[2],row[4])

    del ObsReportDictDone
    del CursorS
    arcpy.RemoveJoin_management(joinres5)

    joinres6 = arcpy.AddJoin_management(view6,[x.name for x in arcpy.ListFields(view6) if "MainPipeID" in x.name][0],view7,[x.name for x in arcpy.ListFields(view7) if "ObjectID" in x.name][0],"KEEP_COMMON")
    joinres7 = arcpy.AddJoin_management(joinres6,[x.name for x in arcpy.ListFields(joinres6) if "MainPipe.DownstreamNodeID" in x.name][0],view8,[x.name for x in arcpy.ListFields(view8) if "ObjectID" in x.name][0],"KEEP_ALL")

    joinfields3 = [x.name for x in arcpy.ListFields(joinres7)
    if "Pipe.Slope" in x.name
    or "Pipe.MaterialCode" in x.name
    or "Pipe.MainDimension" in x.name
    or "Pipe.CrossSectionCode" in x.name
    or "Pipe.FeatureGUID" in x.name
    or "Pipe.Category" in x.name
    or "MainPipe.ObjectID" in x.name
    or "MainPipe.NetworkTypeCode" in x.name
    or "MainPipe.StatusCode" in x.name
    or "MainPipe.OwnerID" in x.name
    or "Node.NodeName" in x.name
    or "Node.InvertLevel" in x.name
    or "Node.GroundLevel" in x.name]
    joinfields3.append("SHAPE@")

#[u'WW_Pipe.Slope',
# u'WW_Pipe.MaterialCode',
# u'WW_Pipe.MainDimension',
# u'WW_Pipe.CrossSectionCode',
# u'WW_Pipe.FeatureGUID',
# u'WW_Pipe.Category',
# u'WW_MainPipe.ObjectID',   <- for dictionary key
# u'WW_MainPipe.NetworkTypeCode',
# u'WW_MainPipe.StatusCode',
# u'WW_MainPipe.OwnerID',
# u'WW_Node.NodeName',
# u'WW_Node.InvertLevel',
# u'WW_Node.InvertLevelOriginID',  <- skip
# u'WW_Node.GroundLevel',
# u'WW_Node.GroundLevelOriginID'] <- skip
# + SHAPE@

    outfields = [x.name for x in arcpy.ListFields(OutputDB)[3:-3]] #first three are shapefile generated, last three will have to be manually inserted
    outfields.append("SHAPE@")

    cursorSearch = arcpy.da.SearchCursor(joinres7,joinfields3)

    cursorI = arcpy.da.InsertCursor(OutputDB,outfields)

    errcount = 0
    for row in cursorSearch:
        if UpstreamNodeDict.has_key(row[6]):
            Elements = UpstreamNodeDict.get(row[6],(0,0,"",datetime.datetime(1,1,1),"",0,0))
            cursorI.insertRow([Elements[2],Elements[3],Elements[0],Elements[1],row[5],Elements[4],row[7],row[8],row[9],row[1],row[3],row[2],row[0],Elements[5],Elements[6],Elements[7],row[10],row[11],row[13],row[4],row[15]])
            errcount += 1
    del cursorI
    del cursorSearch

    print errcount

    arcpy.RemoveJoin_management(joinres7)
    arcpy.Delete_management(view6)
    arcpy.Delete_management(view7)
    arcpy.Delete_management(view8)

if __name__ == '__main__':
    main()
