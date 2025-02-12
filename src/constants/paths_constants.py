
###########################################################################
#####                        Table of Contents                        ##### 
###########################################################################



    #####     1. DIR PATHS     #####

          ##  1.1. MAIN
          ##  1.2. OUTPUTS



    #####     2. PARTS OF FILE NAMES AND PATHS     #####

          ##  2.1. NAMES
          ##  2.2. EXTENSIONS
          ##  2.3. SUFFIXES AND PREFIXES



    #####     3. FILE BASE NAMES     #####

          ##  3.1. BASIC
          ##  3.2. BASIC EXTRA
          ##  3.3. BASIC GROUPED
          ##  3.4. OVERVIEW
          ##  3.5. OVERVIEW [BASIC GROUPED]
          ##  3.6. OVERVIEW FOR RESOURCES
          ##  3.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES
          ##  3.8. OVERVIEW RESOURCES BY DAYS
          ##  3.9. OVERVIEW [BASIC GROUPED] RESOURCES BY DAYS
          ##  3.10. OVERVIEW FOR RESOURCES BY HOURS
          ##  3.11. OVERVIEW [BASIC GROUPED] RESOURCES BY HOURS



    #####     4. FILE NAMES     #####

        ###   4.1. Excel   ###

          ##  4.1.1. BASIC
          ##  4.1.2. BASIC EXTRA
          ##  4.1.3. BASIC GROUPED
          ##  4.1.4. OVERVIEW
          ##  4.1.5. OVERVIEW [BASIC GROUPED]
          ##  4.1.6. OVERVIEW FOR RESOURCES
          ##  4.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES
          ##  4.1.8. OVERVIEW FOR RESOURCES BY DAYS
          ##  4.1.9. OVERVIEW [BASIC GROUPED] RESOURCES BY DAYS
          ##  4.1.10. OVERVIEW FOR RESOURCES BY HOURS
          ##  4.1.11. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS


        ###   4.2. JSON   ###

          ##  4.2.1. BASIC MAIN


        ###   4.3 JSON with DataFrames   ###

          ##  4.3.1. BASIC MAIN
          ##  4.3.2. BASIC
          ##  4.3.3. BASIC EXTRA
          ##  4.3.4. BASIC GROUPED



    #####     5. FILE PATHS     #####

       ###    5.1 Excel   ###

          ##  5.1.1. BASIC
          ##  5.1.2. BASIC EXTRA
          ##  5.1.3. BASIC GROUPED
          ##  5.1.4. OVERVIEW
          ##  5.1.5. OVERVIEW [BASIC GROUPED]
          ##  5.1.6. OVERVIEW FOR RESOURCES
          ##  5.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES
          ##  5.1.8. OVERVIEW FOR RESOURCES BY DAYS
          ##  5.1.9. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY DAYS
          ##  5.1.10. OVERVIEW FOR RESOURCES BY HOURS
          ##  5.1.11. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS


        ###   5.2. JSON   ###

          ##  5.2.1 BASIC MAIN


        ###   5.3. JSON with DataFrames   ###

          ##  5.3.1. BASIC MAIN
          ##  5.3.2. BASIC
          ##  5.3.3. BASIC EXTRA
          ##  5.3.4. BASIC GROUPED
          ##  5.3.5. OVERVIEW FOR RESOURCES
          ##  5.3.6. OVERVIEW [BASIC GROUPED] FOR RESOURCES
          ##  5.3.7. OVERVIEW FOR RESOURCES BY DAYS
          ##  5.3.8. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY DAYS
          ##  5.3.9. OVERVIEW FOR RESOURCES BY HOURS
          ##  5.3.10. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS


###########################################################################

import os



#####     1. DIR PATHS     #####

##  1.1 MAIN  ##

currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
projectRoot = os.path.dirname(srcDirPath)



##  1.2. OUTPUTS  ##

documentsPath = os.path.join(projectRoot, 'documents')

documentsGroupedPath = os.path.join(documentsPath, 'grouped')
documentsOverviewsPath = os.path.join(documentsPath, 'overviews')
documentsOverviewsGroupedPath = os.path.join(documentsOverviewsPath, 'grouped')

documentsPrototypesPath = os.path.join(documentsPath, 'prototypes')


processingFilesPath = os.path.join(projectRoot, 'processing_files')

processingFilesJSONPath = os.path.join(processingFilesPath, 'json')
processingFilesJSONGroupedPath = os.path.join(processingFilesJSONPath, 'grouped')
processingFilesJSONOverviewsPath = os.path.join(processingFilesJSONPath, 'overviews')
processingFilesJSONOverviewsGroupedPath = os.path.join(processingFilesJSONOverviewsPath, 'grouped')

processingFilesExcelPath = os.path.join(processingFilesPath, 'excel')


logsPath = os.path.join(projectRoot, 'logs')
schedulesPath = os.path.join(projectRoot, 'schedules')



#####     2. PARTS OF FILE NAMES AND PATHS     #####

##  2.1. EXTENSIONS  ##
extExcel = '.xlsx'
extJSON = '.json'



##  2.2 NAMES  ##

scheduleName = 'schedule'
schedulesName = 'schedules'

classesName = 'classes'
teachersName = 'teachers'
classroomsName = 'classrooms'
subjectsName = 'subjects'

allOwnerTypeNames = [ classesName,
                      teachersName,
                      classroomsName,
                      subjectsName ] 



##  2.3 SUFFIXES AND PREFIXES  ##
dfsPrefix = 'dfs_'
multiDfsPrefix = 'multi-dfs_'
schedulePrefixMain = scheduleName + '_'
schedulePartOfPrefix = scheduleName + '-'
groupedSuffix = '-grouped'
overviewSuffix = '_overview'
resourcesSuffix = '_resources'
byHoursSuffix = '-by-hours'
byDaysSuffix = '-by-days'
wideSuffix = '_wide'
verticallySuffix = '_vertically'
brieflySuffix = '_briefly'



#####     3. FILE BASE NAMES     #####

##  3.0. TEST  ##
testBaseName = 'test'



##  3.1. BASIC  ##

# For all the schedules
schedulesBaseName = schedulesName

# For the classes
scheduleClassesBaseName = schedulePrefixMain + classesName
# For the teachers
scheduleTeachersBaseName = schedulePrefixMain + teachersName
# For the classrooms
scheduleClassroomsBaseName = schedulePrefixMain + classroomsName
# For the subjects
scheduleSubjectsBaseName = schedulePrefixMain + subjectsName

# For all of the above
allScheduleBaseNames = [ scheduleClassesBaseName,
                         scheduleTeachersBaseName,
                         scheduleClassroomsBaseName,
                         scheduleSubjectsBaseName ]



##  3.2. BASIC EXTRA  ##

# For all the schedules wide and vertically
schedulesWideAndVerticallyBaseName = schedulesBaseName + wideSuffix + verticallySuffix
# For the classrooms wide and vertically
scheduleClassroomsWideAndVerticallyBaseName = scheduleClassroomsBaseName + wideSuffix + verticallySuffix
# For the classrooms briefly wide and vertically
scheduleClassroomsBrieflyWideAndVerticallyBaseName = scheduleClassroomsBaseName + brieflySuffix + wideSuffix + verticallySuffix

