# ---------------------------------------------------------------------------
# Name:       ServiceAreaOfWatersheds.py
# Purpose:    This tool calculates the regulated, unregulated,impervious,
#             turf and forested areas of watershed layer and creates
#             an excel file
# Author:   	Nasir Ahmad
# Created:		20/06/2016
# ArcGIS Version: 	10.3
# Python Version: 	2.7.3
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os

# Parameters
mainLayer = arcpy.GetParameterAsText(0) # Main Layer
serviceAreaLayer = arcpy.GetParameterAsText(1) # Service Area Layer
otherServiceLayer = arcpy.GetParameterAsText(2) # Other service area
imperviousLayer = arcpy.GetParameterAsText(3) # Impervious Layer
forestLayer = arcpy.GetParameterAsText(4)# Forest Layer
identifier = arcpy.GetParameterAsText(5) # field identifier
excelOutput = arcpy.GetParameterAsText(6) # output to excel


# Set Environment Variables
path = os.path.dirname(excelOutput)
gdbname = "temp.gdb"
gdb = os.path.join(path,gdbname)
if not arcpy.Exists(gdb):
    arcpy.CreateFileGDB_management(path,gdbname)
scratchgdbname = "scratch.gdb"
scratchgdb = os.path.join(path,scratchgdbname)
if not arcpy.Exists(scratchgdb):
    arcpy.CreateFileGDB_management(path,scratchgdbname)
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = scratchgdb


# Set Global Variables
arcpy.arcpy.AddWarning(scratchgdb)
arcpy.arcpy.AddWarning(gdb)
clippedServiceLayer = os.path.join(scratchgdb,'clippedServiceLayer')
clippedOtherServiceLayer = os.path.join(scratchgdb,'clippedOtherServiceLayer')
clippedImperviousLayer = os.path.join(scratchgdb,'clippedImperviousLayer')
clippedForestLayer = os.path.join(scratchgdb,'clippedForestLayer')
serviceAreaDissolved = os.path.join(scratchgdb,'serviceAreaDissolved')
serviceAreaImpervious = os.path.join(scratchgdb,'serviceAreaImpervious')
serviceAreaForest = os.path.join(scratchgdb,'serviceAreaForest')
serviceAreaForestImpervious = os.path.join(scratchgdb,'serviceAreaForestImpervious')
finalServiceImpervious = os.path.join(gdb,'finalServiceImpervious')
finalServiceForest = os.path.join(gdb,'finalServiceForest')
finalServicePervious = os.path.join(gdb,'finalServicePervious')
finalServiceLayer = os.path.join(gdb,'finalServiceLayer')
otherServiceDissolved = os.path.join(scratchgdb,'otherServiceDissolved')
otherServiceImpervious = os.path.join(scratchgdb,'otherServiceImpervious')
otherServiceForest = os.path.join(scratchgdb,'otherServiceForest')
otherServiceForestImpervious = os.path.join(scratchgdb,'otherServiceForestImpervious')
finalOtherImpervious = os.path.join(gdb,'finalOtherImpervious')
finalOtherForest = os.path.join(gdb,'finalOtherForest')
finalOtherPervious = os.path.join(gdb,'finalOtherPervious')
finalOtherLayer = os.path.join(gdb,'finalOtherLayer')
finalMainLayer = os.path.join(gdb,'finalMainLayer')
erasedMainImpervious = os.path.join(gdb,'erasedMainImpervious')
erasedMainForest = os.path.join(gdb,'erasedMainForest')
mainForestImpervious = os.path.join(gdb,'mainForestImpervious')



arcpy.AddWarning(identifier)

def intersector(layerOne,layerTwo):
    arcpy.env.overwriteOutput = True
    outLayer = "temp_{0}".format(arcpy.Describe(layerTwo).name)
    arcpy.Intersect_analysis([layerOne,layerTwo],outLayer,"NO_FID","","INPUT")
    arcpy.AddWarning(outLayer)
    return outLayer

def Merger(layer,layerTwo,layerThree):
    arcpy.env.overwriteOutput = True
    mergeLayer = "Temp_{0}".format(arcpy.Describe(layerTwo).name)
    arcpy.Merge_management([layerTwo,layerThree],mergeLayer)
    outLayer = arcpy.Erase_analysis(layer,mergeLayer)
    arcpy.AddWarning(outLayer)
    return outLayer
##
def Calc(layer,fieldname):
    arcpy.env.overwriteOutput = True
