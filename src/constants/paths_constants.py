
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
          ##  3.6. OVERVIEW FOR LESSONS BY NUMBERS
          ##  3.7. OVERVIEW [BASIC GROUPED] FOR LESSONS BY NUMBERS
          ##  3.8. OVERVIEW FOR RESOURCE ALLOCATION
          ##  3.9. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION
          ##  3.10. OVERVIEW RESOURCE ALLOCATION BY DAYS
          ##  3.11. OVERVIEW [BASIC GROUPED] RESOURCE ALLOCATION BY DAYS
          ##  3.12. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS
          ##  3.13. OVERVIEW [BASIC GROUPED] RESOURCE ALLOCATION BY HOURS



    #####     4. FILE NAMES     #####

        ###   4.1. Excel   ###

          ##  4.1.1. BASIC
          ##  4.1.2. BASIC EXTRA
          ##  4.1.3. BASIC GROUPED
          ##  4.1.4. OVERVIEW
          ##  4.1.5. OVERVIEW [BASIC GROUPED]
          ##  4.1.6. OVERVIEW FOR RESOURCE ALLOCATION
          ##  4.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION
          ##  4.1.8. OVERVIEW FOR RESOURCE ALLOCATION BY NUMBERS
          ##  4.1.9. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS
          ##  4.1.10. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS
          ##  4.1.11. OVERVIEW [BASIC GROUPED] RESOURCE ALLOCATION BY DAYS
          ##  4.1.12. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS
          ##  4.1.13. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS


        ###   4.2. JSON   ###

          ##  4.2.1. BASIC MAIN
          ##  4.2.2  BASIC EXTRA


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
          ##  5.1.6. OVERVIEW FOR RESOURCE ALLOCATION
          ##  5.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION
          ##  5.1.8. OVERVIEW FOR RESOURCE ALLOCATION BY NUMBERS
          ##  5.1.9. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS
          ##  5.1.10. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS
          ##  5.1.11. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY DAYS
          ##  5.1.12. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS
          ##  5.1.13. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS


        ###   5.2. JSON   ###

          ##  5.2.1 BASIC MAIN


        ###   5.3. JSON with DataFrames   ###

          ##  5.3.1. BASIC MAIN
          ##  5.3.2. BASIC
          ##  5.3.3. BASIC EXTRA
          ##  5.3.4. BASIC GROUPED
          ##  5.3.5. OVERVIEW FOR RESOURCE ALLOCATION
          ##  5.3.6. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION
          ##  5.3.7. OVERVIEW FOR RESOURCE ALLOCATION BY NUMBERS
          ##  5.3.8. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS
          ##  5.3.9. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS
          ##  5.3.10. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY DAYS
          ##  5.3.11. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS
          ##  5.3.12. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS


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
overviewSuffix = '_OV'
resourceAllocSuffix = '_resource-alloc'
byHoursSuffix = '-by-hours'
byDaysSuffix = '-by-days'
wideSuffix = '_wide'
verticalSuffix = '_vertical'
brieflySuffix = '_briefly'
byNumbersSuffix = '_lessons-by-numbers'



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

# For all the schedules in wide and vertical format
schedulesWideAndVertBaseName = schedulesBaseName + wideSuffix + verticalSuffix

# For the classrooms in wide and vertical format
scheduleClassroomsWideAndVertBaseName = scheduleClassroomsBaseName + wideSuffix + verticalSuffix

# For the classes vertical
scheduleClassesVertBaseName = scheduleClassesBaseName + verticalSuffix



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



##  3.6. OVERVIEW FOR RESOURCE ALLOCATION  ##

# For the classes overview for the resources
scheduleClassesResourceAllocBaseName = scheduleClassesOverviewBaseName + resourceAllocSuffix
# For the teachers overview for the resources
scheduleTeachersResourceAllocBaseName = scheduleTeachersOverviewBaseName + resourceAllocSuffix
# For the classrooms overview for the resources
scheduleClassroomsResourceAllocBaseName = scheduleClassroomsOverviewBaseName + resourceAllocSuffix
# For the subjects overview for the resources
scheduleSubjectsResourceAllocBaseName = scheduleSubjectsOverviewBaseName + resourceAllocSuffix

# For all of the above
allScheduleResourceAllocBaseNames = [ scheduleClassesResourceAllocBaseName,
                                      scheduleTeachersResourceAllocBaseName,
                                      scheduleClassroomsResourceAllocBaseName,
                                      scheduleSubjectsResourceAllocBaseName ]



##  3.7. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedResourceAllocBaseName = scheduleClassesGroupedOverviewBaseName + resourceAllocSuffix
# For the teachers grouped overview for the resources
scheduleTeachersGroupedResourceAllocBaseName = scheduleTeachersGroupedOverviewBaseName + resourceAllocSuffix
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedResourceAllocBaseName = scheduleClassroomsGroupedOverviewBaseName + resourceAllocSuffix
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedResourceAllocBaseName = scheduleSubjectsGroupedOverviewBaseName + resourceAllocSuffix

