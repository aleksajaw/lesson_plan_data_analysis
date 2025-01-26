import os



#####     DIR PATHS     #####

currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
projectRoot = os.path.dirname(srcDirPath)

#schedulePath = os.path.join(srcDirPath, 'schedules')
schedulePath = os.path.join(projectRoot, 'schedules')
scheduleJSONPath = os.path.join(schedulePath, 'json')

logsPath = os.path.join(projectRoot, 'logs')



#####     PARTS OF FILE NAMES AND PATHS     #####

extExcel = '.xlsx'
extJSON = '.json' 
dfsPrefix = 'dfs_'
groupedSufix = '-grouped'
overviewSufix = '_overview'



#####     FILE BASE NAMES     #####

# For classes
scheduleClassesBaseName = 'schedule_classes'
# For teachers
scheduleTeachersBaseName = 'schedule_teachers'
# For classrooms
scheduleClassroomsBaseName = 'schedule_classrooms'
# For subjects
scheduleSubjectsBaseName = 'schedule_subjects'

# For all of the above
scheduleFileBaseNames = [ scheduleClassesBaseName,
                          scheduleTeachersBaseName,
                          scheduleClassroomsBaseName,
                          scheduleSubjectsBaseName ]


# For classes grouped
scheduleClassesGroupedBaseName = scheduleClassesBaseName + groupedSufix
# For teachers grouped
scheduleTeachersGroupedBaseName = scheduleTeachersBaseName + groupedSufix
# For classrooms grouped
scheduleClassroomsGroupedBaseName = scheduleClassroomsBaseName + groupedSufix
# For subjects grouped
scheduleSubjectsGroupedBaseName = scheduleSubjectsBaseName + groupedSufix

# For all of the above 
scheduleFileGroupedBaseNames = [ scheduleClassesGroupedBaseName,
                                 scheduleTeachersGroupedBaseName,
                                 scheduleClassroomsGroupedBaseName,
                                 scheduleSubjectsGroupedBaseName ]


# For classes overview
scheduleClassesOverviewBaseName = scheduleClassesBaseName + overviewSufix
# For teachers overview
scheduleTeachersOverviewBaseName = scheduleTeachersBaseName + overviewSufix
# For classrooms overview
scheduleClassroomsOverviewBaseName = scheduleClassroomsBaseName + overviewSufix
# For subjects overview
scheduleSubjectsOverviewBaseName = scheduleSubjectsBaseName +  overviewSufix

# For all of the above 
scheduleFileGroupedOverviewBaseNames = [ scheduleClassesOverviewBaseName,
                                         scheduleTeachersOverviewBaseName,
                                         scheduleClassroomsOverviewBaseName,
                                         scheduleSubjectsOverviewBaseName ]


# For classes grouped overview
scheduleClassesGroupedOverviewBaseName = scheduleClassesBaseName + groupedSufix + overviewSufix
# For teachers grouped overview
scheduleTeachersGroupedOverviewBaseName = scheduleTeachersBaseName + groupedSufix + overviewSufix
# For classrooms grouped overview
scheduleClassroomsGroupedOverviewBaseName = scheduleClassroomsBaseName + groupedSufix + overviewSufix
# For subjects grouped overview
scheduleSubjectsGroupedOverviewBaseName = scheduleSubjectsBaseName + groupedSufix + overviewSufix

# For all of the above 
scheduleFileGroupedOverviewBaseNames = [ scheduleClassesGroupedOverviewBaseName,
                                         scheduleTeachersGroupedOverviewBaseName,
                                         scheduleClassroomsGroupedOverviewBaseName,
                                         scheduleSubjectsGroupedOverviewBaseName ]



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
scheduleExcelClassesGroupedName = scheduleClassesGroupedBaseName + extExcel
# For the teachers grouped
scheduleExcelTeachersGroupedName = scheduleTeachersGroupedBaseName + extExcel
# For the classrooms grouped
scheduleExcelClassroomsGroupedName = scheduleClassroomsGroupedBaseName + extExcel
# For the subjects grouped
scheduleExcelSubjectsGroupedName = scheduleSubjectsGroupedBaseName + extExcel


# For the classes overview
scheduleExcelClassesOverviewName = scheduleClassesOverviewBaseName + extExcel
# For the teachers overview
scheduleExcelTeachersOverviewName = scheduleTeachersOverviewBaseName + extExcel
# For the classrooms overview
scheduleExcelClassroomsOverviewName = scheduleClassroomsOverviewBaseName + extExcel
# For the subjects overview
scheduleExcelSubjectsOverviewName = scheduleSubjectsOverviewBaseName + extExcel


