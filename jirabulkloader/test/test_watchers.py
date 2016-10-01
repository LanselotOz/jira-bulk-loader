from mock import MagicMock, call


def test_load_watcher(te_real, issue, dry_run_key):
    input_text = ('h5. h5 task1 *assignee* %2016-10-01% +watcher_1+\n'
                  'h5. h5 task2 *assignee*')
    expected_load_result = \
        [{'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task1',
          'duedate': '2016-10-01', 'watchers': ['watcher_1'],
          'line_number': 1},
         {'assignee': 'assignee', 'markup': 'h5.',
          'summary': 'h5 task2', 'line_number': 2}]
    expected_result = ("h5. h5 task1 ({0})\n"
                       "h5. h5 task2 ({0})").format(dry_run_key)

    assert te_real.load(input_text) == expected_load_result
    te_real.jira.add_watcher = MagicMock()
    assert te_real.create_tasks(expected_load_result) == expected_result
    te_real.jira.add_watcher.assert_called_once_with(issue, 'watcher_1')
    assert te_real.jira.create_issue.called is True


def test_load_multiple_watchers(te_real, issue, dry_run_key):
    input_text = ('h5. h5 task1 *assignee* +watcher1+ '
                  '%2016-10-02% +watcher2+\n'
                  'h5. h5 task2 *assignee* +watcher3+')
    expected_load_result = \
        [{'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task1',
          'duedate': '2016-10-02', 'watchers': ['watcher1', 'watcher2'],
          'line_number': 1},
         {'assignee': 'assignee', 'markup': 'h5.',
          'summary': 'h5 task2', 'watchers': ['watcher3'], 'line_number': 2}]
    expected_result = ("h5. h5 task1 ({0})\n"
                       "h5. h5 task2 ({0})").format(dry_run_key)

    assert te_real.load(input_text) == expected_load_result
    te_real.jira.add_watcher = MagicMock()
    assert te_real.create_tasks(expected_load_result) == expected_result
    assert te_real.jira.add_watcher.mock_calls == [call(issue, 'watcher1'),
                                                   call(issue, 'watcher2'),
                                                   call(issue, 'watcher3')]
    assert te_real.jira.create_issue.called is True
