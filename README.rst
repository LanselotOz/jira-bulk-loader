Introduction
============

I used to waste hours cloning tasks in JIRA, editing their summaries, description and etc. Step by step I came to the idea that I need a template of my frequently used tasks so that I can re-create them very easy and effortless.

The key idea of jira-bulk-loader is an activity template.

The template is written in human language with a few markup rules. jira-bulk-loader.py uses the prepared template to create the corresponding set of tasks in less than one minute.



Installation
============

Download and install using pip:

    pip install jira-bulk-loader



Very simple case
================

Template:

    | 	h5. First task summary \*assignee\*
    |	=description line 1
    | 	=description line 2
    |
    | 	h5. Second task summary \*assignee\*
    | 	=description line 3
    | 	=description line 4

command: 

	./jira-bulk-loader.py -U <your_username> -P <your_password> -H jira.your_domain.org -W PRKEY template_file

two tasks will be created and assigned to *assignee* in the project with a project key *PRKEY*.



One more simple case
====================

Template:

    | 	h5. Task summary \*assignee\*
    |	=description line 1
    | 	=description line 2
    |
    | 	# First sub-task summary \*assignee1\* 
    | 	=description line 3
    |
    |	# Second sub-task summary \*assignee2\* %2012-09-18%
    | 	=description line 3

and the command:

	./jira-bulk-loader.py -U <your_username> -P <your_password> -H jira.your_domain.org -D 2012-09-20 -W PRKEY template_file

It will create a task with two subtasks. Moreover it also sets due date 2012-09-18 (YYYY-mm-DD) to 2nd sub-task, and 2012-09-20 to the task and its first sub-task.



Dry run option
==============

jira-bulk-loader.py has an option *--dry*. If it is specified in command line, jira-bulk-loader checks template syntax, verifies project name and assignees but doesn't create tasks.

I would strongly recommend using it every time.



User story and 'included in' tasks
==================================

Sometime an activity is too complex and it is much easier and appropriate to create several tasks with sub-tasks and link them to a user story.

    | 	h4. User story summary \*assignee\*
    |	=description
    |
    | 	h5. First task summary \*assignee1\*
    |	=description
    | 	# Sub-task summary \*assignee1\* 
    | 	=description
    |
    | 	h5. Second task summary \*assignee2\*
    |	=description
    | 	# Sub-task summary \*assignee2\* 
    | 	=description

In this case h5 tasks will be linked to h4 user story.



A short summary
===============

Let me summarize what are the possible markups to begin a line with:

- a user story: h4. summary \*assignee\*
- a task: h5. summary \*assignee\*
- a sub-task: # summary \*assignee\*  
- one more sub-task: #* summary \*assignee\*
- description: = 



Task parameters
===============

It is possible to define task attributes in template:

    |	{"project":{"key":"PRKEY"}
    |	{"priority": {"name": "High"}}
    |	{"duedate": "2012-09-20"}
    |	{"components": [{"name": "Production"}]}
    |
    | 	h5. First task summary \*assignee1\*
    |	=description
    |
    | 	h5. Second task summary \*assignee2\* {"components": [{"name": "Localizations"}]}
    |	=description
    |
    | 	h5. Third task summary \*assignee3\*
    |	=description

It the example *project*, *priority* and *duedate* will be applied to both tasks by default. The *component* 'Production' will be applied to task 1 and 3. However, the second task will use the *component* 'Localizations'.

`This part <http://docs.atlassian.com/jira/REST/latest/#id200060>`_ of Jira documentation could give a clue how to find out relevant parameters in your project and their format.



Template variables
==================

    |	[REVISION=194567]
    |	[QA=John]
    |
    | 	h5. First task summary \*$QA\*
    |	=description $REVISION
    |
    | 	h5. Second task summary \*$QA\*
    |	=description $REVISION

is equivalent to 

    | 	h5. First task summary \*John\*
    |	=description 194567
    |
    | 	h5. Second task summary \*John\*
    |	=description 194567

the important difference is that you don't need to change assignee or description of each task in your template. You change variable value instead and it is applied to every line in the template. 



Issues and new ideas
====================

If you found an issue or if you have an idea of improvement please visit `http://bitbucket.org/oktopuz/jira-bulk-loader/issues <http://bitbucket.org/oktopuz/jira-bulk-loader/issues>`_


