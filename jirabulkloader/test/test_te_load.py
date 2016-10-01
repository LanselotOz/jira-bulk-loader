import pytest


def test_load(te, std_te_input, std_te_tasks):
    assert te.load(std_te_input) == std_te_tasks


@pytest.fixture
def existing_h4_input():
    return ".. JIRA-1234\n# test subtask *assignee*\nh5. h5 task *assignee*"


def test_load_existing_h4_task(te, existing_h4_input):
    assert te.load(existing_h4_input) == \
        [{'markup': '..', 'issue_key': 'JIRA-1234', 'line_number': 1},
         {'assignee': 'assignee', 'line_number': 2,
          'markup': '#', 'summary': 'test subtask'},
         {'assignee': 'assignee', 'line_number': 3,
          'markup': 'h5.', 'summary': 'h5 task'}]


def test_load_Check_dueDate_and_JSON_in_one_line(te):
    input_text = ('h5. h5 task1 *assignee* %2012-04-01% {"item2":"test2"}\n'
                  'h5. h5 task2 *assignee*')
    expected_result = \
        [{'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task1',
          'duedate': '2012-04-01', 'tmpl_ext': {"item2": "test2"},
          'line_number': 1},
         {'assignee': 'assignee', 'markup': 'h5.',
          'summary': 'h5 task2', 'line_number': 2}]
    assert te.load(input_text) == expected_result


def test_load_Check_JSON_inline(te):
    input_text = ('{"item1":{"name":"test"}}\n'
                  'h5. h5 task *assignee* {"item2": {"name": "test2"}}')
    expected_result = \
        [{'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task',
          'line_number': 2, 'tmpl_ext': {"item1": {"name": "test"},
                                         "item2": {"name": "test2"}}}]
    assert te.load(input_text) == expected_result


def test_load_Check_JSON_inline_replacement(te):
    input_text = ('{"item1":{"name":"test"}}\n{"item2":"test2"}\n'
                  'h5. h5 task *assignee* {"item1":"test1"}\n'
                  '#* Sub-task 1 *assignee*')
    expected_result = \
        [{'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task',
          'line_number': 3, 'tmpl_ext': {"item1": "test1", "item2": "test2"}},
         {'assignee': 'assignee', 'markup': '#*', 'summary': 'Sub-task 1',
          'line_number': 4,
          'tmpl_ext': {"item1": {"name": "test"}, "item2": "test2"}}]
    assert te.load(input_text) == expected_result
