"""
Blogger Platform Publisher
Posts articles to Google Blogger via API v3
"""

import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'blogger_token.json')


def get_credentials(credentials_file):
    """Get or refresh Google API credentials."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def publish(title, html_content, tags, config):
    """Publish an article to Blogger.

    Args:
        title: Article title
        html_content: Article body as HTML
        tags: List of tag strings
        config: Blogger config dict with blog_id and credentials_file

    Returns:
        dict with 'success', 'url', and 'error' keys
    """
    try:
        creds = get_credentials(config['credentials_file'])
        service = build('blogger', 'v3', credentials=creds)

        body = {
            'kind': 'blogger#post',
            'title': title,
            'content': html_content,
            'labels': tags
        }

        post = service.posts().insert(
            blogId=config['blog_id'],
            body=body,
            isDraft=False
        ).execute()

        return {
            'success': True,
            'url': post.get('url', ''),
            'id': post.get('id', ''),
            'error': None
        }

    except Exception as e:
        return {
            'success': False,
            'url': None,
            'error': str(e)
        }
