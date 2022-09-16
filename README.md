# SuperAdmin3000
Further documentation can be found [here](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/main/docs/docs.md).
## Starting the application
- Activate poetry environment: `poetry install`
- Start flask: `poetry run invoke start`
- Or start Poetry shell first and run Flask from within the environment:
```
$ poetry shell
$ invoke start
```
- Go to http://127.0.0.1:5000/

## Definition of done

The definition of done for sprint 1 or until the minimum viable product (MVP) has been developed is as follows:
- The source code is peer reviewed and linted
- The source code is deployed onto the ‘master’ branch 
- The source code is unit tested with a code coverage of 70%

Sprint 2 / MVP onwards:

Every developer commits to creating unit tests and E2E-tests using robot framework (when applicable) before deployment. The deployed code should be documented. Also all code submitted to the main branch should be peer reviewed utilising pull requests. The automated tests should reach a code coverage of 75%. 