# For the classes grouped overview
scheduleExcelClassesGroupedOverviewName = scheduleClassesGroupedOverviewBaseName + extExcel
# For the teachers grouped overview
scheduleExcelTeachersGroupedOverviewName = scheduleTeachersGroupedOverviewBaseName + extExcel
# For the classrooms grouped overview
scheduleExcelClassroomsGroupedOverviewName = scheduleClassroomsGroupedOverviewBaseName + extExcel
# For the subjects grouped overview
scheduleExcelSubjectsGroupedOverviewName = scheduleSubjectsGroupedOverviewBaseName + extExcel



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
allScheduleDfsJSONNames = [ scheduleClassesDfsJSONName,
                            scheduleTeachersDfsJSONName,
                            scheduleClassroomsDfsJSONName,
                            scheduleSubjectsDfsJSONName ]


# For the list of the schedule owners
scheduleListsOwnersGroupedDfsJSONName = dfsPrefix + 'schedule-lists_owners' + groupedSufix + extJSON

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
allScheduleExcelPath = [ #scheduleExcelClassesPath,
                         scheduleExcelTeachersPath,
                         scheduleExcelClassroomsPath,
                         scheduleExcelSubjectsPath ]


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
allScheduleExcelGroupedPath = [ #scheduleExcelClassesGroupedPath,
                                scheduleExcelTeachersGroupedPath,
                                scheduleExcelClassroomsGroupedPath,
                                scheduleExcelSubjectsGroupedPath ]


# For the classes overview
scheduleExcelClassesOverviewPath = os.path.join(schedulePath, scheduleExcelClassesOverviewName)
# For the teachers overview
scheduleExcelTeachersOverviewPath =  os.path.join(schedulePath, scheduleExcelTeachersOverviewName)
# For the classrooms overview
scheduleExcelClassroomsOverviewPath =  os.path.join(schedulePath, scheduleExcelClassroomsOverviewName)
# For the subjects overview
scheduleExcelSubjectsOverviewPath =  os.path.join(schedulePath, scheduleExcelSubjectsOverviewName)

# For all of the above
allScheduleExcelOverviewPath = [ scheduleExcelClassesOverviewPath,
                                 scheduleExcelTeachersOverviewPath,
                                 scheduleExcelClassroomsOverviewPath,
                                 scheduleExcelSubjectsOverviewPath ]


# For the classes grouped overview
scheduleExcelClassesGroupedOverviewPath =  os.path.join(schedulePath, scheduleExcelClassesGroupedOverviewName)
# For the teachers grouped overview
scheduleExcelTeachersGroupedOverviewPath =  os.path.join(schedulePath, scheduleExcelTeachersGroupedOverviewName)
# For the classrooms grouped overview
scheduleExcelClassroomsGroupedOverviewPath =  os.path.join(schedulePath, scheduleExcelClassroomsGroupedOverviewName)
# For the subjects grouped overview
scheduleExcelSubjectsGroupedOverviewPath =  os.path.join(schedulePath, scheduleExcelSubjectsGroupedOverviewName)

# For all of the above
allScheduleExcelGroupedOverviewPath = [ scheduleExcelClassesGroupedOverviewPath,
                                        scheduleExcelTeachersGroupedOverviewPath,
                                        scheduleExcelClassroomsGroupedOverviewPath,
                                        scheduleExcelSubjectsGroupedOverviewPath ]


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
allScheduleDfsJSONPath = [ scheduleClassesDfsJSONPath,
                           scheduleTeachersDfsJSONPath,
                           scheduleClassroomsDfsJSONPath,
                           scheduleSubjectsDfsJSONPath ]


# For the classes grouped
scheduleClassesGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassesGroupedDfsJSONName)
# For the teachers grouped
scheduleTeachersGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersGroupedDfsJSONName)
# For the classrooms grouped
scheduleClassroomsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsGroupedDfsJSONName)
# For the subjects grouped
scheduleSubjectsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsGroupedDfsJSONName)

# For all of the above
allScheduleGroupedDfsJSONPath = [ #scheduleClassesGroupedDfsJSONPath,
                                  scheduleTeachersGroupedDfsJSONPath,
                                  scheduleClassroomsGroupedDfsJSONPath,
                                  scheduleSubjectsGroupedDfsJSONPath ]