# For the classes vertically
scheduleClassesVerticallyBaseName = scheduleClassesBaseName + verticallySuffix

# For the classrooms grouped overview for the resources vertically
scheduleClassroomsGroupedOverviewResourcesVerticallyBaseName  = scheduleClassroomsBaseName + overviewSuffix + resourcesSuffix + verticallySuffix + extExcel



##  3.3. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedBaseName = scheduleClassesBaseName + groupedSuffix
# For the teachers grouped
scheduleTeachersGroupedBaseName = scheduleTeachersBaseName + groupedSuffix
# For the classrooms grouped
scheduleClassroomsGroupedBaseName = scheduleClassroomsBaseName + groupedSuffix
# For the subjects grouped
scheduleSubjectsGroupedBaseName = scheduleSubjectsBaseName + groupedSuffix

# For all of the above
allScheduleGroupedBaseNames = [ scheduleClassesGroupedBaseName,
                                scheduleTeachersGroupedBaseName,
                                scheduleClassroomsGroupedBaseName,
                                scheduleSubjectsGroupedBaseName ]



##  3.4. OVERVIEW  ##

# For the classes overview
scheduleClassesOverviewBaseName = scheduleClassesBaseName + overviewSuffix
# For the teachers overview
scheduleTeachersOverviewBaseName = scheduleTeachersBaseName + overviewSuffix
# For the classrooms overview
scheduleClassroomsOverviewBaseName = scheduleClassroomsBaseName + overviewSuffix
# For the subjects overview
scheduleSubjectsOverviewBaseName = scheduleSubjectsBaseName +  overviewSuffix

# For all of the above
allScheduleGroupedOverviewBaseNames = [ scheduleClassesOverviewBaseName,
                                        scheduleTeachersOverviewBaseName,
                                        scheduleClassroomsOverviewBaseName,
                                        scheduleSubjectsOverviewBaseName ]



##  3.5. OVERVIEW [BASIC GROUPED]  ##

# For the classes grouped overview
scheduleClassesGroupedOverviewBaseName = scheduleClassesGroupedBaseName + overviewSuffix
# For the teachers grouped overview
scheduleTeachersGroupedOverviewBaseName = scheduleTeachersGroupedBaseName + overviewSuffix
# For the classrooms grouped overview
scheduleClassroomsGroupedOverviewBaseName = scheduleClassroomsGroupedBaseName + overviewSuffix
# For the subjects grouped overview
scheduleSubjectsGroupedOverviewBaseName = scheduleSubjectsGroupedBaseName + overviewSuffix

# For all of the above
allScheduleGroupedOverviewBaseNames = [ scheduleClassesGroupedOverviewBaseName,
                                        scheduleTeachersGroupedOverviewBaseName,
                                        scheduleClassroomsGroupedOverviewBaseName,
                                        scheduleSubjectsGroupedOverviewBaseName ]



##  3.6. OVERVIEW FOR RESOURCES  ##

# For the classes overview for the resources
scheduleClassesOverviewResourcesBaseName = scheduleClassesOverviewBaseName + resourcesSuffix
# For the teachers overview for the resources
scheduleTeachersOverviewResourcesBaseName = scheduleTeachersOverviewBaseName + resourcesSuffix
# For the classrooms overview for the resources
scheduleClassroomsOverviewResourcesBaseName = scheduleClassroomsOverviewBaseName + resourcesSuffix
# For the subjects overview for the resources
scheduleSubjectsOverviewResourcesBaseName = scheduleSubjectsOverviewBaseName + resourcesSuffix

# For all of the above
allScheduleOverviewResourcesBaseNames = [ scheduleClassesOverviewResourcesBaseName,
                                          scheduleTeachersOverviewResourcesBaseName,
                                          scheduleClassroomsOverviewResourcesBaseName,
                                          scheduleSubjectsOverviewResourcesBaseName ]



##  3.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedOverviewResourcesBaseName = scheduleClassesGroupedOverviewBaseName + resourcesSuffix
# For the teachers grouped overview for the resources
scheduleTeachersGroupedOverviewResourcesBaseName = scheduleTeachersGroupedOverviewBaseName + resourcesSuffix
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedOverviewResourcesBaseName = scheduleClassroomsGroupedOverviewBaseName + resourcesSuffix
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedOverviewResourcesBaseName = scheduleSubjectsGroupedOverviewBaseName + resourcesSuffix

# For all of the above
allScheduleGroupedOverviewResourcesBaseNames = [ scheduleClassesGroupedOverviewResourcesBaseName,
                                                 scheduleTeachersGroupedOverviewResourcesBaseName,
                                                 scheduleClassroomsGroupedOverviewResourcesBaseName,
                                                 scheduleSubjectsGroupedOverviewResourcesBaseName ]



##  3.8. OVERVIEW BY DAYS  ##

# For the classes overview for the resources grouped by days
scheduleClassesOverviewResourcesByDaysBaseName = scheduleClassesOverviewResourcesBaseName + byDaysSuffix
# For the teachers overview for the resources grouped by days
scheduleTeachersOverviewResourcesByDaysBaseName = scheduleTeachersOverviewResourcesBaseName + byDaysSuffix
# For the classrooms overview for the resources grouped by days
scheduleClassroomsOverviewResourcesByDaysBaseName = scheduleClassroomsOverviewResourcesBaseName + byDaysSuffix
# For the subjects overview for the resources grouped by days
scheduleSubjectsOverviewResourcesByDaysBaseName = scheduleSubjectsOverviewResourcesBaseName + byDaysSuffix

# For all of the above
allScheduleOverviewResourcesByDaysBaseNames = [ scheduleClassesOverviewResourcesByDaysBaseName,
                                                scheduleTeachersOverviewResourcesByDaysBaseName,
                                                scheduleClassroomsOverviewResourcesByDaysBaseName,
                                                scheduleSubjectsOverviewResourcesByDaysBaseName ]



##  3.9. OVERVIEW [BASIC GROUPED] BY DAYS  ##

# For the classes grouped overview for the resources grouped by days
scheduleClassesGroupedOverviewResourcesByDaysBaseName = scheduleClassesGroupedOverviewResourcesBaseName + byDaysSuffix
# For the teachers grouped overview for the resources grouped by days
scheduleTeachersGroupedOverviewResourcesByDaysBaseName = scheduleTeachersGroupedOverviewResourcesBaseName + byDaysSuffix
# For the classrooms grouped overview for the resources grouped by days
scheduleClassroomsGroupedOverviewResourcesByDaysBaseName = scheduleClassroomsGroupedOverviewResourcesBaseName + byDaysSuffix
# For the subjects grouped overview for the resources grouped by days
scheduleSubjectsGroupedOverviewResourcesByDaysBaseName = scheduleSubjectsGroupedOverviewResourcesBaseName + byDaysSuffix

# For all of the above
allScheduleGroupedOverviewResourcesByDaysBaseNames = [ scheduleClassesGroupedOverviewResourcesByDaysBaseName,
                                                       scheduleTeachersGroupedOverviewResourcesByDaysBaseName,
                                                       scheduleClassroomsGroupedOverviewResourcesByDaysBaseName,
                                                       scheduleSubjectsGroupedOverviewResourcesByDaysBaseName ]



