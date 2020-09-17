#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     scripts for testing should be run from this as the main program
#
# Author:      sa-sbm
#
# Created:     10-02-2020
#-------------------------------------------------------------------------------

import arcpy
import datetime, time
import os
import sys
import globalScriptSettings as gSS
import scriptKnudeNamelen
import scriptNodevalidRefrence
import scriptLateralvalidRefrence
import scriptNodeMultiplecover
import scriptMainPipeMissingPipes
import scriptOwnerMatch
import scriptMainPipeFlowConflict
import scriptReportClockRefrence
import scriptCoverNodeCoordinates
import scriptPipeNodeCoordinates
import scriptShapeFieldCoordinates
import scriptLateralPipeCoordinates
import scriptTVInspectionvalidRefrence
import scriptCovervalidNode
import scriptNodetooclose
import scriptNodetoomanyPipes
import scriptPipedepthNode

def main():
    res = 0
    test = [17]#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

    if (1 in test):
        try:
            res += scriptKnudeNamelen.NamelenTest(1,gSS.getDB("Knude"),gSS.getDB("DB_ErrType1"),gSS.getDB("ErrLog"))
        except:
            print "test 1 failed"

    if (2 in test):
        try:
            res += scriptNodevalidRefrence.NodeRefrence(2,gSS.getDB("Knude"),gSS.getDB("KompleksBygvaerk"),gSS.getDB("DB_ErrType2"),gSS.getDB("ErrLog"))
        except:
            print "test 2 failed"

    if (3 in test):
        try:
            res += scriptLateralvalidRefrence.LateralRefrence(3,gSS.getDB("Stik"),gSS.getDB("Hovedledning"),gSS.getDB("DB_ErrType3"),gSS.getDB("ErrLog"))
        except:
            print "test 3 failed"

    if (4 in test):
        try:
            res += scriptNodeMultiplecover.NodeMulCover(4,gSS.getDB("Cover"),gSS.getDB("DB_ErrType4"),gSS.getDB("ErrLog"))
        except:
            print "test 4 failed"

    if (5 in test):
        try:
            res += scriptMainPipeMissingPipes.MainPipePipes(5,gSS.getDB("Hovedledning"),gSS.getDB("Delledning"),gSS.getDB("DB_ErrType5"),gSS.getDB("ErrLog"))
        except:
            print "test 5 failed"

    if (6 in test):
        try:
            res += scriptOwnerMatch.Ownercheck(6,gSS.getDB("Hovedledning"),gSS.getDB("Ejer"),gSS.getDB("DB_ErrType6"),gSS.getDB("ErrLog"))
        except:
            print "test 6 failed"

    if (7 in test):
        try:
            res += scriptMainPipeFlowConflict.MainpipeFlow(7,gSS.getDB("Delledning"),gSS.getDB("Hovedledning"),gSS.getDB("DB_ErrType7"),gSS.getDB("ErrLog"))
        except:
            print "test 7 failed"

    if (8 in test):
        try:
            res += scriptReportClockRefrence.Clockrefrence(8,gSS.getDB("TVInspection"),gSS.getDB("Report"),gSS.getDB("ReportFromToward"),gSS.getDB("Knude"),gSS.getDB("Stik"),gSS.getDB("DB_ErrType8"),gSS.getDB("ErrLog"))
        except:
            print "test 8 failed"

    if (9 in test):
        try:
            res += scriptCoverNodeCoordinates.CoordinateCheck(9,gSS.getDB("Cover"),gSS.getDB("Knude"),gSS.getDB("DB_ErrType9"),gSS.getDB("ErrLog"))
        except:
            print "test 9 failed"

    if (10 in test):
        try:
            res += scriptPipeNodeCoordinates.CoordinateCheck(10,gSS.getDB("Delledning"),gSS.getDB("Knude"),gSS.getDB("DB_ErrType10"),gSS.getDB("ErrLog"))
        except:
            print "test 10 failed"

    if (11 in test):
        try:
            res += scriptShapeFieldCoordinates.CoordinateCheck(11,gSS.getDB("Knude"),gSS.getDB("DB_ErrType11"),gSS.getDB("ErrLog"))
        except:
            print "test 11 failed"

    if (12 in test):
        try:
            res += scriptLateralPipeCoordinates.CoordinateCheck(12,gSS.getDB("Delledning"),gSS.getDB("Hovedledning"),gSS.getDB("Knude"),gSS.getDB("Stik"),gSS.getDB("DB_ErrType12"),gSS.getDB("ErrLog"))
        except:
            print "test 12 failed"

    if (13 in test):
        try:
            res += scriptTVInspectionvalidRefrence.TVCCInRefrence(13,gSS.getDB("TVInspection"),gSS.getDB("Report"),gSS.getDB("PipeReport"),gSS.getDB("DB_ErrType13"),gSS.getDB("ErrLog"))
        except:
            print "test 13 failed"

    if (14 in test):
        try:
            res += scriptCovervalidNode.InvalidCover(14,gSS.getDB("Cover"),gSS.getDB("Knude"),gSS.getDB("DB_ErrType14"),gSS.getDB("ErrLog"))
        except:
            print "test 14 failed"

    if (15 in test):
        try:
            res += scriptNodetooclose.ClosenesCheck(15,gSS.getDB("Knude"),gSS.getDB("DB_ErrType15"),gSS.getDB("ErrLog"))
        except:
            print "test 15 failed"

    if (16 in test):
        try:
            res += scriptNodetoomanyPipes.NodePipeCounting(16,gSS.getDB("Delledning"),gSS.getDB("Knude"),gSS.getDB("DB_ErrType16"),gSS.getDB("ErrLog"))
        except:
            print "test 16 failed"

    if (17 in test):
        try:
            res += scriptPipedepthNode.PipeDepthCheck(17,gSS.getDB("Delledning"),gSS.getDB("Knude"),gSS.getDB("DB_ErrType17"),gSS.getDB("ErrLog"))
        except:
            print "test 17 failed"

    print "testRunner Finished, " +str(res) +" errors found"
    return 0

if __name__ == '__main__':

    gSS.script_Init()
    res = main()
    gSS.script_Exit()
    sys.exit(res)