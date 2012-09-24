#!/usr/bin/python
#-*- coding: UTF-8 -*-

import argparse
from jirabulkloader.task_extractor import TaskExtractor
from jirabulkloader.task_extractor_exceptions import TaskExtractorTemplateErrorProject, TaskExtractorJiraValidationError, TaskExtractorTemplateErrorJson, TaskExtractorJiraCreationError
from requests.exceptions import ConnectionError

prg_description="""Uses template file to create many tasks in Jira at once.
For more information about template format please visit http://bitbucket.org/oktopuz/jira-bulk-loader"""

parser = argparse.ArgumentParser(description=prg_description, formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('template_file', type=argparse.FileType('rU'), help='file containing tasks definition')
parser.add_argument('-W', dest='project', help='Project key')
parser.add_argument('-R', dest='priority', help='Task priority. "Medium" by default', default="Medium")
parser.add_argument('-D', dest='dueDate', help='dueDate  (YYYY-mm-DD). For example: 2012-05-31')
parser.add_argument('--dry', dest='dry_run', action='store_true', help='Make a dry run. It checks everything but does not create tasks', default=False)

mandatory = parser.add_argument_group('mandatory arguments')
mandatory.add_argument('-H', dest='hostname', required=True, help='Jira hostname. Without http://')
mandatory.add_argument('-U', dest='username', required=True, help='your Jira username')
mandatory.add_argument('-P', dest='password', required=True, help='your Jira password')

args = parser.parse_args()


##############################################################
# open input file, parse and create tasks

input_text = args.template_file.read()

options = {}
if args.dueDate: options['duedate'] = args.dueDate
if args.priority: options['priority'] = {'name':args.priority}
if args.project: options['project'] = {'key':args.project}

jira_url = "http://" + args.hostname

task_ext = TaskExtractor(jira_url, args.username, args.password, options, dry_run = args.dry_run)

try:
    print "Parsing task list.."
    tasks =  task_ext.load(input_text)

    print "Validating tasks.."
    task_ext.validate_load(tasks)

    print "Creating tasks.."
    breakdown = task_ext.create_tasks(tasks)
except TaskExtractorTemplateErrorProject, e:
    print e.message
    exit(1)
except TaskExtractorJiraValidationError, e:
    print e.message
    exit(1)
except TaskExtractorJiraCreationError, e:
    print e.message
    exit(1)
except TaskExtractorTemplateErrorJson, e:
    print "ERROR: The following line in template is not valid:", e.error_element
    print "A correct JSON structure expected."
    exit(1)

print '===  The following structure will be created ===' + '\n\n' + breakdown

print "\nDone."

