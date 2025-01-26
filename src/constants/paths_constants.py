import os



#####     DIR PATHS     #####

currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
projectRoot = os.path.dirname(srcDirPath)

#schedulePath = os.path.join(srcDirPath, 'schedules')
schedulePath = os.path.join(projectRoot, 'schedules')
scheduleJSONPath = os.path.join(schedulePath, 'json')

logsPath = os.path.join(projectRoot, 'logs')



#####     FILE BASE NAMES     #####

scheduleClassesBaseName = 'schedule_classes'
scheduleTeachersBaseName = 'schedule_teachers'
scheduleClassroomsBaseName = 'schedule_classrooms'
scheduleSubjectsBaseName = 'schedule_subjects'

scheduleFileBaseNames = [ scheduleClassesBaseName,
                          scheduleTeachersBaseName,
                          scheduleClassroomsBaseName,
                          scheduleSubjectsBaseName ]



#####     PARTS OF FILE NAMES AND PATHS     #####

extExcel = '.xlsx'
extJSON = '.json' 
dfsPrefix = 'dfs_'
groupedSufix = '-grouped'



#####     FILE NAMES     #####


###   Excel   ###

# For the classes
scheduleExcelClassesName = scheduleClassesBaseName + extExcel
# For the teachers
scheduleExcelTeachersName = scheduleTeachersBaseName + extExcel
# For the classrooms
scheduleExcelClassroomsName = scheduleClassroomsBaseName + extExcel
# For the subjects
scheduleExcelSubjectsName = scheduleSubjectsBaseName + extExcel

# For the lists of schedule owners
scheduleListsExcelOwnersGroupedName = 'schedule-lists_owners' + groupedSufix + extExcel


# For the classes grouped
scheduleExcelClassesGroupedName = scheduleClassesBaseName + groupedSufix + extExcel
# For the teachers grouped
scheduleExcelTeachersGroupedName = scheduleTeachersBaseName + groupedSufix + extExcel
# For the classrooms grouped
scheduleExcelClassroomsGroupedName = scheduleClassroomsBaseName + groupedSufix + extExcel
# For the subjects grouped
scheduleExcelSubjectsGroupedName = scheduleSubjectsBaseName + groupedSufix + extExcel



###   JSON   ###

# For the scraped classes data, base for other files
scheduleClassesBaseJSONName = 'base_' + scheduleClassesBaseName + extJSON



###   JSON with Data Frames   ###

# For the classes read from Excel
scheduleExcelClassesJSONName = dfsPrefix + 'schedule-excel_classes' + extJSON

# For the classes
scheduleClassesDfsJSONName = dfsPrefix + scheduleClassesBaseName + extJSON
# For the teachers
scheduleTeachersDfsJSONName = dfsPrefix + scheduleTeachersBaseName + extJSON
# For the classrooms
scheduleClassroomsDfsJSONName = dfsPrefix + scheduleClassroomsBaseName + extJSON
# For the subjects
scheduleSubjectsDfsJSONName = dfsPrefix + scheduleSubjectsBaseName + extJSON

# For all of the above
allScheduleDfsJSONNames = [
                            scheduleClassesDfsJSONName,
                            scheduleTeachersDfsJSONName,
                            scheduleClassroomsDfsJSONName,
                            scheduleSubjectsDfsJSONName
                          ]


# For the list of the schedule owners
scheduleListsOwnersGroupedDfsJSONName = dfsPrefix + 'schedule-lists_owners' + groupedSufix + extJSON

# For the classes grouped
scheduleClassesGroupedDfsJSONName = dfsPrefix + scheduleClassesBaseName + '' + groupedSufix + extJSON
# For the teachers grouped
scheduleTeachersGroupedDfsJSONName = dfsPrefix + scheduleTeachersBaseName + '' + groupedSufix + extJSON
# For the classrooms grouped
scheduleClassroomsGroupedDfsJSONName = dfsPrefix + scheduleClassroomsBaseName + '' + groupedSufix + extJSON
# For the subjects grouped
scheduleSubjectsGroupedDfsJSONName = dfsPrefix + scheduleSubjectsBaseName + '' + groupedSufix + extJSON