##  3.10. OVERVIEW BY HOURS  ##

# For the classes overview for the resources grouped by hours
scheduleClassesOverviewResourcesByHoursBaseName = scheduleClassesOverviewResourcesBaseName + byHoursSuffix
# For the teachers overview for the resources grouped by hours
scheduleTeachersOverviewResourcesByHoursBaseName = scheduleTeachersOverviewResourcesBaseName + byHoursSuffix
# For the classrooms overview for the resources grouped by hours
scheduleClassroomsOverviewResourcesByHoursBaseName = scheduleClassroomsOverviewResourcesBaseName + byHoursSuffix
# For the subjects overview for the resources grouped by hours
scheduleSubjectsOverviewResourcesByHoursBaseName = scheduleSubjectsOverviewResourcesBaseName + byHoursSuffix

# For all of the above
allScheduleOverviewResourcesByHoursBaseNames = [ scheduleClassesOverviewResourcesByHoursBaseName,
                                                 scheduleTeachersOverviewResourcesByHoursBaseName,
                                                 scheduleClassroomsOverviewResourcesByHoursBaseName,
                                                 scheduleSubjectsOverviewResourcesByHoursBaseName ]



##  3.11. OVERVIEW [BASIC GROUPED] BY HOURS  ##

# For the classes grouped overview for the resources grouped by hours
scheduleClassesGroupedOverviewResourcesByHoursBaseName = scheduleClassesGroupedOverviewResourcesBaseName + byHoursSuffix
# For the teachers grouped overview for the resources grouped by hours
scheduleTeachersGroupedOverviewResourcesByHoursBaseName = scheduleTeachersGroupedOverviewResourcesBaseName + byHoursSuffix
# For the classrooms grouped overview for the resources grouped by hours
scheduleClassroomsGroupedOverviewResourcesByHoursBaseName = scheduleClassroomsGroupedOverviewResourcesBaseName + byHoursSuffix
# For the subjects grouped overview for the resources grouped by hours
scheduleSubjectsGroupedOverviewResourcesByHoursBaseName = scheduleSubjectsGroupedOverviewResourcesBaseName + byHoursSuffix

# For all of the above
allScheduleGroupedOverviewResourcesByHoursBaseNames = [ scheduleClassesGroupedOverviewResourcesByHoursBaseName,
                                                        scheduleTeachersGroupedOverviewResourcesByHoursBaseName,
                                                        scheduleClassroomsGroupedOverviewResourcesByHoursBaseName,
                                                        scheduleSubjectsGroupedOverviewResourcesByHoursBaseName ]



#####     4. FILE NAMES     #####


###   4.1. Excel   ###

##  4.1.0. TEST  ##
testExcelName = testBaseName + extExcel



##  4.1.1. BASIC  ##

# For the classes
scheduleClassesExcelName = scheduleClassesBaseName + extExcel
# For the teachers
scheduleTeachersExcelName = scheduleTeachersBaseName + extExcel
# For the classrooms
scheduleClassroomsExcelName = scheduleClassroomsBaseName + extExcel
# For the subjects
scheduleSubjectsExcelName = scheduleSubjectsBaseName + extExcel

# For all of the above
allScheduleExcelNames = [ scheduleClassesExcelName,
                          scheduleTeachersExcelName,
                          scheduleClassroomsExcelName,
                          scheduleSubjectsExcelName ]



##  4.1.2. BASIC EXTRA  ##

# For all the schedules wide and vertically
schedulesWideAndVerticallyExcelName = schedulesWideAndVerticallyBaseName + extExcel
# For the classrooms wide and vertically
scheduleClassroomsWideAndVerticallyExcelName = scheduleClassroomsWideAndVerticallyBaseName + extExcel

# For the classrooms briefly wide and vertically
scheduleClassroomsBrieflyWideAndVerticallyExcelName = scheduleClassroomsBrieflyWideAndVerticallyBaseName + extExcel

# For the classes vertically
scheduleClassesVerticallyExcelName = scheduleClassesVerticallyBaseName + extExcel

# For the classrooms grouped overview for the resources vertically
scheduleClassroomsGroupedOverviewResourcesVerticallyExcelName  = scheduleClassroomsGroupedOverviewResourcesVerticallyBaseName + extExcel

# For the lists of schedule owners
scheduleListsOwnersGroupedExcelName = schedulePartOfPrefix + 'lists_owners' + groupedSuffix + extExcel



##  4.1.3. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedExcelName = scheduleClassesGroupedBaseName + extExcel
# For the teachers grouped
scheduleTeachersGroupedExcelName = scheduleTeachersGroupedBaseName + extExcel
# For the classrooms grouped
scheduleClassroomsGroupedExcelName = scheduleClassroomsGroupedBaseName + extExcel
# For the subjects grouped
scheduleSubjectsGroupedExcelName = scheduleSubjectsGroupedBaseName + extExcel

# For all of the above
allScheduleGroupedExcelNames = [ scheduleClassesGroupedExcelName,
                                 scheduleTeachersGroupedExcelName,
                                 scheduleClassroomsGroupedExcelName,
                                 scheduleSubjectsGroupedExcelName ]



##  4.1.4. OVERVIEW  ##

# For the classes overview
scheduleClassesOverviewExcelName = scheduleClassesOverviewBaseName + extExcel
# For the teachers overview
scheduleTeachersOverviewExcelName = scheduleTeachersOverviewBaseName + extExcel
# For the classrooms overview
scheduleClassroomsOverviewExcelName = scheduleClassroomsOverviewBaseName + extExcel
# For the subjects overview
scheduleSubjectsOverviewExcelName = scheduleSubjectsOverviewBaseName + extExcel

# For all of the above
allScheduleOverviewExcelNames = [ scheduleClassesOverviewExcelName,
                                  scheduleTeachersOverviewExcelName,
                                  scheduleClassroomsOverviewExcelName,
                                  scheduleSubjectsOverviewExcelName ]



##  4.1.5. OVERVIEW [BASIC GROUPED]  ##

# For the classes grouped overview
scheduleClassesGroupedOverviewExcelName = scheduleClassesGroupedOverviewBaseName + extExcel
# For the teachers grouped overview
scheduleTeachersGroupedOverviewExcelName = scheduleTeachersGroupedOverviewBaseName + extExcel
# For the classrooms grouped overview
scheduleClassroomsGroupedOverviewExcelName = scheduleClassroomsGroupedOverviewBaseName + extExcel
# For the subjects grouped overview
scheduleSubjectsGroupedOverviewExcelName = scheduleSubjectsGroupedOverviewBaseName + extExcel

# For all of the above
allScheduleGroupedOverviewExcelNames = [ scheduleClassesGroupedOverviewExcelName,
                                         scheduleTeachersGroupedOverviewExcelName,
                                         scheduleClassroomsGroupedOverviewExcelName,
                                         scheduleSubjectsGroupedOverviewExcelName ]



##  4.1.6. OVERVIEW FOR RESOURCES  ##