# For all of the above
allScheduleGroupedResourceAllocBaseNames = [ scheduleClassesGroupedResourceAllocBaseName,
                                             scheduleTeachersGroupedResourceAllocBaseName,
                                             scheduleClassroomsGroupedResourceAllocBaseName,
                                             scheduleSubjectsGroupedResourceAllocBaseName ]



##  3.8. OVERVIEW FOR LESSONS BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsWideAndVertOverviewByNumbersBaseName = scheduleClassroomsBaseName + wideSuffix + verticalSuffix + overviewSuffix + byNumbersSuffix



##  3.9. OVERVIEW BASIC GROUPED] FOR LESSONS BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsGroupedWideAndVertOverviewByNumbersBaseName = scheduleClassroomsBaseName + groupedSuffix + wideSuffix + verticalSuffix + overviewSuffix + byNumbersSuffix



##  3.10. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes overview for the resource allocation by days
scheduleClassesResourceAllocByDaysBaseName = scheduleClassesResourceAllocBaseName + byDaysSuffix
# For the teachers overview for the resource allocation by days
scheduleTeachersResourceAllocByDaysBaseName = scheduleTeachersResourceAllocBaseName + byDaysSuffix
# For the classrooms overview for the resource allocation by days
scheduleClassroomsResourceAllocByDaysBaseName = scheduleClassroomsResourceAllocBaseName + byDaysSuffix
# For the subjects overview for the resource allocation by days
scheduleSubjectsResourceAllocByDaysBaseName = scheduleSubjectsResourceAllocBaseName + byDaysSuffix

# For all of the above
allScheduleResourceAllocByDaysBaseNames = [ scheduleClassesResourceAllocByDaysBaseName,
                                            scheduleTeachersResourceAllocByDaysBaseName,
                                            scheduleClassroomsResourceAllocByDaysBaseName,
                                            scheduleSubjectsResourceAllocByDaysBaseName ]



##  3.11. OVERVIEW [BASIC GROUPED] BY DAYS  ##

# For the classes grouped overview for the resource allocation by days
scheduleClassesGroupedResourceAllocByDaysBaseName = scheduleClassesGroupedResourceAllocBaseName + byDaysSuffix
# For the teachers grouped overview for the resource allocation by days
scheduleTeachersGroupedResourceAllocByDaysBaseName = scheduleTeachersGroupedResourceAllocBaseName + byDaysSuffix
# For the classrooms grouped overview for the resource allocation by days
scheduleClassroomsGroupedResourceAllocByDaysBaseName = scheduleClassroomsGroupedResourceAllocBaseName + byDaysSuffix
# For the subjects grouped overview for the resource allocation by days
scheduleSubjectsGroupedResourceAllocByDaysBaseName = scheduleSubjectsGroupedResourceAllocBaseName + byDaysSuffix

# For all of the above
allScheduleGroupedResourceAllocByDaysBaseNames = [ scheduleClassesGroupedResourceAllocByDaysBaseName,
                                                   scheduleTeachersGroupedResourceAllocByDaysBaseName,
                                                   scheduleClassroomsGroupedResourceAllocByDaysBaseName,
                                                   scheduleSubjectsGroupedResourceAllocByDaysBaseName ]



##  3.12. OVERVIEW BY HOURS  ##

# For the classes overview for the resource allocation by hours
scheduleClassesResourceAllocByHoursBaseName = scheduleClassesResourceAllocBaseName + byHoursSuffix
# For the teachers overview for the resource allocation by hours
scheduleTeachersResourceAllocByHoursBaseName = scheduleTeachersResourceAllocBaseName + byHoursSuffix
# For the classrooms overview for the resource allocation by hours
scheduleClassroomsResourceAllocByHoursBaseName = scheduleClassroomsResourceAllocBaseName + byHoursSuffix
# For the subjects overview for the resource allocation by hours
scheduleSubjectsResourceAllocByHoursBaseName = scheduleSubjectsResourceAllocBaseName + byHoursSuffix

# For all of the above
allScheduleResourceAllocByHoursBaseNames = [ scheduleClassesResourceAllocByHoursBaseName,
                                             scheduleTeachersResourceAllocByHoursBaseName,
                                             scheduleClassroomsResourceAllocByHoursBaseName,
                                             scheduleSubjectsResourceAllocByHoursBaseName ]



##  3.13. OVERVIEW [BASIC GROUPED] BY HOURS  ##

# For the classes grouped overview for the resource allocation by hours
scheduleClassesGroupedResourceAllocByHoursBaseName = scheduleClassesGroupedResourceAllocBaseName + byHoursSuffix
# For the teachers grouped overview for the resource allocation by hours
scheduleTeachersGroupedResourceAllocByHoursBaseName = scheduleTeachersGroupedResourceAllocBaseName + byHoursSuffix
# For the classrooms grouped overview for the resource allocation by hours
scheduleClassroomsGroupedResourceAllocByHoursBaseName = scheduleClassroomsGroupedResourceAllocBaseName + byHoursSuffix
# For the subjects grouped overview for the resource allocation by hours
scheduleSubjectsGroupedResourceAllocByHoursBaseName = scheduleSubjectsGroupedResourceAllocBaseName + byHoursSuffix

