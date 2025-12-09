import requests
from flask_babel import _
from flask import has_request_context
from app import app
import time


def translate(text, source_language, dest_language):
    """Translate text with retry logic for transient network failures."""
    if 'MS_TRANSLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
        if has_request_context():
            return _('Error: the translation service is not configured.')
        return 'Error: the translation service is not configured.'
    
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'southafricanorth',
        'Content-Type': 'application/json'
    }
    
    max_retries = 3
    retry_delay = 1  # Start with 1 second delay
    
    for attempt in range(max_retries):
        try:
            r = requests.post(
                'https://api.cognitive.microsofttranslator.com'
                '/translate?api-version=3.0&from={}&to={}'.format(
                    source_language, dest_language), 
                headers=auth, 
                json=[{'Text': text}],
                timeout=10  # Add timeout to prevent hanging
            )
            
            if r.status_code == 200:
                return r.json()[0]['translations'][0]['text']
            elif r.status_code >= 500:
                # Server error - retry
                app.logger.warning(
                    f'Translation API server error (attempt {attempt + 1}/{max_retries}): '
                    f'Status {r.status_code}'
                )
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    if has_request_context():
                        return _('Error: the translation service failed.')
                    return 'Error: the translation service failed.'
            else:
                # Client error (4xx) - don't retry
                app.logger.error(f'Translation API client error: Status {r.status_code}')
                if has_request_context():
                    return _('Error: the translation service failed.')
                return 'Error: the translation service failed.'
                
        except requests.exceptions.Timeout:
            app.logger.warning(
                f'Translation API timeout (attempt {attempt + 1}/{max_retries})'
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                if has_request_context():
                    return _('Error: the translation service failed.')
                return 'Error: the translation service failed.'
        except requests.exceptions.RequestException as e:
            app.logger.warning(
                f'Translation API request error (attempt {attempt + 1}/{max_retries}): {str(e)}'
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                if has_request_context():
                    return _('Error: the translation service failed.')
                return 'Error: the translation service failed.'
    
    # Fallback return in case loop completes without returning
    if has_request_context():
        return _('Error: the translation service failed.')
    return 'Error: the translation service failed.'