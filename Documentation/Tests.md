# Tests and style
To access the poetry shell, run the following command in the project root folder:
```
$ poetry shell
```
Any commands described in this document should be run in the poetry shell enviroment.

## Unit tests

Pytest library is used, and the tests can be run by giving the following command:

```
invoke tests
```

Alternatively use the following command to first reset the database, then run the unit tests:
```
invoke reset-and-test <localdb>
```

**Test coverage**

The following files are unit tested:

- src/db.py
- src/helper.py
- src/logger/logger.py
- src/repositories/statistic_repository.py
- src/repositories/survey_repository.py
- src/services/statistic_service.py
- src/services/survey_service.py


Test coverage data can be collected with command:

```
invoke coverage
```

Aftere the data has been collected, HTML and XML reports
can be produced with commands:

```
invoke coveragehtml
```

The `index.html`file can be found in the `htmlcov` subdirectory.

```
invoke coveragexml
```

The coverage report can be produced with one combined command:
```
invoke coverage && invoke coveragehtml
```

The XML file appears in the project root directory.



## End-to-end tests
Robot framework is used for end-to-end testing. The tests cover common use case scenarios such as survey creation, removal and updates, visual feedback (checking survey status), logging in, viewing statistics and so forth.

Tests can be run with the following command:

```
invoke e2etests
```

Alternatively use the following command to first reset the database, then run the end to end tests:
```
invoke reset-and-e2etests <localdb>
```
The test report and log files are generated in the project root as `/log.html` and `/report.html`

![robotohtu](https://user-images.githubusercontent.com/80696138/192254326-f192158d-99ad-4af5-a527-cb3d6305585c.png)


## Style checks
Pylint is used for style checking. Usage:

```
invoke lint
```

## Automatic style corrections
Autopep8 can be used for automatic style corrections. Usage:

```
invoke format
```

# Note for further development
In the earlier stages of the development process, the developer team did not always properly consider that the tests should be atomic (i.e. cleanly executed and torn down while not dependent on other tests). We took steps to correct our testing procedures, but decided that rewriting the tests would be too costly of an operation in terms of working hours. This might lead to maintenance issues later on.