# For all of the above
allScheduleGroupedDfsJSONNames = [
                                   scheduleClassesGroupedDfsJSONName,
                                   scheduleTeachersGroupedDfsJSONName,
                                   scheduleClassroomsGroupedDfsJSONName,
                                   scheduleSubjectsGroupedDfsJSONName
                                 ]




#####     FILE PATHS     #####


###    Excel   ###

# For the classes
scheduleExcelClassesPath = os.path.join(schedulePath, scheduleExcelClassesName)
# For the teachers
scheduleExcelTeachersPath =  os.path.join(schedulePath, scheduleExcelTeachersName)
# For the classrooms
scheduleExcelClassroomsPath =  os.path.join(schedulePath, scheduleExcelClassroomsName)
# For the subjects
scheduleExcelSubjectsPath =  os.path.join(schedulePath, scheduleExcelSubjectsName)

# For all of the above
allScheduleExcelPath = [
                         #scheduleExcelClassesPath,
                         scheduleExcelTeachersPath,
                         scheduleExcelClassroomsPath,
                         scheduleExcelSubjectsPath
                       ]


# For schedule lists with grouped owners
scheduleListsExcelOwnersGroupedPath =  os.path.join(schedulePath, scheduleListsExcelOwnersGroupedName)

# For the classes grouped
scheduleExcelClassesGroupedPath =  os.path.join(schedulePath, scheduleExcelClassesGroupedName)
# For the teachers grouped
scheduleExcelTeachersGroupedPath =  os.path.join(schedulePath, scheduleExcelTeachersGroupedName)
# For the classrooms grouped
scheduleExcelClassroomsGroupedPath =  os.path.join(schedulePath, scheduleExcelClassroomsGroupedName)
# For the subjects grouped
scheduleExcelSubjectsGroupedPath =  os.path.join(schedulePath, scheduleExcelSubjectsGroupedName)

# For all of the above
allScheduleExcelGroupedPath = [ 
                                #scheduleExcelClassesGroupedPath,
                                scheduleExcelTeachersGroupedPath,
                                scheduleExcelClassroomsGroupedPath,
                                scheduleExcelSubjectsGroupedPath
                              ]



###   JSON   ###

# For the pure scraped classes
scheduleClassesBaseJSONPath =  os.path.join(scheduleJSONPath, scheduleClassesBaseJSONName)

# For the schedule lists with the grouped owners
scheduleListsOwnersGroupedJSONPath =  os.path.join(scheduleJSONPath, scheduleListsOwnersGroupedDfsJSONName)



###   JSON with Data Frames   ###

# For the content of the current main (basic) Excel
scheduleExcelClassesDfsJSONPath =  os.path.join(scheduleJSONPath, scheduleExcelClassesJSONName)


# For the classes
scheduleClassesDfsJSONPath =  os.path.join(scheduleJSONPath, scheduleClassesDfsJSONName)
# For the teachers
scheduleTeachersDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersDfsJSONName)
# For the classrooms
scheduleClassroomsDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsDfsJSONName)
# For the subjects
scheduleSubjectsDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsDfsJSONName)

# For all of the above
allScheduleDfsJSONPath = [
                           scheduleClassesDfsJSONPath,
                           scheduleTeachersDfsJSONPath,
                           scheduleClassroomsDfsJSONPath,
                           scheduleSubjectsDfsJSONPath
                         ]


# For the classes grouped
scheduleClassesGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassesGroupedDfsJSONName)
# For the teachers grouped
scheduleTeachersGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersGroupedDfsJSONName)
# For the classrooms grouped
scheduleClassroomsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsGroupedDfsJSONName)
# For the subjects grouped
scheduleSubjectsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsGroupedDfsJSONName)

# For all of the above
allScheduleGroupedDfsJSONPath = [
                                  #scheduleClassesGroupedDfsJSONPath,
                                  scheduleTeachersGroupedDfsJSONPath,
                                  scheduleClassroomsGroupedDfsJSONPath,
                                  scheduleSubjectsGroupedDfsJSONPath
                                ]