# Survey status
Surveys are complex and feature many different fields of information. To ensure that users create surveys that work in the survey application, Super Admin 3000 features a survey status functionality. Each survey has a status. The status can be one of the following three:

### All Good (green)
The survey will function correctly in the survey application

### Warning (yellow
The warning status indicates that the survey has some defects. The survey will not break the survey application, but the defects should be addressed. Warning status is displayed when:
- There are questions that do not affect any category
- There are categories that do not affect any question

### Attention required (red)
The attention required status indicates that there is a critical error in a survey. The survey will not function in the survey application, and it could possibly break the application. Attention required status is displayed when:
- The survey has no survey results
- There are categories without category results
- The survey has no questions
- The survey has questions with no answers
- The survey has no categories
- The questions of the survey have category weights that cannot be found in the categories table. Category weights are stored as JSON data in the questions table. See [database diagram](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/main/Documentation/ER-diagram.pdf) for more info. This problem should not be possible in the later versions of Super Admin 3000.

## Modifying the conditions of statuses
The status of a survey is determined in the check_survey_function in [survey_repository.py](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/a004c2eb812b48fa52feee4da2c3ea18f569f7e5/src/repositories/survey_repository.py#L1056). 
