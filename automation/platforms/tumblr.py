"""
Tumblr Platform Publisher
Posts articles to Tumblr via their API v2
"""


def publish(title, html_content, tags, config):
    """Publish an article to Tumblr."""
    try:
        import pytumblr
    except ImportError:
        return {
            'success': False,
            'url': None,
            'error': 'pytumblr not installed. Run: pip3 install pytumblr'
        }

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
