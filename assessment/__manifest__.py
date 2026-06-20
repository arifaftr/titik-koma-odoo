{
  'name': 'Assessment',
  'depends': ['website', 'survey', 'titikkoma'],
  'data': [
    'views/survey_custom.xml',
  ],
  'assets': {
    'web.assets_frontend': [
      'assessment/static/src/css/survey_custom.css',
      'assessment/static/src/js/tk_survey_likert.js',
    ],
    'web.assets_frontend_lazy': [
        'assessment/static/src/js/tk_survey_likert.js',
    ],
    'survey.survey_assets': [
        'assessment/static/src/js/tk_survey_likert.js',
    ],
  },
}