# For all of the above
allScheduleGroupedResourceAllocByHoursBaseNames = [ scheduleClassesGroupedResourceAllocByHoursBaseName,
                                                    scheduleTeachersGroupedResourceAllocByHoursBaseName,
                                                    scheduleClassroomsGroupedResourceAllocByHoursBaseName,
                                                    scheduleSubjectsGroupedResourceAllocByHoursBaseName ]



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

# For the lists of schedule owners
scheduleListsOwnersGroupedExcelName = schedulePartOfPrefix + 'lists_owners' + groupedSuffix + extExcel


# For all the schedules in wide and vertical format
schedulesWideAndVertExcelName = schedulesWideAndVertBaseName + extExcel

# For the classrooms in wide and vertical format
scheduleClassroomsWideAndVertExcelName = scheduleClassroomsWideAndVertBaseName + extExcel

# For the classes vertical
scheduleClassesVertExcelName = scheduleClassesVertBaseName + extExcel



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



##  4.1.6. OVERVIEW FOR RESOURCE ALLOCATION  ##

# For the classes overview for the resources
scheduleClassesResourceAllocExcelName = scheduleClassesResourceAllocBaseName + extExcel
# For the teachers overview for the resources
scheduleTeachersResourceAllocExcelName = scheduleTeachersResourceAllocBaseName + extExcel
# For the classrooms overview for the resources
scheduleClassroomsResourceAllocExcelName = scheduleClassroomsResourceAllocBaseName + extExcel
# For the subjects overview for the resources
scheduleSubjectsResourceAllocExcelName = scheduleSubjectsResourceAllocBaseName + extExcel

# For all of the above
allScheduleResourceAllocExcelNames = [ scheduleClassesResourceAllocExcelName,
                                       scheduleTeachersResourceAllocExcelName,
                                       scheduleClassroomsResourceAllocExcelName,
                                       scheduleSubjectsResourceAllocExcelName ]



##  4.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedResourceAllocExcelName = scheduleClassesGroupedResourceAllocBaseName + extExcel
# For the teachers grouped overview for the resources
scheduleTeachersGroupedResourceAllocExcelName = scheduleTeachersGroupedResourceAllocBaseName + extExcel
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedResourceAllocExcelName = scheduleClassroomsGroupedResourceAllocBaseName + extExcel
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedResourceAllocExcelName = scheduleSubjectsGroupedResourceAllocBaseName + extExcel

# For all of the above
allScheduleGroupedResourceAllocExcelNames = [ scheduleClassesGroupedResourceAllocExcelName,
                                              scheduleTeachersGroupedResourceAllocExcelName,
                                              scheduleClassroomsGroupedResourceAllocExcelName,
                                              scheduleSubjectsGroupedResourceAllocExcelName ]



##  4.1.8. OVERVIEW FOR RESOURCE ALLOCATION BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsWideAndVertOverviewByNumbersExcelName = scheduleClassroomsWideAndVertOverviewByNumbersBaseName + extExcel



##  4.1.9. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsGroupedWideAndVertOverviewByNumbersExcelName = scheduleClassroomsGroupedWideAndVertOverviewByNumbersBaseName + extExcel



##  4.1.10. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes overview for the resource allocation by days
scheduleClassesResourceAllocByDaysExcelName = scheduleClassesResourceAllocByDaysBaseName + extExcel
# For the teachers overview for the resource allocation by days
scheduleTeachersResourceAllocByDaysExcelName = scheduleTeachersResourceAllocByDaysBaseName + extExcel
# For the classrooms overview for the resource allocation by days
scheduleClassroomsResourceAllocByDaysExcelName = scheduleClassroomsResourceAllocByDaysBaseName + extExcel
# For the subjects overview for the resource allocation by days
scheduleSubjectsResourceAllocByDaysExcelName = scheduleSubjectsResourceAllocByDaysBaseName + extExcel

# For all of the above
allScheduleResourceAllocByDaysExcelNames = [ scheduleClassesResourceAllocByDaysExcelName,
                                             scheduleTeachersResourceAllocByDaysExcelName,
                                             scheduleClassroomsResourceAllocByDaysExcelName,
                                             scheduleSubjectsResourceAllocByDaysExcelName ]



##  4.1.11. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes grouped overview for the resource allocation by days
scheduleClassesGroupedResourceAllocByDaysExcelName = scheduleClassesGroupedResourceAllocByDaysBaseName + extExcel
# For the teachers grouped overview for the resource allocation by days
scheduleTeachersGroupedResourceAllocByDaysExcelName = scheduleTeachersGroupedResourceAllocByDaysBaseName + extExcel
# For the classrooms grouped overview for the resource allocation by days
scheduleClassroomsGroupedResourceAllocByDaysExcelName = scheduleClassroomsGroupedResourceAllocByDaysBaseName + extExcel
# For the subjects grouped overview for the resource allocation by days
scheduleSubjectsGroupedResourceAllocByDaysExcelName = scheduleSubjectsGroupedResourceAllocByDaysBaseName + extExcel

