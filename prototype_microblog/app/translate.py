import requests
from flask import current_app


def translate(text, source_language, dest_language):
    """Translate text from source_language to dest_language using Microsoft Translator API.
    
    Args:
        text: The text to translate
        source_language: Source language code (e.g., 'en')
        dest_language: Destination language code (e.g., 'es')
        
    Returns:
        Translated text or error message
    """
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return 'Error: the translation service is not configured.'
    
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': current_app.config.get('MS_TRANSLATOR_REGION', 'global'),
        'Content-Type': 'application/json'
    }
    
    try:
        r = requests.post(
            'https://api.cognitive.microsofttranslator.com/translate'
            '?api-version=3.0&from={}&to={}'.format(source_language, dest_language),
            headers=auth,
            json=[{'Text': text}]
        )
        
        if r.status_code != 200:
            return 'Error: the translation service failed.'
        
        response_data = r.json()
        if (not response_data or not isinstance(response_data, list) or
                len(response_data) == 0 or 'translations' not in response_data[0] or
                len(response_data[0]['translations']) == 0 or
                'text' not in response_data[0]['translations'][0]):
            return 'Error: the translation service failed.'
        
        return response_data[0]['translations'][0]['text']
    except (requests.exceptions.RequestException, ValueError, KeyError, IndexError):
        return 'Error: the translation service failed.'
