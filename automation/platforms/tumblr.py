"""
Tumblr Platform Publisher
Posts articles to Tumblr via their API v2
"""

import pytumblr


def publish(title, html_content, tags, config):
    """Publish an article to Tumblr.

    Args:
        title: Article title
        html_content: Article body as HTML
        tags: List of tag strings
        config: Tumblr config dict with OAuth keys and blog_name

    Returns:
        dict with 'success', 'url', and 'error' keys
    """
    try:
        client = pytumblr.TumblrRestClient(
            config['consumer_key'],
            config['consumer_secret'],
            config['oauth_token'],
            config['oauth_secret']
        )

        blog_name = config['blog_name']

        result = client.create_text(
            blog_name,
            title=title,
            body=html_content,
            tags=tags,
            format='html'
        )

        # Tumblr returns {'id': <post_id>} on success
        if 'id' in result:
            post_id = result['id']
            url = f'https://{blog_name}.tumblr.com/post/{post_id}'
            return {
                'success': True,
                'url': url,
                'id': str(post_id),
                'error': None
            }
        else:
            return {
                'success': False,
                'url': None,
                'error': str(result)
            }

    except Exception as e:
        return {
            'success': False,
            'url': None,
            'error': str(e)
        }
