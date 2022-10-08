# Tests and style

## Unit tests

Pytest library is used, and the tests can be run by giving a command in
the Poetry shell:

```
invoke tests
```

## Test coverage

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



## Style checks
- Pylint is used fo style checking
- From Poetry shell give a command:

```
invoke lint
```

## Automatic style corrections
- Autopep8
- From Poetry shell give a command:

```
invoke format
```

## End-to-end tests
- Robot framework 
- From Poetry shell give a command:

```
invoke e2etests
```

![robotohtu](https://user-images.githubusercontent.com/80696138/192254326-f192158d-99ad-4af5-a527-cb3d6305585c.png)
