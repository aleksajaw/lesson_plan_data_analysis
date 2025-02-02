
###########################################################################
#####                        Table of Contents                        ##### 
###########################################################################



    #####     1. DIR PATHS     #####

          ##  1.1. MAIN
          ##  1.2. OUTPUTS



    #####     2. PARTS OF FILE NAMES AND PATHS     #####

          ##  2.1. NAMES
          ##  2.2. EXTENSIONS
          ##  2.3. SUFIXES AND PREFIXES



    #####     3. FILE BASE NAMES     #####

          ##  3.1. BASIC
          ##  3.2. BASIC EXTRA
          ##  3.3. BASIC GROUPED
          ##  3.4. OVERVIEW
          ##  3.5. OVERVIEW [BASIC GROUPED]
          ##  3.6. OVERVIEW FOR RESOURCES
          ##  3.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES
          ##  3.8. OVERVIEW FOR TIME
          ##  3.9. OVERVIEW [BASIC GROUPED] FOR TIME



    #####     4. FILE NAMES     #####

        ###   4.1. Excel   ###

          ##  4.1.1. BASIC
          ##  4.1.2. BASIC EXTRA
          ##  4.1.3. BASIC GROUPED
          ##  4.1.4. OVERVIEW
          ##  4.1.5. OVERVIEW [BASIC GROUPED]
          ##  4.1.6. OVERVIEW FOR RESOURCES
          ##  4.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES


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


        ###   5.2. JSON   ###

          ##  5.2.1 BASIC MAIN


        ###   5.3. JSON with DataFrames   ###

          ##  5.3.1. BASIC MAIN
          ##  5.3.2. BASIC
          ##  5.3.3. BASIC EXTRA
          ##  5.3.4. BASIC GROUPED



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
#schedulesPath = os.path.join(srcDirPath, 'schedules')
schedulesPath = os.path.join(projectRoot, 'schedules')
#scheduleJSONPath = os.path.join(schedulesPath, 'json')

logsPath = os.path.join(projectRoot, 'logs')

processingFilesPath = os.path.join(projectRoot, 'processing_files')
processingFilesJSONPath = os.path.join(processingFilesPath, 'json')
processingFilesExcelPath = os.path.join(processingFilesPath, 'excel')



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



##  2.3 SUFIXES AND PREFIXES  ##
dfsPrefix = 'dfs_'
schedulePrefixMain = scheduleName + '_'
schedulePartOfPrefix = scheduleName + '-'
groupedSufix = '-grouped'
overviewSufix = '_overview'
resourcesSufix = '_resources'
timeSufix = '_time'
wideSuffix = '_wide'
verticallySufix = '_vertically'



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
schedulesWideAndVerticallyBaseName = schedulesBaseName + wideSuffix + verticallySufix

# For the classes vertically
scheduleClassesVerticallyBaseName = scheduleClassesBaseName + verticallySufix

# For the classrooms grouped overview for the resources vertically
scheduleClassroomsGroupedOverviewResourcesVerticallyBaseName  = scheduleClassroomsBaseName + overviewSufix + resourcesSufix + verticallySufix + extExcel


##  3.3. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedBaseName = scheduleClassesBaseName + groupedSufix
# For the teachers grouped
scheduleTeachersGroupedBaseName = scheduleTeachersBaseName + groupedSufix
# For the classrooms grouped
scheduleClassroomsGroupedBaseName = scheduleClassroomsBaseName + groupedSufix
# For the subjects grouped
scheduleSubjectsGroupedBaseName = scheduleSubjectsBaseName + groupedSufix

# For all of the above
allScheduleGroupedBaseNames = [ scheduleClassesGroupedBaseName,
                                scheduleTeachersGroupedBaseName,
                                scheduleClassroomsGroupedBaseName,
                                scheduleSubjectsGroupedBaseName ]



##  3.4. OVERVIEW  ##

# For the classes overview
scheduleClassesOverviewBaseName = scheduleClassesBaseName + overviewSufix
# For the teachers overview
scheduleTeachersOverviewBaseName = scheduleTeachersBaseName + overviewSufix
# For the classrooms overview
scheduleClassroomsOverviewBaseName = scheduleClassroomsBaseName + overviewSufix
# For the subjects overview
scheduleSubjectsOverviewBaseName = scheduleSubjectsBaseName +  overviewSufix

# For all of the above
allScheduleGroupedOverviewBaseNames = [ scheduleClassesOverviewBaseName,
                                        scheduleTeachersOverviewBaseName,
                                        scheduleClassroomsOverviewBaseName,
                                        scheduleSubjectsOverviewBaseName ]



##  3.5. OVERVIEW [BASIC GROUPED]  ##

# For the classes grouped overview
scheduleClassesGroupedOverviewBaseName = scheduleClassesGroupedBaseName + overviewSufix
# For the teachers grouped overview
scheduleTeachersGroupedOverviewBaseName = scheduleTeachersGroupedBaseName + overviewSufix
# For the classrooms grouped overview
scheduleClassroomsGroupedOverviewBaseName = scheduleClassroomsGroupedBaseName + overviewSufix
# For the subjects grouped overview
scheduleSubjectsGroupedOverviewBaseName = scheduleSubjectsGroupedBaseName + overviewSufix

# For all of the above
allScheduleGroupedOverviewBaseNames = [ scheduleClassesGroupedOverviewBaseName,
                                        scheduleTeachersGroupedOverviewBaseName,
                                        scheduleClassroomsGroupedOverviewBaseName,
                                        scheduleSubjectsGroupedOverviewBaseName ]



