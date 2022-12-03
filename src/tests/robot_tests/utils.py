def parse_survey_id_from_url(url):
    return url.rsplit('/', 1)[-1]