# For all of the above
allScheduleGroupedResourceAllocByDaysExcelNames = [ scheduleClassesGroupedResourceAllocByDaysExcelName,
                                                    scheduleTeachersGroupedResourceAllocByDaysExcelName,
                                                    scheduleClassroomsGroupedResourceAllocByDaysExcelName,
                                                    scheduleSubjectsGroupedResourceAllocByDaysExcelName ]



##  4.1.12. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS ##

# For the classes overview for the resource allocation by hours
scheduleClassesResourceAllocByHoursExcelName = scheduleClassesResourceAllocByHoursBaseName + extExcel
# For the teachers overview for the resource allocation by hours
scheduleTeachersResourceAllocByHoursExcelName = scheduleTeachersResourceAllocByHoursBaseName + extExcel
# For the classrooms overview for the resource allocation by hours
scheduleClassroomsResourceAllocByHoursExcelName = scheduleClassroomsResourceAllocByHoursBaseName + extExcel
# For the subjects overview for the resource allocation by hours
scheduleSubjectsResourceAllocByHoursExcelName = scheduleSubjectsResourceAllocByHoursBaseName + extExcel

# For all of the above
allScheduleResourceAllocByHoursExcelNames = [ scheduleClassesResourceAllocByHoursExcelName,
                                              scheduleTeachersResourceAllocByHoursExcelName,
                                              scheduleClassroomsResourceAllocByHoursExcelName,
                                              scheduleSubjectsResourceAllocByHoursExcelName ]



##  4.1.13. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes grouped overview for the resource allocation by hours
scheduleClassesGroupedResourceAllocByHoursExcelName = scheduleClassesGroupedResourceAllocByHoursBaseName + extExcel
# For the teachers grouped overview for the resource allocation by hours
scheduleTeachersGroupedResourceAllocByHoursExcelName = scheduleTeachersGroupedResourceAllocByHoursBaseName + extExcel
# For the classrooms grouped overview for the resource allocation by hours
scheduleClassroomsGroupedResourceAllocByHoursExcelName = scheduleClassroomsGroupedResourceAllocByHoursBaseName + extExcel
# For the subjects grouped overview for the resource allocation by hours
scheduleSubjectsGroupedResourceAllocByHoursExcelName = scheduleSubjectsGroupedResourceAllocByHoursBaseName + extExcel

# For all of the above
allScheduleGroupedResourceAllocByHoursExcelNames = [ scheduleClassesGroupedResourceAllocByHoursExcelName,
                                                     scheduleTeachersGroupedResourceAllocByHoursExcelName,
                                                     scheduleClassroomsGroupedResourceAllocByHoursExcelName,
                                                     scheduleSubjectsGroupedResourceAllocByHoursExcelName ]



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


# For all the schedules in wide and vertical format
schedulesWideAndVertDfsJSONName = dfsPrefix + schedulesWideAndVertBaseName + extJSON

# For the classrooms in wide and vertical format
scheduleClassroomsWideAndVertDfsJSONName = dfsPrefix + scheduleClassroomsWideAndVertBaseName + extJSON



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



##  4.3.5. OVERVIEW FOR RESOURCE ALLOCATION  ##

# For the classes overview for the resources
scheduleClassesResourceAllocDfsJSONName = multiDfsPrefix + scheduleClassesResourceAllocBaseName + extJSON
# For the teachers overview for the resources
scheduleTeachersResourceAllocDfsJSONName = multiDfsPrefix + scheduleTeachersResourceAllocBaseName + extJSON
# For the classrooms overview for the resources
scheduleClassroomsResourceAllocDfsJSONName = multiDfsPrefix + scheduleClassroomsResourceAllocBaseName + extJSON
# For the subjects overview for the resources
scheduleSubjectsResourceAllocDfsJSONName = multiDfsPrefix + scheduleSubjectsResourceAllocBaseName + extJSON

# For all of the above
allScheduleResourceAllocDfsJSONNames = [ scheduleClassesResourceAllocDfsJSONName,
                                         scheduleTeachersResourceAllocDfsJSONName,
                                         scheduleClassroomsResourceAllocDfsJSONName,
                                         scheduleSubjectsResourceAllocDfsJSONName ]



##  4.3.6. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedResourceAllocDfsJSONName = multiDfsPrefix + scheduleClassesGroupedResourceAllocBaseName + extJSON
# For the teachers grouped overview for the resources
scheduleTeachersGroupedResourceAllocDfsJSONName = multiDfsPrefix + scheduleTeachersGroupedResourceAllocBaseName + extJSON
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedResourceAllocDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedResourceAllocBaseName + extJSON
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedResourceAllocDfsJSONName = multiDfsPrefix + scheduleSubjectsGroupedResourceAllocBaseName + extJSON

