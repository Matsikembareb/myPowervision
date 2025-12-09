import requests
from flask_babel import _
from flask import has_request_context
from app import app

def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
        if has_request_context():
            return _('Error: the translation service is not configured.')
        return 'Error: the translation service is not configured.'
    
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'southafricanorth',
        'Content-Type': 'application/json'
    }

    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[{'Text': text}])
    if r.status_code != 200:
        if has_request_context():
            return _('Error: the translation service failed.')
        return 'Error: the translation service failed.'
    return r.json()[0]['translations'][0]['text']