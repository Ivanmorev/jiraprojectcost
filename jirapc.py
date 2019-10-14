from jira import JIRA
import pandas as pd
from pandas import ExcelWriter
from openpyxl import load_workbook
import configparser


path = "configuration.ini"
config = configparser.ConfigParser()
config.read(path)
result_slug = str(config.get("DEFAULT", "result_slug"))
data_path = str(config.get("DEFAULT", "data_path"))
jql = str(config.get("DEFAULT", "jql"))
workbook_path = str(config.get("DEFAULT", "workbook_path"))
jira_url = str(config.get("DEFAULT", "jira_url"))
login = str(config.get("DEFAULT", "login"))
password = str(config.get("DEFAULT", "password"))

workbook_full_path =  workbook_path

workbook = load_workbook(filename = workbook_full_path)
sheet = workbook.active

values = sheet.values
salarydf = pd.DataFrame(values)
salarydf = pd.DataFrame(salarydf.values, columns = ["assigneeuser", "salary_user"])
salarydf.set_index("assigneeuser",inplace=True)
salarydf["salary_per_hour"] = salarydf["salary_user"]/160
print('Salary per user:')
print(salarydf)

allissues = []


print("Connecting to jira, jql filter is", jql)




# Defines a function for connecting to Jira
def connect_jira(jira_server, jira_user, jira_password):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        print("Connecting to JIRA: %s" % jira_server)
        jira_options = {'server': jira_server}
        jira = JIRA(options=jira_options, basic_auth=(jira_user, jira_password))
                                        # ^--- Note the tuple
        return jira
    except Exception:
        print("Failed to connect to JIRA: %s" % e)
        return None

jira = connect_jira(jira_url,login , password)
issues = jira.search_issues(jql)

for issue in issues:
   allissues.append(issue)
print ('Tasks found:', len(allissues))

issues = pd.DataFrame()
for issue in allissues:
     issue = jira.issue(issue.key)
     WorkLog = jira.worklogs(issue)
     if len(WorkLog) > 0:
         for i in range(len(WorkLog)):
             d = {
              'assigneeuser': str(issue.fields.assignee.name),
              'timespent': WorkLog[i].timeSpentSeconds / 3600
             }
             issues = issues.append(d, ignore_index=True)
issues.set_index('assigneeuser',inplace=True)
grouped = issues.groupby('assigneeuser').mean()
print('Time spent per user:')
print(grouped)
df_merge = pd.merge(salarydf, grouped, on="assigneeuser")
df_merge['summ'] = df_merge['salary_per_hour'] * df_merge['timespent']
print(df_merge)

TaskCost = round(df_merge['summ'].sum(axis = 0, skipna = True))
print('Task cost is',TaskCost, 'rur')

new_path = data_path + '-tasks-'+result_slug+'.xlsx'
writer = ExcelWriter(new_path)
df_merge.to_excel(writer,'jiratasks', index=False, engine='xlsxwriter')
writer.save()
print('Saved to', new_path)