# For all of the above
allScheduleGroupedResourceAllocDfsJSONNames = [ scheduleClassesGroupedResourceAllocDfsJSONName,
                                                scheduleTeachersGroupedResourceAllocDfsJSONName,
                                                scheduleClassroomsGroupedResourceAllocDfsJSONName,
                                                scheduleSubjectsGroupedResourceAllocDfsJSONName ]



##  4.3.7. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsWideAndVertOverviewByNumbersDfsJSONName = multiDfsPrefix + scheduleClassroomsWideAndVertOverviewByNumbersBaseName + extJSON



##  4.3.8. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsGroupedWideAndVertOverviewByNumbersDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedWideAndVertOverviewByNumbersBaseName + extJSON



##  4.3.9. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes overview for the resource allocation by days
scheduleClassesResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleClassesResourceAllocByDaysBaseName + extJSON
# For the teachers overview for the resource allocation by days
scheduleTeachersResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleTeachersResourceAllocByDaysBaseName + extJSON
# For the classrooms overview for the resource allocation by days
scheduleClassroomsResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleClassroomsResourceAllocByDaysBaseName + extJSON
# For the subjects overview for the resource allocation by days
scheduleSubjectsResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleSubjectsResourceAllocByDaysBaseName + extJSON

# For all of the above
allScheduleResourceAllocByDaysDfsJSONNames = [ scheduleClassesResourceAllocByDaysDfsJSONName,
                                               scheduleTeachersResourceAllocByDaysDfsJSONName,
                                               scheduleClassroomsResourceAllocByDaysDfsJSONName,
                                               scheduleSubjectsResourceAllocByDaysDfsJSONName ]



##  4.3.10. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes grouped overview for the resource allocation by days
scheduleClassesGroupedResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleClassesGroupedResourceAllocByDaysBaseName + extJSON
# For the teachers grouped overview for the resource allocation by days
scheduleTeachersGroupedResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleTeachersGroupedResourceAllocByDaysBaseName + extJSON
# For the classrooms grouped overview for the resource allocation by days
scheduleClassroomsGroupedResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedResourceAllocByDaysBaseName + extJSON
# For the subjects grouped overview for the resource allocation by days
scheduleSubjectsGroupedResourceAllocByDaysDfsJSONName = multiDfsPrefix + scheduleSubjectsGroupedResourceAllocByDaysBaseName + extJSON

# For all of the above
allScheduleGroupedResourceAllocByDaysDfsJSONNames = [ scheduleClassesGroupedResourceAllocByDaysDfsJSONName,
                                                      scheduleTeachersGroupedResourceAllocByDaysDfsJSONName,
                                                      scheduleClassroomsGroupedResourceAllocByDaysDfsJSONName,
                                                      scheduleSubjectsGroupedResourceAllocByDaysDfsJSONName ]


##  4.3.11. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes overview for the resource allocation by hours
scheduleClassesResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleClassesResourceAllocByHoursBaseName + extJSON
# For the teachers overview for the resource allocation by hours
scheduleTeachersResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleTeachersResourceAllocByHoursBaseName + extJSON
# For the classrooms overview for the resource allocation by hours
scheduleClassroomsResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleClassroomsResourceAllocByHoursBaseName + extJSON
# For the subjects overview for the resource allocation by hours
scheduleSubjectsResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleSubjectsResourceAllocByHoursBaseName + extJSON

# For all of the above
allScheduleResourceAllocByHoursDfsJSONNames = [ scheduleClassesResourceAllocByHoursDfsJSONName,
                                                scheduleTeachersResourceAllocByHoursDfsJSONName,
                                                scheduleClassroomsResourceAllocByHoursDfsJSONName,
                                                scheduleSubjectsResourceAllocByHoursDfsJSONName ]



##  4.3.12. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes grouped overview for the resource allocation by hours
scheduleClassesGroupedResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleClassesGroupedResourceAllocByHoursBaseName + extJSON
# For the teachers grouped overview for the resource allocation by hours
scheduleTeachersGroupedResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleTeachersGroupedResourceAllocByHoursBaseName + extJSON
# For the classrooms grouped overview for the resource allocation by hours
scheduleClassroomsGroupedResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleClassroomsGroupedResourceAllocByHoursBaseName + extJSON
# For the subjects grouped overview for the resource allocation by hours
scheduleSubjectsGroupedResourceAllocByHoursDfsJSONName = multiDfsPrefix + scheduleSubjectsGroupedResourceAllocByHoursBaseName + extJSON

# For all of the above
allScheduleGroupedResourceAllocByHoursDfsJSONNames = [ scheduleClassesGroupedResourceAllocByHoursDfsJSONName,
                                                       scheduleTeachersGroupedResourceAllocByHoursDfsJSONName,
                                                       scheduleClassroomsGroupedResourceAllocByHoursDfsJSONName,
                                                       scheduleSubjectsGroupedResourceAllocByHoursDfsJSONName ]



