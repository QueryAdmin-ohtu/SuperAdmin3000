# SuperAdmin3000

[App on Heroku](https://superadmin3000.herokuapp.com/)

Further documentation can be found [here](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/main/docs/docs.md).

[![codecov](https://codecov.io/gh/QueryAdmin-ohtu/SuperAdmin3000/branch/main/graph/badge.svg?token=N3ODFPVKZB)](https://codecov.io/gh/QueryAdmin-ohtu/SuperAdmin3000)

## Starting the application
- Activate poetry environment: `poetry install`
- Start flask: `poetry run invoke start`
- Or start Poetry shell first and run Flask from within the environment:
```
$ poetry shell
$ invoke start
```

To generate `requirements.txt` file for Heroku deployment, run from with in Poetry shell:
```
pip list --format freeze > requirements.txt
```

- Go to http://localhost:5000/

## Definition of done

Every developer commits to creating unit tests and E2E-tests using robot framework (when applicable) before deployment. The deployed code should be documented. Also all code submitted to the main branch should be peer reviewed utilising pull requests. The automated tests should reach a code coverage of 75%. 

## Documentation and diagrams

* [Architecture](Documentation/Architecture.md)
* [Backend API](Documentation/BackendAPI.md)
* [Deployment](Documentation/Deployment.md)
* [Design](Documentation/DesignDocument.png)
* [ER diagram](Documentation/ER-diagram.pdf)
* [Functional scope](Documentation/FunctionalScope.md)
* [Structure](Documentation/Structure.pdf)
* [Survey status](Documentation/SurveyStatus.md)
* [Testing](Documentation/Tests.md)
* [Restlist](Documentation/RestList.md)
* [Tooltips](Documentation/Tooltips.md)
* [User guide](Documentation/UserGuide.md)

_* Original `.dia` files have been created with the [Dia](https://wiki.gnome.org/Apps/Dia/) software and can be found in the Documents folder._

