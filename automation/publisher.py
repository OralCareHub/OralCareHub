#!/usr/bin/env python3
"""
OralCareHub Multi-Platform Publisher
=====================================

Publish articles to ALL platforms with a single command.

Usage:
    python publisher.py ../content/articles/teeth-whitening-guide.md
    python publisher.py ../content/articles/*.md          # Publish all articles
    python publisher.py --platforms blogger,medium article.md  # Specific platforms only
    python publisher.py --dry-run article.md              # Preview without posting
    python publisher.py --list-platforms                   # Show configured platforms

Article format: Markdown files with YAML frontmatter (see content/templates/)
"""

import argparse
import json
import os
import sys
import glob
from datetime import datetime

import frontmatter
import markdown

# Lazy import platform modules — only load when actually used
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')
LOG_FILE = os.path.join(SCRIPT_DIR, 'publish_log.json')


def _get_platform_modules():
    """Lazy-load platform modules to avoid import errors for uninstalled deps."""
    from platforms import blogger, medium, tumblr, wordpress
    return {
        'blogger': blogger,
        'medium': medium,
        'tumblr': tumblr,
        'wordpress': wordpress,
    }


def load_config():
    """Load configuration from config.json."""
    if not os.path.exists(CONFIG_FILE):
        print("ERROR: config.json not found!")
        print("Copy config.example.json to config.json and fill in your API keys.")
        print(f"  cp {os.path.join(SCRIPT_DIR, 'config.example.json')} {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE) as f:
        return json.load(f)


def parse_article(filepath):
    """Parse a markdown article with frontmatter.

    Expected frontmatter:
        ---
        title: "Article Title"
        tags: [dental, whitening, tips]
        description: "SEO meta description"
        affiliate_link: "https://..."  (optional, overrides config)
        ---
    """
    post = frontmatter.load(filepath)

    title = post.get('title', 'Untitled')
    tags = post.get('tags', [])
    description = post.get('description', '')
    affiliate_link = post.get('affiliate_link', None)

    # Convert markdown body to HTML
    html_content = markdown.markdown(
        post.content,
        extensions=['extra', 'codehilite', 'toc']
    )

    return {
        'title': title,
        'tags': tags,
        'description': description,
        'affiliate_link': affiliate_link,
        'markdown': post.content,
        'html': html_content,
        'source_file': filepath
    }


def inject_branding(html_content, config, article):
    """Add OralCareHub branding, backlinks, and affiliate links to the article."""
    site_url = config['brand']['website_url']
    brand = config['brand']['name']
    affiliate = article.get('affiliate_link') or config['brand'].get('affiliate_link', '')

    # Footer with backlink to main site
    footer = f'''
    <hr>
    <p><strong>Want more dental health tips?</strong> Visit <a href="{site_url}" rel="nofollow">{brand}</a> for free guides, product reviews, and expert advice.</p>
    '''

    # Add affiliate CTA if link is provided
    if affiliate:
        footer += f'''
    <p>&#x1F449; <a href="{affiliate}" rel="nofollow"><strong>Check out our recommended products here</strong></a></p>
    '''

    return html_content + footer


def publish_article(article, config, platforms=None, dry_run=False):
    """Publish an article to all enabled platforms.

    Args:
        article: Parsed article dict
        config: Full config dict
        platforms: List of platform names to publish to (None = all enabled)
        dry_run: If True, just preview without posting

    Returns:
        dict of platform -> result
    """
    results = {}

    # Inject branding into HTML
    branded_html = inject_branding(article['html'], config, article)

    # Merge default tags with article tags
    all_tags = list(set(article['tags'] + config.get('seo', {}).get('default_tags', [])))

    platform_modules = _get_platform_modules()
    for platform_name, module in platform_modules.items():
        platform_config = config['platforms'].get(platform_name, {})

        # Skip disabled platforms
        if not platform_config.get('enabled', False):
            continue

        # Skip if not in requested platforms list
        if platforms and platform_name not in platforms:
            continue

        if dry_run:
            print(f"  [DRY RUN] Would publish to {platform_name}: \"{article['title']}\"")
            results[platform_name] = {'success': True, 'url': '[dry-run]', 'error': None}
            continue

        print(f"  Publishing to {platform_name}...", end=' ')

        result = module.publish(
            title=article['title'],
            html_content=branded_html,
            tags=all_tags,
            config=platform_config
        )

        if result['success']:
            print(f"OK -> {result['url']}")
        else:
            print(f"FAILED: {result['error']}")

        results[platform_name] = result

    return results


def log_publish(article, results):
    """Append publish results to the log file."""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'article': article['title'],
        'source': article['source_file'],
        'results': {}
    }

    for platform, result in results.items():
        log_entry['results'][platform] = {
            'success': result['success'],
            'url': result.get('url'),
            'error': result.get('error')
        }

    # Load existing log or create new
    log = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            log = json.load(f)

    log.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='OralCareHub Multi-Platform Publisher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python publisher.py ../content/articles/teeth-whitening.md
  python publisher.py ../content/articles/*.md
  python publisher.py --platforms blogger,tumblr article.md
  python publisher.py --dry-run article.md
  python publisher.py --list-platforms
        '''
    )
    parser.add_argument('articles', nargs='*', help='Markdown article file(s) to publish')
    parser.add_argument('--platforms', type=str, help='Comma-separated list of platforms')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')
    parser.add_argument('--list-platforms', action='store_true', help='List configured platforms')

    args = parser.parse_args()
    config = load_config()

    if args.list_platforms:
        print("\nConfigured platforms:")
        for name, pconfig in config['platforms'].items():
            status = "ENABLED" if pconfig.get('enabled') else "disabled"
            print(f"  {name}: {status}")
        return

    if not args.articles:
        parser.print_help()
        return

    # Expand glob patterns
    article_files = []
    for pattern in args.articles:
        article_files.extend(glob.glob(pattern))

    if not article_files:
        print("No article files found.")
        return

    platforms = args.platforms.split(',') if args.platforms else None

    print(f"\n{'='*50}")
    print(f"  OralCareHub Publisher")
    print(f"  Publishing {len(article_files)} article(s)")
    if args.dry_run:
        print(f"  MODE: DRY RUN")
    print(f"{'='*50}\n")

    for filepath in article_files:
        print(f"\nArticle: {os.path.basename(filepath)}")
        print(f"{'-'*40}")

        article = parse_article(filepath)
        print(f"  Title: {article['title']}")
        print(f"  Tags: {', '.join(article['tags'])}")
        print()

        results = publish_article(article, config, platforms, args.dry_run)

        if not args.dry_run:
            log_publish(article, results)

    # Summary
    print(f"\n{'='*50}")
    print("  Done! Check publish_log.json for full results.")
    print(f"{'='*50}\n")


if __name__ == '__main__':
    main()