##  3.6. OVERVIEW FOR RESOURCES  ##

# For the classes overview for the resources
scheduleClassesOverviewResourcesBaseName = scheduleClassesOverviewBaseName + resourcesSufix
# For the teachers overview for the resources
scheduleTeachersOverviewResourcesBaseName = scheduleTeachersOverviewBaseName + resourcesSufix
# For the classrooms overview for the resources
scheduleClassroomsOverviewResourcesBaseName = scheduleClassroomsOverviewBaseName + resourcesSufix
# For the subjects overview for the resources
scheduleSubjectsOverviewResourcesBaseName = scheduleSubjectsOverviewBaseName + resourcesSufix

# For all of the above
allScheduleOverviewResourcesBaseNames = [ scheduleClassesOverviewResourcesBaseName,
                                          scheduleTeachersOverviewResourcesBaseName,
                                          scheduleClassroomsOverviewResourcesBaseName,
                                          scheduleSubjectsOverviewResourcesBaseName ]



##  3.7. OVERVIEW [BASIC GROUPED] FOR RESOURCES  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedOverviewResourcesBaseName = scheduleClassesGroupedOverviewBaseName + resourcesSufix
# For the teachers grouped overview for the resources
scheduleTeachersGroupedOverviewResourcesBaseName = scheduleTeachersGroupedOverviewBaseName + resourcesSufix
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedOverviewResourcesBaseName = scheduleClassroomsGroupedOverviewBaseName + resourcesSufix
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedOverviewResourcesBaseName = scheduleSubjectsGroupedOverviewBaseName + resourcesSufix

# For all of the above
allScheduleGroupedOverviewResourcesBaseNames = [ scheduleClassesGroupedOverviewResourcesBaseName,
                                                 scheduleTeachersGroupedOverviewResourcesBaseName,
                                                 scheduleClassroomsGroupedOverviewResourcesBaseName,
                                                 scheduleSubjectsGroupedOverviewResourcesBaseName ]



##  3.8. OVERVIEW FOR TIME  ##

# For the classes overview for the time
scheduleClassesOverviewTimeBaseName = scheduleClassesOverviewBaseName + timeSufix
# For the teachers overview for  the time
scheduleTeachersOverviewTimeBaseName = scheduleTeachersOverviewBaseName + timeSufix
# For the classrooms overview for  the time
scheduleClassroomsOverviewTimeBaseName = scheduleClassroomsOverviewBaseName + timeSufix
# For the subjects overview for  the time
scheduleSubjectsOverviewTimeBaseName = scheduleSubjectsOverviewBaseName + timeSufix

# For all of the above
allScheduleOverviewTimeBaseNames = [ scheduleClassesOverviewTimeBaseName,
                                     scheduleTeachersOverviewTimeBaseName,
                                     scheduleClassroomsOverviewTimeBaseName,
                                     scheduleSubjectsOverviewTimeBaseName ]



##  3.9. OVERVIEW [BASIC GROUPED] FOR TIME  ##

# For the classes grouped overview for time
scheduleClassesGroupedOverviewTimeBaseName = scheduleClassesGroupedOverviewBaseName + timeSufix
# For the teachers grouped overview for time
scheduleTeachersGroupedOverviewTimeBaseName = scheduleTeachersGroupedOverviewBaseName + timeSufix
# For the classrooms grouped overview for time
scheduleClassroomsGroupedOverviewTimeBaseName = scheduleClassroomsGroupedOverviewBaseName + timeSufix
# For the subjects grouped overview for time
scheduleSubjectsGroupedOverviewTimeBaseName = scheduleSubjectsGroupedOverviewBaseName + timeSufix

# For all of the above
allScheduleGroupedOverviewTimeBaseNames = [ scheduleClassesGroupedOverviewTimeBaseName,
                                            scheduleTeachersGroupedOverviewTimeBaseName,
                                            scheduleClassroomsGroupedOverviewTimeBaseName,
                                            scheduleSubjectsGroupedOverviewTimeBaseName ]



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

# For the classes vertically
scheduleClassesVerticallyExcelName = scheduleClassesVerticallyBaseName + extExcel

# For the classrooms grouped overview for the resources vertically
scheduleClassroomsGroupedOverviewResourcesVerticallyExcelName  = scheduleClassroomsGroupedOverviewResourcesVerticallyBaseName + extExcel

# For the lists of schedule owners
scheduleListsOwnersGroupedExcelName = schedulePartOfPrefix + 'lists_owners' + groupedSufix + extExcel



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
scheduleListsOwnersGroupedDfsJSONName = dfsPrefix + schedulePartOfPrefix + 'lists_owners' + groupedSufix + extJSON

# For all the schedules wide and vertically
schedulesWideAndVerticallyDfsJSONName = dfsPrefix + schedulesWideAndVerticallyBaseName + extJSON



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



##  5.3.4. BASIC GROUPED  ##

# For the classes grouped
scheduleClassesGroupedDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleClassesGroupedDfsJSONName)
# For the teachers grouped
scheduleTeachersGroupedDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleTeachersGroupedDfsJSONName)
# For the classrooms grouped
scheduleClassroomsGroupedDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleClassroomsGroupedDfsJSONName)
# For the subjects grouped
scheduleSubjectsGroupedDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleSubjectsGroupedDfsJSONName)

# For all of the above
allScheduleGroupedDfsJSONPaths = [ scheduleClassesGroupedDfsJSONPath,
                                   scheduleTeachersGroupedDfsJSONPath,
                                   scheduleClassroomsGroupedDfsJSONPath,
                                   scheduleSubjectsGroupedDfsJSONPath ]