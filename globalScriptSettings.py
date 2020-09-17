#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     header file for global variables and settings
#
# Author:      sa-sbm
#
# Created:     10-02-2020
#-------------------------------------------------------------------------------

import os
try:
    import cPickle as pickle
except:
    import pickle

#arbitrary numbers, real ones gotten from file
spentID = 101
runcount = 41

datafilepath = "scriptdata.txt"
dbpathdict = {
"ErrLog" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\ErrBacklog',
"DB_ErrType1" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType1',
"DB_ErrType2" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType2',
"DB_ErrType3" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType3',
"DB_ErrType4" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType4',
"DB_ErrType5" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType5',
"DB_ErrType6" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType6',
"DB_ErrType7" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType7',
"DB_ErrType8" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType8',
"DB_ErrType9" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType9',
"DB_ErrType10" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType10',
"DB_ErrType11" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType11',
"DB_ErrType12" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType12',
"DB_ErrType13" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType13',
"DB_ErrType14" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType14',
"DB_ErrType15" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType15',
"DB_ErrType16" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType16',
"DB_ErrType17" : r'C:\Users\sa-sbm\OneDrive - Samaqua A S\PythonScripts\dbsTables\TestTables.gdb\DB_ErrType17',
"Knude" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WasteWater\GIS_VCS_DD_TEST.DANDAS.WW_Node',
"KompleksBygvaerk" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WasteWater\GIS_VCS_DD_TEST.DANDAS.WW_ComplexStructure',
"Stik" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_LateralConnection',
"Hovedledning" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_MainPipe',
"Cover" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_Cover',
"Delledning" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WasteWater\GIS_VCS_DD_TEST.DANDAS.WW_Pipe',
"Ejer" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_Owner',
"TVInspection" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WasteWater\GIS_VCS_DD_TEST.DANDAS.WW_CCTVInspection',
"Report" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_Report',
"ReportFromToward" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_ReportFromToward',
"CCTVObs" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_CCTVObs',
"PipeEvent" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_PipeEvent',
"PipeReport" : r'K:\GIS\CKL\Til SBM\TEST@WA@GIS_VCS_DD_TEST@geodata.sde\GIS_VCS_DD_TEST.DANDAS.WW_PipeReport'
}
workspace = ""

def script_Init():
    #get ints from file: Runcount so far, SpentIDs
    datafile = open(datafilepath,"rb")
    global spentID
    global runcount
    datalist = pickle.load(datafile)
    spentID = datalist[0]
    runcount = datalist[1]
    datafile.close()
    runcount += 1
    return 0

def script_Exit():
    datafile = open(datafilepath,"wb")
    global spentID
    global runcount
    pickle.dump([spentID,runcount],datafile)
    datafile.close()
    return 0

#overwrites the saved error ID and run ID with inputs
def overwritecounters(NEWspentID,NEWruncount):
    datafile = open(datafilepath,"wb")
    pickle.dump([NEWspentID,NEWruncount],datafile)
    datafile.close()
    return 0

def getErrID():
    global spentID
    spentID += 1
    return spentID

def getRunCount():
    global runcount
    #runcount += 1
    return runcount

def getDB(dbname):
    global dbpathdict
    return dbpathdict.get(dbname,"not found")

#dont think below works for sde databases

#def validateDB(dbname):
#    global dbpathdict
#    if dbpathdict.has_key(dbname):
#        print dbpathdict.get(dbname)
#        return os.path.exists(dbpathdict.get(dbname))
#    return False

#def validateAllDB():
#    global dbpathdict
#    res = True
#    for key in dbpathdict:
#        if not validateDB(key):
#            print "DB error: " + str(key)
#            res = False
#    return res
