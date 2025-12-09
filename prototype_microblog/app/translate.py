import requests
from flask import current_app
from urllib.parse import quote


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
        # URL-encode language parameters to prevent injection
        url = ('https://api.cognitive.microsofttranslator.com/translate'
               '?api-version=3.0&from={}&to={}'.format(
                   quote(source_language, safe=''),
                   quote(dest_language, safe='')))
        
        r = requests.post(url, headers=auth, json=[{'Text': text}])
        
        if r.status_code != 200:
            return 'Error: the translation service failed.'
        
        # Parse and validate API response
        try:
            response_data = r.json()
        except ValueError:
            return 'Error: the translation service failed.'
        
        # Validate response structure
        if not _is_valid_translation_response(response_data):
            return 'Error: the translation service failed.'
        
        return response_data[0]['translations'][0]['text']
    except requests.exceptions.RequestException:
        return 'Error: the translation service failed.'


def _is_valid_translation_response(response_data):
    """Validate the structure of Microsoft Translator API response.
    
    Args:
        response_data: The parsed JSON response from the API
        
    Returns:
        True if response has expected structure, False otherwise
    """
    if not response_data or not isinstance(response_data, list):
        return False
    if len(response_data) == 0:
        return False
    if 'translations' not in response_data[0]:
        return False
    if not isinstance(response_data[0]['translations'], list):
        return False
    if len(response_data[0]['translations']) == 0:
        return False
    if 'text' not in response_data[0]['translations'][0]:
        return False
    return True
