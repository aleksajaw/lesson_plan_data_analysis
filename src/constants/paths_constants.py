###   DIR PATHS   ###
import os
currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
projectRoot = os.path.dirname(srcDirPath)
#schedulePath = os.path.join(srcDirPath, 'schedules')
schedulePath = os.path.join(projectRoot, 'schedules')
scheduleJSONPath = os.path.join(schedulePath, 'json')
logsPath = os.path.join(projectRoot, 'logs')


###   FILE NAMES   ###
scheduleExcelClassesName = 'schedule_classes.xlsx'
scheduleExcelTeachersName = 'schedule_teachers.xlsx'
scheduleExcelClassroomsName = 'schedule_classrooms.xlsx'
scheduleExcelSubjectsName = 'schedule_subjects.xlsx'

scheduleListsExcelOwnersGroupedName = 'schedule-lists_owners-grouped.xlsx'

scheduleExcelClassesGroupedName = 'schedule_classes-grouped.xlsx'
scheduleExcelTeachersGroupedName = 'schedule_teachers-grouped.xlsx'
scheduleExcelClassroomsGroupedName = 'schedule_classrooms-grouped.xlsx'
scheduleExcelSubjectsGroupedName = 'schedule_subjects-grouped.xlsx'

scheduleClassesBaseJSONName = 'base_schedule_classes.json'

scheduleListsOwnersGroupedJSONName = 'dfs_schedule-lists_owners-grouped.json'

scheduleClassesGroupedJSONName = 'dfs_schedule_classes-grouped.json'
scheduleTeachersGroupedJSONName = 'dfs_schedule_teachers-grouped.json'
scheduleClassroomsGroupedJSONName = 'dfs_schedule_classrooms-grouped.json'
scheduleSubjectsGroupedJSONName = 'dfs_schedule_subjects-grouped.json'

scheduleClassesDfsJSONName = 'dfs_schedule_classes.json'
scheduleTeachersDfsJSONName = 'dfs_schedule_teachers.json'
scheduleClassroomsDfsJSONName = 'dfs_schedule_classrooms.json'
scheduleSubjectsDfsJSONName = 'dfs_schedule_subjects.json'

scheduleExcelClassesJSONName = 'dfs_schedule-excel_classes.json'


###   FILE PATHS   ###
# Excel
# For classes
scheduleExcelClassesPath = os.path.join(schedulePath, scheduleExcelClassesName)
# For teachers
scheduleExcelTeachersPath =  os.path.join(schedulePath, scheduleExcelTeachersName)
# For classrooms
scheduleExcelClassroomsPath =  os.path.join(schedulePath, scheduleExcelClassroomsName)
# For subjects
scheduleExcelSubjectsPath =  os.path.join(schedulePath, scheduleExcelSubjectsName)


# For schedule lists with grouped owners
scheduleListsExcelOwnersGroupedPath =  os.path.join(schedulePath, scheduleListsExcelOwnersGroupedName)

# For classes grouped
scheduleExcelClassesGroupedPath =  os.path.join(schedulePath, scheduleExcelClassesGroupedName)
# For teachers grouped
scheduleExcelTeachersGroupedPath =  os.path.join(schedulePath, scheduleExcelTeachersGroupedName)
# For classrooms grouped
scheduleExcelClassroomsGroupedPath =  os.path.join(schedulePath, scheduleExcelClassroomsGroupedName)
# For subjects grouped
scheduleExcelSubjectsGroupedPath =  os.path.join(schedulePath, scheduleExcelSubjectsGroupedName)


###   JSON   ###
# Pure scraped classes
scheduleClassesBaseJSONPath =  os.path.join(scheduleJSONPath, scheduleClassesBaseJSONName)


# JSON with Data Frames
# For schedule lists with grouped owners
scheduleListsOwnersGroupedJSONPath =  os.path.join(scheduleJSONPath, scheduleListsOwnersGroupedJSONName)

# For classes grouped
scheduleClassesGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassesGroupedJSONName)
# For teachers grouped
scheduleTeachersGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersGroupedJSONName)
# For classrooms grouped
scheduleClassroomsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsGroupedJSONName)
# For subjects grouped
scheduleSubjectsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsGroupedJSONName)


# For classes
scheduleClassesDfsJSONPath =  os.path.join(scheduleJSONPath, scheduleClassesDfsJSONName)
# For teachers
scheduleTeachersDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersDfsJSONName)
# For classrooms
scheduleClassroomsDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsDfsJSONName)
# For subjects
scheduleSubjectsDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsDfsJSONName)


# Data read from the current basic Excel
scheduleExcelClassesDfsJSONPath =  os.path.join(scheduleJSONPath, scheduleExcelClassesJSONName)