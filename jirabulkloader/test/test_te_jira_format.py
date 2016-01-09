
def test_jira_format_Simple_case(te):
    input_dict = {'parent': 'DRY-RUN-XXXX', 'markup': '#',
                  'summary': 'sub-task', 'assignee': 'assignee',
                  'issuetype': 'Sub-task'}
    expected_result = {'parent': {'key': 'DRY-RUN-XXXX'}, 'summary': 'sub-task',
                       'assignee':  {'name': 'assignee'},
                       'issuetype': {'name': 'Sub-task'}}
    assert te.jira_format(input_dict) == expected_result


def test_jira_format_if_additional_fields_provided(te):
    te.default_params = {'project': {'key': 'TestProject'},
                         'item1': ['subitem1', 'subitem2']}
    input_dict = {'parent': 'DRY-RUN-XXXX', 'markup': '#',
                  'summary': 'sub-task', 'assignee': 'assignee',
                  'issuetype': 'Sub-task'}
    expected_result = {'parent': {'key': 'DRY-RUN-XXXX'}, 'summary': 'sub-task',
                       'project': {'key': 'TestProject'},
                       'assignee': {'name': 'assignee'},
                       'issuetype': {'name': 'Sub-task'},
                       'item1': ['subitem1', 'subitem2']}
    assert te.jira_format(input_dict) == expected_result


def test_jira_format_Replaces_default_params_by_tmpl_json(te):
    te.default_params = {'project': {'key': 'TestProject'},
                         'duedate': '2012-03-01', 'item1': 'default_value'}
    input_json = {'duedate': '2012-04-01', 'issuetype': 'Task',
                  'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task',
                  'tmpl_ext': {'item1': 'template_value'}}
    expected_result = {'summary': 'h5 task', 'project': {'key': 'TestProject'},
                       'duedate': '2012-04-01',
                       'assignee': {'name': 'assignee'},
                       'issuetype': {'name': 'Task'},
                       'item1': 'template_value'}
    assert te.jira_format(input_json) == expected_result
