"""
WordPress.com Platform Publisher
Posts articles to WordPress.com via REST API v1.1 using OAuth2 bearer token.
"""

import requests


WP_API_BASE = 'https://public-api.wordpress.com/rest/v1.1'


def publish(title, html_content, tags, config):
    """Publish an article to WordPress.com.

    Args:
        title: Article title
        html_content: Article body as HTML
        tags: List of tag strings
        config: WordPress config dict with site and access_token

    Returns:
        dict with 'success', 'url', and 'error' keys
    """
    try:
        site = config['site']
        token = config['access_token']

        payload = {
            'title': title,
            'content': html_content,
            'tags': ','.join(tags),
            'status': 'publish',
            'format': 'standard'
        }

        resp = requests.post(
            f'{WP_API_BASE}/sites/{site}/posts/new',
            headers={'Authorization': f'Bearer {token}'},
            data=payload
        )
        if resp.status_code == 401:
            return {
                'success': False,
                'url': None,
                'error': 'Access token expired or invalid — re-run the OAuth2 flow'
            }
        resp.raise_for_status()
        data = resp.json()

        return {
            'success': True,
            'url': data.get('URL', ''),
            'id': str(data.get('ID', '')),
            'error': None
        }

    except Exception as e:
        return {
            'success': False,
            'url': None,
            'error': str(e)
        }