#####     5. FILE PATHS     #####


###    5.1 Excel   ###

##  5.1.0 TEST  ##
testExcelPath = os.path.join(documentsPrototypesPath, testExcelName)



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

# For schedule lists with grouped owners
scheduleListsOwnersGroupedExcelPath =  os.path.join(processingFilesExcelPath, scheduleListsOwnersGroupedExcelName)


# For all the schedules in wide and vertical format
schedulesWideAndVertExcelPath = os.path.join(documentsPath, schedulesWideAndVertExcelName)

# For the classrooms in wide and vertical format
scheduleClassroomsWideAndVertExcelPath = os.path.join(documentsPath, scheduleClassroomsWideAndVertExcelName)

# For the classes vertical
scheduleClassesVertExcelPath = os.path.join(documentsPrototypesPath, scheduleClassesVertExcelName)



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



##  5.1.6. OVERVIEW FOR RESOURCE ALLOCATION  ##

# For the classes overview for the resources
scheduleClassesResourceAllocExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesResourceAllocExcelName)
# For the teachers overview for the resources
scheduleTeachersResourceAllocExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersResourceAllocExcelName)
# For the classrooms overview for the resources
scheduleClassroomsResourceAllocExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsResourceAllocExcelName)
# For the subjects overview for the resources
scheduleSubjectsResourceAllocExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsResourceAllocExcelName)

# For all of the above
allScheduleResourceAllocExcelPaths = [ scheduleClassesResourceAllocExcelPath,
                                       scheduleTeachersResourceAllocExcelPath,
                                       scheduleClassroomsResourceAllocExcelPath,
                                       scheduleSubjectsResourceAllocExcelPath ]



##  5.1.7. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedResourceAllocExcelPath = os.path.join(documentsOverviewsGroupedPath, scheduleClassesGroupedResourceAllocExcelName)
# For the teachers grouped overview for the resources
scheduleTeachersGroupedResourceAllocExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleTeachersGroupedResourceAllocExcelName)
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedResourceAllocExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleClassroomsGroupedResourceAllocExcelName)
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedResourceAllocExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleSubjectsGroupedResourceAllocExcelName)

# For all of the above
allScheduleGroupedResourceAllocExcelPaths = [ scheduleClassesGroupedResourceAllocExcelPath,
                                              scheduleTeachersGroupedResourceAllocExcelPath,
                                              scheduleClassroomsGroupedResourceAllocExcelPath,
                                              scheduleSubjectsGroupedResourceAllocExcelPath ]



##  5.1.8. OVERVIEW FOR RESOURCE ALLOCATION BY NUMBERS  ##

# For the classrooms in wide and vertical format, by the numbers
scheduleClassroomsWideAndVertOverviewByNumbersExcelPath = os.path.join(documentsOverviewsPath, scheduleClassroomsWideAndVertOverviewByNumbersExcelName)



##  5.1.9. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY NUMBERS  ##

# For the classrooms grouped overview for the resources vertically
scheduleClassroomsGroupedWideAndVertOverviewExcelPath =  os.path.join(documentsPrototypesPath, scheduleClassroomsGroupedWideAndVertOverviewByNumbersExcelName)



##  5.1.10. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes overview for the resource allocation by days
scheduleClassesResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesResourceAllocByDaysExcelName)
# For the teachers overview for the resource allocation by days
scheduleTeachersResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersResourceAllocByDaysExcelName)
# For the classrooms overview for the resource allocation by days
scheduleClassroomsResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsResourceAllocByDaysExcelName)
# For the subjects overview for the resource allocation by days
scheduleSubjectsResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsResourceAllocByDaysExcelName)

# For all of the above
allScheduleResourceAllocByDaysExcelPaths = [ scheduleClassesResourceAllocByDaysExcelPath,
                                             scheduleTeachersResourceAllocByDaysExcelPath,
                                             scheduleClassroomsResourceAllocByDaysExcelPath,
                                             scheduleSubjectsResourceAllocByDaysExcelPath ]



##  5.1.11. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes grouped overview for the resource allocation by days
scheduleClassesGroupedResourceAllocByDaysExcelPath = os.path.join(documentsOverviewsGroupedPath, scheduleClassesGroupedResourceAllocByDaysExcelName)
# For the teachers grouped overview for the resource allocation by days
scheduleTeachersGroupedResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleTeachersGroupedResourceAllocByDaysExcelName)
# For the classrooms grouped overview for the resource allocation by days
scheduleClassroomsGroupedResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleClassroomsGroupedResourceAllocByDaysExcelName)
# For the subjects grouped overview for the resource allocation by days
scheduleSubjectsGroupedResourceAllocByDaysExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleSubjectsGroupedResourceAllocByDaysExcelName)

