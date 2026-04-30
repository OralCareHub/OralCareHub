"""
Medium Platform Publisher
Posts articles to Medium via their Publishing API
"""

import requests


MEDIUM_API_BASE = 'https://api.medium.com/v1'


def _get_user_id(token):
    """Get the authenticated user's Medium ID."""
    resp = requests.get(
        f'{MEDIUM_API_BASE}/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    resp.raise_for_status()
    return resp.json()['data']['id']


def publish(title, html_content, tags, config):
    """Publish an article to Medium.

    Args:
        title: Article title
        html_content: Article body as HTML
        tags: List of tag strings (Medium allows max 5)
        config: Medium config dict with integration_token

    Returns:
        dict with 'success', 'url', and 'error' keys
    """
    try:
        token = config['integration_token']
        user_id = _get_user_id(token)

        # Medium allows max 5 tags
        post_tags = tags[:5]

        payload = {
            'title': title,
            'contentFormat': 'html',
            'content': html_content,
            'tags': post_tags,
            'publishStatus': 'public'
        }

        resp = requests.post(
            f'{MEDIUM_API_BASE}/users/{user_id}/posts',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json=payload
        )
        resp.raise_for_status()
        data = resp.json()['data']

        return {
            'success': True,
            'url': data.get('url', ''),
            'id': data.get('id', ''),
            'error': None
        }

    except Exception as e:
        return {
            'success': False,
            'url': None,
            'error': str(e)
        }