##    output = "in_memory" + "\\"+ "Temp_{0}".format(arcpy.Describe(layer).name)
    arcpy.AddField_management(layer, fieldname, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Process: Calculate Field
    arcpy.CalculateField_management(layer, fieldname, "!shape.area@acres!", "PYTHON_9.3", "")
    return layer
##
def Dissolve_Add_Cal(layer,identify,fieldname):
    arcpy.env.overwriteOutput = True
    outPut = output = "Temp_{0}".format(arcpy.Describe(layer).name)
    arcpy.Dissolve_management(layer, outPut, identify,None, "MULTI_PART", "DISSOLVE_LINES")
    # Process: Add Field
    outLayer = Calc(outPut,fieldname)
    arcpy.AddWarning(outLayer)
    return outLayer
##
def Joining(layer,joinfield,*layers):

    outLayer = arcpy.MakeFeatureLayer_management(layer)
    for i in layers:
        arcpy.AddJoin_management(outLayer,joinfield,i,joinfield)
    arcpy.AddWarning(outLayer)
    return outLayer


# clipping by main layer
clippedServiceLayer = intersector(mainLayer,serviceAreaLayer) # clipped service area by main layer
clippedOtherServiceLayer = intersector(mainLayer,otherServiceLayer) # clipped other service area by main layer
clippedImperviousLayer = intersector(mainLayer,imperviousLayer) # clipped impervious layer by main layer
clippedForestLayer = intersector(mainLayer,forestLayer) # clipped forest layer by main layer

# Dissolve service layer
serviceAreaDissolved = Dissolve_Add_Cal(clippedServiceLayer,identifier,"Regulated")
arcpy.AddWarning(serviceAreaDissolved)

# clipping by Service layers
serviceAreaImpervious = intersector(serviceAreaDissolved,clippedImperviousLayer)
arcpy.AddWarning(serviceAreaImpervious)
serviceAreaForest= Intersecter(serviceAreaDissolved,clippedForestLayer)
arcpy.AddWarning(serviceAreaForest)

# Merging forest and impervious layers
serviceAreaForestImpervious = Merger(serviceAreaDissolved,serviceAreaImpervious,serviceAreaForest)

# dissolving impervious, forest and pervious layers
finalServiceImpervious = Dissolve_Add_Cal(serviceAreaImpervious,identifier,"Imper")
finalServiceForest = Dissolve_Add_Cal(serviceAreaForest,identifier,"Forest")
finalServicePervious = Dissolve_Add_Cal(serviceAreaForestImpervious,identifier,"Per")

# joining all service impervious, service forest and service pervious
finalServiceLayer = Joining(serviceAreaDissolved,identifier,finalServiceImpervious,finalServiceForest,finalServicePervious)


# other service area dissolved
otherServiceDissolved = Dissolve_Add_Cal(clippedOtherServiceLayer,identifier,"OtherRegu")
# clipping by other Service dissolved layer
otherServiceImpervious = intersector(otherServiceDissolved,clippedImperviousLayer)
otherServiceForest = intersector(otherServiceDissolved,clippedForestLayer)
# Merging forest and impervious layers
otherServiceForestImpervious = Merger(otherServiceDissolved,otherServiceImpervious,otherServiceForest)
# other service impervious, forest and pervious dissolved
finalOtherImpervious = Dissolve_Add_Cal(otherServiceImpervious,identifier,"OtherImpe")
finalOtherForest = Dissolve_Add_Cal(otherServiceForest,identifier,"OtherForest")
finalOtherPervious = Dissolve_Add_Cal(otherServiceForestImpervious,identifier,"OtherPer")
# Joining other perviou, impervious and impervious to other layer
finalOtherLayer = Joining(otherServiceDissolved,identifier,finalOtherImpervious,finalServiceForest,finalOtherPervious)


#unregulated areas
finalMainLayer = Calc(mainLayer,"Drainage") # add drainage area in main layer
erasedMainImpervious = Merger(imperviousLayer,finalServiceLayer,finalOtherLayer)# needs a little work
erasedMainForest = Merger(forestLayer,finalServiceLayer,finalOtherLayer)# Needs a little work
mainForestImpervious = Merger(mainLayer,erasedMainImpervious,erasedMainForest)

finalMainImpervious = Dissolve_Add_Cal(erasedMainImpervious,identifier,"UnreImp")
finalMainForest = Dissolve_Add_Cal(erasedMainForest,identifier,"UnreFor")
finalMainPervious = Dissolve_Add_Cal(mainForestImpervious,identifier,"UnrePer")

finalMainLayer = Joining(finalMainLayer,identifier,finalMainImpervious,finalMainForest,finalMainPervious)
alltogether = Joining(finalMainLayer,finalServiceLayer,finalOtherLayer)
arcpy.TableToExcel_conversion(alltogether,excelOutput)