# For all of the above
allScheduleGroupedResourceAllocByDaysExcelPaths = [ scheduleClassesGroupedResourceAllocByDaysExcelPath,
                                                    scheduleTeachersGroupedResourceAllocByDaysExcelPath,
                                                    scheduleClassroomsGroupedResourceAllocByDaysExcelPath,
                                                    scheduleSubjectsGroupedResourceAllocByDaysExcelPath ]


##  5.1.12. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes overview for the resource allocation by hours
scheduleClassesResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassesResourceAllocByHoursExcelName)
# For the teachers overview for the resource allocation by hours
scheduleTeachersResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleTeachersResourceAllocByHoursExcelName)
# For the classrooms overview for the resource allocation by hours
scheduleClassroomsResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleClassroomsResourceAllocByHoursExcelName)
# For the subjects overview for the resource allocation by hours
scheduleSubjectsResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsPath, scheduleSubjectsResourceAllocByHoursExcelName)

# For all of the above
allScheduleResourceAllocByHoursExcelPaths = [ scheduleClassesResourceAllocByHoursExcelPath,
                                              scheduleTeachersResourceAllocByHoursExcelPath,
                                              scheduleClassroomsResourceAllocByHoursExcelPath,
                                              scheduleSubjectsResourceAllocByHoursExcelPath ]



##  5.1.13. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes grouped overview for the resource allocation by hours
scheduleClassesGroupedResourceAllocByHoursExcelPath = os.path.join(documentsOverviewsGroupedPath, scheduleClassesGroupedResourceAllocByHoursExcelName)
# For the teachers grouped overview for the resource allocation by hours
scheduleTeachersGroupedResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleTeachersGroupedResourceAllocByHoursExcelName)
# For the classrooms grouped overview for the resource allocation by hours
scheduleClassroomsGroupedResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleClassroomsGroupedResourceAllocByHoursExcelName)
# For the subjects grouped overview for the resource allocation by hours
scheduleSubjectsGroupedResourceAllocByHoursExcelPath =  os.path.join(documentsOverviewsGroupedPath, scheduleSubjectsGroupedResourceAllocByHoursExcelName)

# For all of the above
allScheduleGroupedResourceAllocByHoursExcelPaths = [ scheduleClassesGroupedResourceAllocByHoursExcelPath,
                                                     scheduleTeachersGroupedResourceAllocByHoursExcelPath,
                                                     scheduleClassroomsGroupedResourceAllocByHoursExcelPath,
                                                     scheduleSubjectsGroupedResourceAllocByHoursExcelPath ]



###   5.2. JSON   ###

##  5.2.0 TEST  ##
testJSONPath = os.path.join(processingFilesJSONPath, testJSONName)



##  5.2.1 BASIC MAIN  ##

# For the pure scraped classes
scheduleClassesBaseJSONPath =  os.path.join(processingFilesJSONPath, scheduleClassesBaseJSONName)



## 5.2.2. BASIC EXTRA

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

# For all the schedules written in wide and vertical format
schedulesWideAndVertDfsJSONPath = os.path.join(processingFilesJSONPath, schedulesWideAndVertDfsJSONName)

# For the classrooms written in wide and vertical format
scheduleClassroomsWideAndVertDfsJSONPath = os.path.join(processingFilesJSONPath, scheduleClassroomsWideAndVertDfsJSONName)



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



##  5.3.5. OVERVIEW FOR RESOURCE ALLOCATION  ##

# For the classes overview for the resources
scheduleClassesResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassesResourceAllocDfsJSONName)
# For the teachers overview for the resources
scheduleTeachersResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleTeachersResourceAllocDfsJSONName)
# For the classrooms overview for the resources
scheduleClassroomsResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsResourceAllocDfsJSONName)
# For the subjects overview for the resources
scheduleSubjectsResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleSubjectsResourceAllocDfsJSONName)

# For all of the above
allScheduleResourceAllocDfsJSONPaths = [ scheduleClassesResourceAllocDfsJSONPath,
                                         scheduleTeachersResourceAllocDfsJSONPath,
                                         scheduleClassroomsResourceAllocDfsJSONPath,
                                         scheduleSubjectsResourceAllocDfsJSONPath ]



##  5.3.6. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION  ##

# For the classes grouped overview for the resources
scheduleClassesGroupedResourceAllocDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassesGroupedResourceAllocDfsJSONName)
# For the teachers grouped overview for the resources
scheduleTeachersGroupedResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleTeachersGroupedResourceAllocDfsJSONName)
# For the classrooms grouped overview for the resources
scheduleClassroomsGroupedResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedResourceAllocDfsJSONName)
# For the subjects grouped overview for the resources
scheduleSubjectsGroupedResourceAllocDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleSubjectsGroupedResourceAllocDfsJSONName)

# For all of the above
allScheduleGroupedResourceAllocDfsJSONPaths = [ scheduleClassesGroupedResourceAllocDfsJSONPath,
                                                scheduleTeachersGroupedResourceAllocDfsJSONPath,
                                                scheduleClassroomsGroupedResourceAllocDfsJSONPath,
                                                scheduleSubjectsGroupedResourceAllocDfsJSONPath ]



