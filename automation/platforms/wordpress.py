"""
WordPress.com Platform Publisher
Posts articles to WordPress.com via REST API v1.1
"""

import requests


WP_API_BASE = 'https://public-api.wordpress.com/rest/v1.1'


def publish(title, html_content, tags, config):
    """Publish an article to WordPress.com.

    Args:
        title: Article title
        html_content: Article body as HTML
        tags: List of tag strings
        config: WordPress config dict with site, username, password

    Returns:
        dict with 'success', 'url', and 'error' keys
    """
    try:
        site = config['site']

        payload = {
            'title': title,
            'content': html_content,
            'tags': ','.join(tags),
            'status': 'publish',
            'format': 'standard'
        }

        resp = requests.post(
            f'{WP_API_BASE}/sites/{site}/posts/new',
            auth=(config['username'], config['password']),
            data=payload
        )
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