# For the classes overview for the resources
scheduleClassesOverviewResourcesExcelName = scheduleClassesOverviewResourcesBaseName + extExcel
# For the teachers overview for the resources
scheduleTeachersOverviewResourcesExcelName = scheduleTeachersOverviewResourcesBaseName + extExcel
# For the classrooms overview for the resources
scheduleClassroomsOverviewResourcesExcelName = scheduleClassroomsOverviewResourcesBaseName + extExcel
# For the subjects overview for the resources
scheduleSubjectsOverviewResourcesExcelName = scheduleSubjectsOverviewResourcesBaseName + extExcel

# For all of the above
allScheduleOverviewResourcesExcelNames = [ scheduleClassesOverviewResourcesExcelName,
                                           scheduleTeachersOverviewResourcesExcelName,
                                           scheduleClassroomsOverviewResourcesExcelName,
                                           scheduleSubjectsOverviewResourcesExcelName ]



##  4.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedOverviewResourcesExcelName = scheduleClassesGroupedOverviewResourcesBaseName + extExcel
# For the teachers grouped overview for the resources
scheduleTeachersGroupedOverviewResourcesExcelName = scheduleTeachersGroupedOverviewResourcesBaseName + extExcel
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedOverviewResourcesExcelName = scheduleClassroomsGroupedOverviewResourcesBaseName + extExcel
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedOverviewResourcesExcelName = scheduleSubjectsGroupedOverviewResourcesBaseName + extExcel

# For all of the above
allScheduleGroupedOverviewResourcesExcelNames = [ scheduleClassesGroupedOverviewResourcesExcelName,
                                                  scheduleTeachersGroupedOverviewResourcesExcelName,
                                                  scheduleClassroomsGroupedOverviewResourcesExcelName,
                                                  scheduleSubjectsGroupedOverviewResourcesExcelName ]



##  4.1.8. OVERVIEW FOR RESOURCES BY DAYS  ##

# For the classes overview for the resources grouped by days
scheduleClassesOverviewResourcesByDaysExcelName = scheduleClassesOverviewResourcesByDaysBaseName + extExcel
# For the teachers overview for the resources grouped by days
scheduleTeachersOverviewResourcesByDaysExcelName = scheduleTeachersOverviewResourcesByDaysBaseName + extExcel
# For the classrooms overview for the resources grouped by days
scheduleClassroomsOverviewResourcesByDaysExcelName = scheduleClassroomsOverviewResourcesByDaysBaseName + extExcel
# For the subjects overview for the resources grouped by days
scheduleSubjectsOverviewResourcesByDaysExcelName = scheduleSubjectsOverviewResourcesByDaysBaseName + extExcel

# For all of the above
allScheduleOverviewResourcesByDaysExcelNames = [ scheduleClassesOverviewResourcesByDaysExcelName,
                                                 scheduleTeachersOverviewResourcesByDaysExcelName,
                                                 scheduleClassroomsOverviewResourcesByDaysExcelName,
                                                 scheduleSubjectsOverviewResourcesByDaysExcelName ]



##  4.1.9. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY DAYS  ##

# For the classes grouped overview for the resources grouped by days
scheduleClassesGroupedOverviewResourcesByDaysExcelName = scheduleClassesGroupedOverviewResourcesByDaysBaseName + extExcel
# For the teachers grouped overview for the resources grouped by days
scheduleTeachersGroupedOverviewResourcesByDaysExcelName = scheduleTeachersGroupedOverviewResourcesByDaysBaseName + extExcel
# For the classrooms grouped overview for the resources grouped by days
scheduleClassroomsGroupedOverviewResourcesByDaysExcelName = scheduleClassroomsGroupedOverviewResourcesByDaysBaseName + extExcel
# For the subjects grouped overview for the resources grouped by days
scheduleSubjectsGroupedOverviewResourcesByDaysExcelName = scheduleSubjectsGroupedOverviewResourcesByDaysBaseName + extExcel

# For all of the above
allScheduleGroupedOverviewResourcesByDaysExcelNames = [ scheduleClassesGroupedOverviewResourcesByDaysExcelName,
                                                        scheduleTeachersGroupedOverviewResourcesByDaysExcelName,
                                                        scheduleClassroomsGroupedOverviewResourcesByDaysExcelName,
                                                        scheduleSubjectsGroupedOverviewResourcesByDaysExcelName ]



##  4.1.10. OVERVIEW FOR RESOURCES BY HOURS ##

# For the classes overview for the resources grouped by hours
scheduleClassesOverviewResourcesByHoursExcelName = scheduleClassesOverviewResourcesByHoursBaseName + extExcel
# For the teachers overview for the resources grouped by hours
scheduleTeachersOverviewResourcesByHoursExcelName = scheduleTeachersOverviewResourcesByHoursBaseName + extExcel
# For the classrooms overview for the resources grouped by hours
scheduleClassroomsOverviewResourcesByHoursExcelName = scheduleClassroomsOverviewResourcesByHoursBaseName + extExcel
# For the subjects overview for the resources grouped by hours
scheduleSubjectsOverviewResourcesByHoursExcelName = scheduleSubjectsOverviewResourcesByHoursBaseName + extExcel

# For all of the above
allScheduleOverviewResourcesByHoursExcelNames = [ scheduleClassesOverviewResourcesByHoursExcelName,
                                                  scheduleTeachersOverviewResourcesByHoursExcelName,
                                                  scheduleClassroomsOverviewResourcesByHoursExcelName,
                                                  scheduleSubjectsOverviewResourcesByHoursExcelName ]



##  4.1.11. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS  ##

# For the classes grouped overview for the resources grouped by hours
scheduleClassesGroupedOverviewResourcesByHoursExcelName = scheduleClassesGroupedOverviewResourcesByHoursBaseName + extExcel
# For the teachers grouped overview for the resources grouped by hours
scheduleTeachersGroupedOverviewResourcesByHoursExcelName = scheduleTeachersGroupedOverviewResourcesByHoursBaseName + extExcel
# For the classrooms grouped overview for the resources grouped by hours
scheduleClassroomsGroupedOverviewResourcesByHoursExcelName = scheduleClassroomsGroupedOverviewResourcesByHoursBaseName + extExcel
# For the subjects grouped overview for the resources grouped by hours
scheduleSubjectsGroupedOverviewResourcesByHoursExcelName = scheduleSubjectsGroupedOverviewResourcesByHoursBaseName + extExcel

# For all of the above
allScheduleGroupedOverviewResourcesByHoursExcelNames = [ scheduleClassesGroupedOverviewResourcesByHoursExcelName,
                                                         scheduleTeachersGroupedOverviewResourcesByHoursExcelName,
                                                         scheduleClassroomsGroupedOverviewResourcesByHoursExcelName,
                                                         scheduleSubjectsGroupedOverviewResourcesByHoursExcelName ]



###   4.2. JSON   ###

##  4.2.0 TEST  ##

testJSONName = testBaseName + extJSON



##  4.2.1. BASIC MAIN  ##

# For the scraped classes data, base for other files
scheduleClassesBaseJSONName = 'base_' + scheduleClassesBaseName + extJSON



###   4.3 JSON with DataFrames   ###

