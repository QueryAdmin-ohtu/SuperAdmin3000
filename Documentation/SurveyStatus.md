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

## Determining the status
The status of the survey is contained in a dictionary, which is passed as an argument to the Jinja2 template that renders the survey page.
```
status_color  : (str) 'red','yellow' or 'green',
no_survey_results : (bool),
no_categories : (bool),
unrelated_categories_in_weights : (list) [category names]
no_questions : (bool),
questions_without_answers :(list) [question names],
questions_without_categories :(list) [category names],
categories_without_questions : (list) [category names]
categories_without_results :  (dictionary) {question_id: [category names]}
```
The dictionary is assembled in the check_survey_status function in [survey_service.py](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/3e6c0caf64de3bf337e260a6d7a547a18536b129/src/services/survey_service.py#L441). The status of a survey is determined in the check_survey_status function in [survey_repository.py](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/a004c2eb812b48fa52feee4da2c3ea18f569f7e5/src/repositories/survey_repository.py#L1056). 
