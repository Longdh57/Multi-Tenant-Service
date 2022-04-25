## Testing

### Config Environment
- In folder /tests, copy env.example to .env, add value for JIRA_USER and JIRA_PASSWORD

- Create one test file with one API, test file must start with test_...

- Create class inheritance APITestCase like
```
class TestGetDepartmentListAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-283"
```

### Testing Command 

* Testing
```
$ pytest
```

* Testing with path
```
$ pytest tests/path/to/test


# Example: test everything in folder role_title
$ pytest tests/api/role_title

# Example: test file test_role_title_list.py
$ pytest tests/api/role_title/test_role_title_list.py
```

* Test submit to Jira
```
$ pytest tests/path/to/test --submit-tests
```

**Important: Don't submit all test to Jira in a command** (don't run `pytest --submit-tests`)