##  4.3.1. BASIC MAIN  ##

# For the classes read from Excel
scheduleClassesExcelDfsJSONName = dfsPrefix + schedulePartOfPrefix + 'excel_classes' + extJSON



##  4.3.2. BASIC  ##

# For the classes
scheduleClassesDfsJSONName = dfsPrefix + scheduleClassesBaseName + extJSON
# For the teachers
scheduleTeachersDfsJSONName = dfsPrefix + scheduleTeachersBaseName + extJSON
# For the classrooms
scheduleClassroomsDfsJSONName = dfsPrefix + scheduleClassroomsBaseName + extJSON
# For the subjects
scheduleSubjectsDfsJSONName = dfsPrefix + scheduleSubjectsBaseName + extJSON

# For all of the above
allScheduleDfsJSONNames = [ scheduleClassesDfsJSONName,
                            scheduleTeachersDfsJSONName,
                            scheduleClassroomsDfsJSONName,
                            scheduleSubjectsDfsJSONName ]



##  4.3.3. BASIC EXTRA  ##

# For the list of the schedule owners
scheduleListsOwnersGroupedDfsJSONName = dfsPrefix + schedulePartOfPrefix + 'lists_owners' + groupedSuffix + extJSON

# For all the schedules wide and vertically
schedulesWideAndVerticallyDfsJSONName = dfsPrefix + schedulesWideAndVerticallyBaseName + extJSON
# For the classrooms wide and vertically
scheduleClassroomsWideAndVerticallyDfsJSONName = dfsPrefix + scheduleClassroomsWideAndVerticallyBaseName + extJSON

# For the classrooms briefly wide and vertically
scheduleClassroomsBrieflyWideAndVerticallyDfsJSONName = dfsPrefix + scheduleClassroomsBrieflyWideAndVerticallyBaseName + extJSON



##  4.3.4. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedDfsJSONName = dfsPrefix + scheduleClassesGroupedBaseName + extJSON
# For the teachers grouped
scheduleTeachersGroupedDfsJSONName = dfsPrefix + scheduleTeachersGroupedBaseName + extJSON
# For the classrooms grouped
scheduleClassroomsGroupedDfsJSONName = dfsPrefix + scheduleClassroomsGroupedBaseName + extJSON
# For the subjects grouped
scheduleSubjectsGroupedDfsJSONName = dfsPrefix + scheduleSubjectsGroupedBaseName + extJSON

# For all of the above
allScheduleGroupedDfsJSONNames = [ scheduleClassesGroupedDfsJSONName,
                                   scheduleTeachersGroupedDfsJSONName,
                                   scheduleClassroomsGroupedDfsJSONName,
                                   scheduleSubjectsGroupedDfsJSONName ]



##  4.3.5. OVERVIEW FOR RESOURCES  ##

# For the classes overview for the resources
scheduleClassesOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleClassesOverviewResourcesBaseName + extJSON
# For the teachers overview for the resources
scheduleTeachersOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleTeachersOverviewResourcesBaseName + extJSON
# For the classrooms overview for the resources
scheduleClassroomsOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleClassroomsOverviewResourcesBaseName + extJSON
# For the subjects overview for the resources
scheduleSubjectsOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleSubjectsOverviewResourcesBaseName + extJSON

# For all of the above
allScheduleOverviewResourcesDfsJSONNames = [ scheduleClassesOverviewResourcesDfsJSONName,
                                             scheduleTeachersOverviewResourcesDfsJSONName,
                                             scheduleClassroomsOverviewResourcesDfsJSONName,
                                             scheduleSubjectsOverviewResourcesDfsJSONName ]



##  4.3.6. OVERVIEW [BASIC GROUPED] FOR RESOURCES  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleClassesGroupedOverviewResourcesBaseName + extJSON
# For the teachers grouped overview for the resources
scheduleTeachersGroupedOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleTeachersGroupedOverviewResourcesBaseName + extJSON
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedOverviewResourcesBaseName + extJSON
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedOverviewResourcesDfsJSONName = multiDfsPrefix + scheduleSubjectsGroupedOverviewResourcesBaseName + extJSON

# For all of the above
allScheduleGroupedOverviewResourcesDfsJSONNames = [ scheduleClassesGroupedOverviewResourcesDfsJSONName,
                                                    scheduleTeachersGroupedOverviewResourcesDfsJSONName,
                                                    scheduleClassroomsGroupedOverviewResourcesDfsJSONName,
                                                    scheduleSubjectsGroupedOverviewResourcesDfsJSONName ]



##  4.3.7. OVERVIEW FOR RESOURCES BY DAYS  ##

# For the classes overview for the resources grouped by days
scheduleClassesOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleClassesOverviewResourcesByDaysBaseName + extJSON
# For the teachers overview for the resources grouped by days
scheduleTeachersOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleTeachersOverviewResourcesByDaysBaseName + extJSON
# For the classrooms overview for the resources grouped by days
scheduleClassroomsOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleClassroomsOverviewResourcesByDaysBaseName + extJSON
# For the subjects overview for the resources grouped by days
scheduleSubjectsOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleSubjectsOverviewResourcesByDaysBaseName + extJSON

# For all of the above
allScheduleOverviewResourcesByDaysDfsJSONNames = [ scheduleClassesOverviewResourcesByDaysDfsJSONName,
                                                   scheduleTeachersOverviewResourcesByDaysDfsJSONName,
                                                   scheduleClassroomsOverviewResourcesByDaysDfsJSONName,
                                                   scheduleSubjectsOverviewResourcesByDaysDfsJSONName ]



##  4.3.8. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY DAYS  ##

# For the classes grouped overview for the resources grouped by days
scheduleClassesGroupedOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleClassesGroupedOverviewResourcesByDaysBaseName + extJSON
# For the teachers grouped overview for the resources grouped by days
scheduleTeachersGroupedOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleTeachersGroupedOverviewResourcesByDaysBaseName + extJSON
# For the classrooms grouped overview for the resources grouped by days
scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedOverviewResourcesByDaysBaseName + extJSON
# For the subjects grouped overview for the resources grouped by days
scheduleSubjectsGroupedOverviewResourcesByDaysDfsJSONName = multiDfsPrefix + scheduleSubjectsGroupedOverviewResourcesByDaysBaseName + extJSON

# For all of the above
allScheduleGroupedOverviewResourcesByDaysDfsJSONNames = [ scheduleClassesGroupedOverviewResourcesByDaysDfsJSONName,
                                                          scheduleTeachersGroupedOverviewResourcesByDaysDfsJSONName,
                                                          scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONName,
                                                          scheduleSubjectsGroupedOverviewResourcesByDaysDfsJSONName ]


##  4.3.9. OVERVIEW FOR RESOURCES BY HOURS  ##

# For the classes overview for the resources grouped by hours
scheduleClassesOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleClassesOverviewResourcesByHoursBaseName + extJSON
# For the teachers overview for the resources grouped by hours
scheduleTeachersOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleTeachersOverviewResourcesByHoursBaseName + extJSON
# For the classrooms overview for the resources grouped by hours
scheduleClassroomsOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleClassroomsOverviewResourcesByHoursBaseName + extJSON
# For the subjects overview for the resources grouped by hours
scheduleSubjectsOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleSubjectsOverviewResourcesByHoursBaseName + extJSON