##  5.3.7. OVERVIEW FOR RESOURCE ALLOCATION BY NUMBERS  ##

scheduleClassroomsWideAndVertOverviewByNumbersDfsJSONPath = os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsWideAndVertOverviewByNumbersDfsJSONName)



##  5.3.8. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION  BY NUMBERS  ##

scheduleClassroomsGroupedWideAndVertOverviewByNumbersDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedWideAndVertOverviewByNumbersDfsJSONName)



##  5.3.9. OVERVIEW FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes overview for the resource allocation by days
scheduleClassesResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassesResourceAllocByDaysDfsJSONName)
# For the teachers overview for the resource allocation by days
scheduleTeachersResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleTeachersResourceAllocByDaysDfsJSONName)
# For the classrooms overview for the resource allocation by days
scheduleClassroomsResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsResourceAllocByDaysDfsJSONName)
# For the subjects overview for the resource allocation by days
scheduleSubjectsResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleSubjectsResourceAllocByDaysDfsJSONName)

# For all of the above
allScheduleResourceAllocByDaysDfsJSONPaths = [ scheduleClassesResourceAllocByDaysDfsJSONPath,
                                               scheduleTeachersResourceAllocByDaysDfsJSONPath,
                                               scheduleClassroomsResourceAllocByDaysDfsJSONPath,
                                               scheduleSubjectsResourceAllocByDaysDfsJSONPath ]



##  5.3.10. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY DAYS  ##

# For the classes grouped overview for the resource allocation by days
scheduleClassesGroupedResourceAllocByDaysDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassesGroupedResourceAllocByDaysDfsJSONName)
# For the teachers grouped overview for the resource allocation by days
scheduleTeachersGroupedResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleTeachersGroupedResourceAllocByDaysDfsJSONName)
# For the classrooms grouped overview for the resource allocation by days
scheduleClassroomsGroupedResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedResourceAllocByDaysDfsJSONName)
# For the subjects grouped overview for the resource allocation by days
scheduleSubjectsGroupedResourceAllocByDaysDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleSubjectsGroupedResourceAllocByDaysDfsJSONName)

# For all of the above
allScheduleGroupedResourceAllocByDaysDfsJSONPaths = [ scheduleClassesGroupedResourceAllocByDaysDfsJSONPath,
                                                      scheduleTeachersGroupedResourceAllocByDaysDfsJSONPath,
                                                      scheduleClassroomsGroupedResourceAllocByDaysDfsJSONPath,
                                                      scheduleSubjectsGroupedResourceAllocByDaysDfsJSONPath ]


##  5.3.11. OVERVIEW FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes overview for the resource allocation by hours
scheduleClassesResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassesResourceAllocByHoursDfsJSONName)
# For the teachers overview for the resource allocation by hours
scheduleTeachersResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleTeachersResourceAllocByHoursDfsJSONName)
# For the classrooms overview for the resource allocation by hours
scheduleClassroomsResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleClassroomsResourceAllocByHoursDfsJSONName)
# For the subjects overview for the resource allocation by hours
scheduleSubjectsResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsPath, scheduleSubjectsResourceAllocByHoursDfsJSONName)

# For all of the above
allScheduleResourceAllocByHoursDfsJSONPaths = [ scheduleClassesResourceAllocByHoursDfsJSONPath,
                                                scheduleTeachersResourceAllocByHoursDfsJSONPath,
                                                scheduleClassroomsResourceAllocByHoursDfsJSONPath,
                                                scheduleSubjectsResourceAllocByHoursDfsJSONPath ]



##  5.3.12. OVERVIEW [BASIC GROUPED] FOR RESOURCE ALLOCATION BY HOURS  ##

# For the classes grouped overview for the resource allocation by hours
scheduleClassesGroupedResourceAllocByHoursDfsJSONPath = os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassesGroupedResourceAllocByHoursDfsJSONName)
# For the teachers grouped overview for the resource allocation by hours
scheduleTeachersGroupedResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleTeachersGroupedResourceAllocByHoursDfsJSONName)
# For the classrooms grouped overview for the resource allocation by hours
scheduleClassroomsGroupedResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleClassroomsGroupedResourceAllocByHoursDfsJSONName)
# For the subjects grouped overview for the resource allocation by hours
scheduleSubjectsGroupedResourceAllocByHoursDfsJSONPath =  os.path.join(processingFilesJSONOverviewsGroupedPath, scheduleSubjectsGroupedResourceAllocByHoursDfsJSONName)

# For all of the above
allScheduleGroupedResourceAllocByHoursDfsJSONPaths = [ scheduleClassesGroupedResourceAllocByHoursDfsJSONPath,
                                                       scheduleTeachersGroupedResourceAllocByHoursDfsJSONPath,
                                                       scheduleClassroomsGroupedResourceAllocByHoursDfsJSONPath,
                                                       scheduleSubjectsGroupedResourceAllocByHoursDfsJSONPath ]