# For all of the above
allScheduleOverviewResourcesByHoursDfsJSONNames = [ scheduleClassesOverviewResourcesByHoursDfsJSONName,
                                                    scheduleTeachersOverviewResourcesByHoursDfsJSONName,
                                                    scheduleClassroomsOverviewResourcesByHoursDfsJSONName,
                                                    scheduleSubjectsOverviewResourcesByHoursDfsJSONName ]



##  4.3.10. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS  ##

# For the classes grouped overview for the resources grouped by hours
scheduleClassesGroupedOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleClassesGroupedOverviewResourcesByHoursBaseName + extJSON
# For the teachers grouped overview for the resources grouped by hours
scheduleTeachersGroupedOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleTeachersGroupedOverviewResourcesByHoursBaseName + extJSON
# For the classrooms grouped overview for the resources grouped by hours
scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedOverviewResourcesByHoursBaseName + extJSON
# For the subjects grouped overview for the resources grouped by hours
scheduleSubjectsGroupedOverviewResourcesByHoursDfsJSONName = multiDfsPrefix + scheduleSubjectsGroupedOverviewResourcesByHoursBaseName + extJSON

# For all of the above
allScheduleGroupedOverviewResourcesByHoursDfsJSONNames = [ scheduleClassesGroupedOverviewResourcesByHoursDfsJSONName,
                                                           scheduleTeachersGroupedOverviewResourcesByHoursDfsJSONName,
                                                           scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONName,
                                                           scheduleSubjectsGroupedOverviewResourcesByHoursDfsJSONName ]



#####     5. FILE PATHS     #####


###    5.1 Excel   ###

##  5.1.0 TEST  ##
testExcelPath = os.path.join(processingFilesExcelPath, testExcelName)



##  5.1.1. BASIC  ##

# For the classes
scheduleClassesExcelPath = os.path.join(documentsPath, scheduleClassesExcelName)
# For the teachers
scheduleTeachersExcelPath =  os.path.join(documentsPath, scheduleTeachersExcelName)
# For the classrooms
scheduleClassroomsExcelPath =  os.path.join(documentsPath, scheduleClassroomsExcelName)
# For the subjects
scheduleSubjectsExcelPath =  os.path.join(documentsPath, scheduleSubjectsExcelName)

# For all of the above
allScheduleExcelPaths = [ scheduleClassesExcelPath,
                          scheduleTeachersExcelPath,
                          scheduleClassroomsExcelPath,
                          scheduleSubjectsExcelPath ]



##  5.1.2. BASIC EXTRA  ##

# For all the schedules wide and vertically
schedulesWideAndVerticallyExcelPath = os.path.join(documentsPath, schedulesWideAndVerticallyExcelName)
# For the classrooms wide and vertically
scheduleClassroomsWideAndVerticallyExcelPath = os.path.join(documentsPath, scheduleClassroomsWideAndVerticallyExcelName)

# For the classrooms briefly wide and vertically
scheduleClassroomsBrieflyWideAndVerticallyExcelPath = os.path.join(documentsPath, scheduleClassroomsBrieflyWideAndVerticallyExcelName)

# For the classes vertically
scheduleClassesVerticallyExcelPath = os.path.join(documentsPrototypesPath, scheduleClassesVerticallyExcelName)

# For the classrooms grouped overview for the resources vertically
scheduleClassroomsGroupedOverviewResourcesVerticallyExcelPath =  os.path.join(documentsPrototypesPath, scheduleClassroomsGroupedOverviewResourcesVerticallyExcelName)


# For schedule lists with grouped owners
scheduleListsOwnersGroupedExcelPath =  os.path.join(processingFilesExcelPath, scheduleListsOwnersGroupedExcelName)



##  5.1.3. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedExcelPath =  os.path.join(documentsGroupedPath, scheduleClassesGroupedExcelName)
# For the teachers grouped
scheduleTeachersGroupedExcelPath =  os.path.join(documentsGroupedPath, scheduleTeachersGroupedExcelName)
# For the classrooms grouped
scheduleClassroomsGroupedExcelPath =  os.path.join(documentsGroupedPath, scheduleClassroomsGroupedExcelName)
# For the subjects grouped
scheduleSubjectsGroupedExcelPath =  os.path.join(documentsGroupedPath, scheduleSubjectsGroupedExcelName)

# For all of the above
allScheduleGroupedExcelPaths = [ scheduleClassesGroupedExcelPath,
                                 scheduleTeachersGroupedExcelPath,
                                 scheduleClassroomsGroupedExcelPath,
                                 scheduleSubjectsGroupedExcelPath ]



##  5.1.4. OVERVIEW  ##

# For the classes overview
scheduleClassesOverviewExcelPath = os.path.join(documentsOverviewsPath, scheduleClassesOverviewExcelName)
# For the teachers overview
scheduleTeachersOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersOverviewExcelName)
# For the classrooms overview
scheduleClassroomsOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsOverviewExcelName)
# For the subjects overview
scheduleSubjectsOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsOverviewExcelName)

# For all of the above
allScheduleOverviewExcelPaths = [ scheduleClassesOverviewExcelPath,
                                  scheduleTeachersOverviewExcelPath,
                                  scheduleClassroomsOverviewExcelPath,
                                  scheduleSubjectsOverviewExcelPath ]



##  5.1.5. OVERVIEW [BASIC GROUPED]  ##

# For the classes grouped overview
scheduleClassesGroupedOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesGroupedOverviewExcelName)
# For the teachers grouped overview
scheduleTeachersGroupedOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersGroupedOverviewExcelName)
# For the classrooms grouped overview
scheduleClassroomsGroupedOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsGroupedOverviewExcelName)
# For the subjects grouped overview
scheduleSubjectsGroupedOverviewExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsGroupedOverviewExcelName)

# For all of the above
allScheduleGroupedOverviewExcelPaths = [ #scheduleClassesGroupedOverviewExcelPath,
                                         scheduleTeachersGroupedOverviewExcelPath,
                                         scheduleClassroomsGroupedOverviewExcelPath,
                                         scheduleSubjectsGroupedOverviewExcelPath ]



##  5.1.6. OVERVIEW FOR RESOURCES  ##

# For the classes overview for the resources
scheduleClassesOverviewResourcesExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesOverviewResourcesExcelName)
# For the teachers overview for the resources
scheduleTeachersOverviewResourcesExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersOverviewResourcesExcelName)
# For the classrooms overview for the resources
scheduleClassroomsOverviewResourcesExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsOverviewResourcesExcelName)
# For the subjects overview for the resources
scheduleSubjectsOverviewResourcesExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsOverviewResourcesExcelName)

# For all of the above
allScheduleOverviewResourcesExcelPaths = [ scheduleClassesOverviewResourcesExcelPath,
                                           scheduleTeachersOverviewResourcesExcelPath,
                                           scheduleClassroomsOverviewResourcesExcelPath,
                                           scheduleSubjectsOverviewResourcesExcelPath ]



##  5.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedOverviewResourcesExcelPath = os.path.join(documentsOverviewsGroupedPath, scheduleClassesGroupedOverviewResourcesExcelName)
# For the teachers grouped overview for the resources
scheduleTeachersGroupedOverviewResourcesExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleTeachersGroupedOverviewResourcesExcelName)
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedOverviewResourcesExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleClassroomsGroupedOverviewResourcesExcelName)
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedOverviewResourcesExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleSubjectsGroupedOverviewResourcesExcelName)

# For all of the above
allScheduleGroupedOverviewResourcesExcelPaths = [ scheduleClassesGroupedOverviewResourcesExcelPath,
                                                  scheduleTeachersGroupedOverviewResourcesExcelPath,
                                                  scheduleClassroomsGroupedOverviewResourcesExcelPath,
                                                  scheduleSubjectsGroupedOverviewResourcesExcelPath ]


##  5.1.8. OVERVIEW FOR RESOURCES BY DAYS  ##

# For the classes overview for the resources grouped by days
scheduleClassesOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesOverviewResourcesByDaysExcelName)
# For the teachers overview for the resources grouped by days
scheduleTeachersOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersOverviewResourcesByDaysExcelName)
# For the classrooms overview for the resources grouped by days
scheduleClassroomsOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsOverviewResourcesByDaysExcelName)
# For the subjects overview for the resources grouped by days
scheduleSubjectsOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsOverviewResourcesByDaysExcelName)

# For all of the above
allScheduleOverviewResourcesByDaysExcelPaths = [ scheduleClassesOverviewResourcesByDaysExcelPath,
                                                 scheduleTeachersOverviewResourcesByDaysExcelPath,
                                                 scheduleClassroomsOverviewResourcesByDaysExcelPath,
                                                 scheduleSubjectsOverviewResourcesByDaysExcelPath ]



##  5.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY DAYS  ##

# For the classes grouped overview for the resources grouped by days
scheduleClassesGroupedOverviewResourcesByDaysExcelPath = os.path.join(documentsOverviewsGroupedPath, scheduleClassesGroupedOverviewResourcesByDaysExcelName)
# For the teachers grouped overview for the resources grouped by days
scheduleTeachersGroupedOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleTeachersGroupedOverviewResourcesByDaysExcelName)
# For the classrooms grouped overview for the resources grouped by days
scheduleClassroomsGroupedOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleClassroomsGroupedOverviewResourcesByDaysExcelName)
# For the subjects grouped overview for the resources grouped by days
scheduleSubjectsGroupedOverviewResourcesByDaysExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleSubjectsGroupedOverviewResourcesByDaysExcelName)

# For all of the above
allScheduleGroupedOverviewResourcesByDaysExcelPaths = [ scheduleClassesGroupedOverviewResourcesByDaysExcelPath,
                                                        scheduleTeachersGroupedOverviewResourcesByDaysExcelPath,
                                                        scheduleClassroomsGroupedOverviewResourcesByDaysExcelPath,
                                                        scheduleSubjectsGroupedOverviewResourcesByDaysExcelPath ]


##  5.1.6. OVERVIEW FOR RESOURCES BY HOURS  ##

# For the classes overview for the resources grouped by hours
scheduleClassesOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesOverviewResourcesByHoursExcelName)
# For the teachers overview for the resources grouped by hours
scheduleTeachersOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersOverviewResourcesByHoursExcelName)
# For the classrooms overview for the resources grouped by hours
scheduleClassroomsOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsOverviewResourcesByHoursExcelName)
# For the subjects overview for the resources grouped by hours
scheduleSubjectsOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsOverviewResourcesByHoursExcelName)

# For all of the above
allScheduleOverviewResourcesByHoursExcelPaths = [ scheduleClassesOverviewResourcesByHoursExcelPath,
                                                  scheduleTeachersOverviewResourcesByHoursExcelPath,
                                                  scheduleClassroomsOverviewResourcesByHoursExcelPath,
                                                  scheduleSubjectsOverviewResourcesByHoursExcelPath ]



##  5.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS  ##

# For the classes grouped overview for the resources grouped by hours
scheduleClassesGroupedOverviewResourcesByHoursExcelPath = os.path.join(documentsOverviewsGroupedPath, scheduleClassesGroupedOverviewResourcesByHoursExcelName)
# For the teachers grouped overview for the resources grouped by hours
scheduleTeachersGroupedOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleTeachersGroupedOverviewResourcesByHoursExcelName)
# For the classrooms grouped overview for the resources grouped by hours
scheduleClassroomsGroupedOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleClassroomsGroupedOverviewResourcesByHoursExcelName)
# For the subjects grouped overview for the resources grouped by hours
scheduleSubjectsGroupedOverviewResourcesByHoursExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleSubjectsGroupedOverviewResourcesByHoursExcelName)

# For all of the above
allScheduleGroupedOverviewResourcesByHoursExcelPaths = [ scheduleClassesGroupedOverviewResourcesByHoursExcelPath,
                                                         scheduleTeachersGroupedOverviewResourcesByHoursExcelPath,
                                                         scheduleClassroomsGroupedOverviewResourcesByHoursExcelPath,
                                                         scheduleSubjectsGroupedOverviewResourcesByHoursExcelPath ]



###   5.2. JSON   ###

##  5.2.0 TEST  ##
testJSONPath = os.path.join(processingFilesJSONPath, testJSONName)



##  5.2.1 BASIC MAIN  ##

# For the pure scraped classes
scheduleClassesBaseJSONPath =  os.path.join(processingFilesJSONPath, scheduleClassesBaseJSONName)

# For the schedule lists with the grouped owners
scheduleListsOwnersGroupedJSONPath =  os.path.join(processingFilesJSONPath, scheduleListsOwnersGroupedDfsJSONName)



###   5.3. JSON with DataFrames   ###

##  5.3.1. BASIC MAIN  ##

# For the content of the current main (basic) Excel
scheduleClassesExcelDfsJSONPath =  os.path.join(processingFilesJSONPath, scheduleClassesExcelDfsJSONName)



##  5.3.2. BASIC  ##

# For the classes
scheduleClassesDfsJSONPath =  os.path.join(processingFilesJSONPath, scheduleClassesDfsJSONName)
# For the teachers
scheduleTeachersDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleTeachersDfsJSONName)
# For the classrooms
scheduleClassroomsDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleClassroomsDfsJSONName)
# For the subjects
scheduleSubjectsDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleSubjectsDfsJSONName)

# For all of the above
allScheduleDfsJSONPaths = [ scheduleClassesDfsJSONPath,
                            scheduleTeachersDfsJSONPath,
                            scheduleClassroomsDfsJSONPath,
                            scheduleSubjectsDfsJSONPath ]



##  5.3.3. BASIC EXTRA  ##

# For all the schedules written wide and vertically
schedulesWideAndVerticallyDfsJSONPath = os.path.join(processingFilesJSONPath, schedulesWideAndVerticallyDfsJSONName)
# For the classrooms written wide and vertically
scheduleClassroomsWideAndVerticallyDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleClassroomsWideAndVerticallyDfsJSONName)

# For the classrooms written briefly wide and vertically
scheduleClassroomsBrieflyWideAndVerticallyDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleClassroomsBrieflyWideAndVerticallyDfsJSONName)



##  5.3.4. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedDfsJSONPath = os.path.join(processingFilesJSONGroupedPath, scheduleClassesGroupedDfsJSONName)
# For the teachers grouped
scheduleTeachersGroupedDfsJSONPath = os.path.join(processingFilesJSONGroupedPath, scheduleTeachersGroupedDfsJSONName)
# For the classrooms grouped
scheduleClassroomsGroupedDfsJSONPath = os.path.join(processingFilesJSONGroupedPath, scheduleClassroomsGroupedDfsJSONName)
# For the subjects grouped
scheduleSubjectsGroupedDfsJSONPath = os.path.join(processingFilesJSONGroupedPath, scheduleSubjectsGroupedDfsJSONName)

# For all of the above
allScheduleGroupedDfsJSONPaths = [ scheduleClassesGroupedDfsJSONPath,
                                   scheduleTeachersGroupedDfsJSONPath,
                                   scheduleClassroomsGroupedDfsJSONPath,
                                   scheduleSubjectsGroupedDfsJSONPath ]



##  5.3.5. OVERVIEW FOR RESOURCES  ##

# For the classes overview for the resources
scheduleClassesOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassesOverviewResourcesDfsJSONName)
# For the teachers overview for the resources
scheduleTeachersOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleTeachersOverviewResourcesDfsJSONName)
# For the classrooms overview for the resources
scheduleClassroomsOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsOverviewResourcesDfsJSONName)
# For the subjects overview for the resources
scheduleSubjectsOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleSubjectsOverviewResourcesDfsJSONName)

# For all of the above
allScheduleOverviewResourcesDfsJSONPaths = [ scheduleClassesOverviewResourcesDfsJSONPath,
                                             scheduleTeachersOverviewResourcesDfsJSONPath,
                                             scheduleClassroomsOverviewResourcesDfsJSONPath,
                                             scheduleSubjectsOverviewResourcesDfsJSONPath ]



##  5.3.6. OVERVIEW [BASIC GROUPED] FOR RESOURCES  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedOverviewResourcesDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassesGroupedOverviewResourcesDfsJSONName)
# For the teachers grouped overview for the resources
scheduleTeachersGroupedOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleTeachersGroupedOverviewResourcesDfsJSONName)
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedOverviewResourcesDfsJSONName)
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedOverviewResourcesDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleSubjectsGroupedOverviewResourcesDfsJSONName)

# For all of the above
allScheduleGroupedOverviewResourcesDfsJSONPaths = [ scheduleClassesGroupedOverviewResourcesDfsJSONPath,
                                                    scheduleTeachersGroupedOverviewResourcesDfsJSONPath,
                                                    scheduleClassroomsGroupedOverviewResourcesDfsJSONPath,
                                                    scheduleSubjectsGroupedOverviewResourcesDfsJSONPath ]



##  5.3.7. OVERVIEW FOR RESOURCES BY DAYS  ##

# For the classes overview for the resources grouped by days
scheduleClassesOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassesOverviewResourcesByDaysDfsJSONName)
# For the teachers overview for the resources grouped by days
scheduleTeachersOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleTeachersOverviewResourcesByDaysDfsJSONName)
# For the classrooms overview for the resources grouped by days
scheduleClassroomsOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsOverviewResourcesByDaysDfsJSONName)
# For the subjects overview for the resources grouped by days
scheduleSubjectsOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleSubjectsOverviewResourcesByDaysDfsJSONName)

# For all of the above
allScheduleOverviewResourcesByDaysDfsJSONPaths = [ scheduleClassesOverviewResourcesByDaysDfsJSONPath,
                                                   scheduleTeachersOverviewResourcesByDaysDfsJSONPath,
                                                   scheduleClassroomsOverviewResourcesByDaysDfsJSONPath,
                                                   scheduleSubjectsOverviewResourcesByDaysDfsJSONPath ]



##  5.3.8. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY DAYS  ##

# For the classes grouped overview for the resources grouped by days
scheduleClassesGroupedOverviewResourcesByDaysDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassesGroupedOverviewResourcesByDaysDfsJSONName)
# For the teachers grouped overview for the resources grouped by days
scheduleTeachersGroupedOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleTeachersGroupedOverviewResourcesByDaysDfsJSONName)
# For the classrooms grouped overview for the resources grouped by days
scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONName)
# For the subjects grouped overview for the resources grouped by days
scheduleSubjectsGroupedOverviewResourcesByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleSubjectsGroupedOverviewResourcesByDaysDfsJSONName)

# For all of the above
allScheduleGroupedOverviewResourcesByDaysDfsJSONPaths = [ scheduleClassesGroupedOverviewResourcesByDaysDfsJSONPath,
                                                          scheduleTeachersGroupedOverviewResourcesByDaysDfsJSONPath,
                                                          scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONPath,
                                                          scheduleSubjectsGroupedOverviewResourcesByDaysDfsJSONPath ]


##  5.3.9. OVERVIEW FOR RESOURCES BY HOURS  ##

# For the classes overview for the resources grouped by hours
scheduleClassesOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassesOverviewResourcesByHoursDfsJSONName)
# For the teachers overview for the resources grouped by hours
scheduleTeachersOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleTeachersOverviewResourcesByHoursDfsJSONName)
# For the classrooms overview for the resources grouped by hours
scheduleClassroomsOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsOverviewResourcesByHoursDfsJSONName)
# For the subjects overview for the resources grouped by hours
scheduleSubjectsOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleSubjectsOverviewResourcesByHoursDfsJSONName)

# For all of the above
allScheduleOverviewResourcesByHoursDfsJSONPaths = [ scheduleClassesOverviewResourcesByHoursDfsJSONPath,
                                             scheduleTeachersOverviewResourcesByHoursDfsJSONPath,
                                             scheduleClassroomsOverviewResourcesByHoursDfsJSONPath,
                                             scheduleSubjectsOverviewResourcesByHoursDfsJSONPath ]



##  5.3.10. OVERVIEW [BASIC GROUPED] FOR RESOURCES BY HOURS  ##

# For the classes grouped overview for the resources grouped by hours
scheduleClassesGroupedOverviewResourcesByHoursDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassesGroupedOverviewResourcesByHoursDfsJSONName)
# For the teachers grouped overview for the resources grouped by hours
scheduleTeachersGroupedOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleTeachersGroupedOverviewResourcesByHoursDfsJSONName)
# For the classrooms grouped overview for the resources grouped by hours
scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONName)
# For the subjects grouped overview for the resources grouped by hours
scheduleSubjectsGroupedOverviewResourcesByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleSubjectsGroupedOverviewResourcesByHoursDfsJSONName)

# For all of the above
allScheduleGroupedOverviewResourcesByHoursDfsJSONPaths = [ scheduleClassesGroupedOverviewResourcesByHoursDfsJSONPath,
                                                           scheduleTeachersGroupedOverviewResourcesByHoursDfsJSONPath,
                                                           scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONPath,
                                                           scheduleSubjectsGroupedOverviewResourcesByHoursDfsJSONPath ]