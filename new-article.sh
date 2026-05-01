#!/bin/bash
# ==============================================================
# OralCareHub - Create a new article from template
#
# Usage:
#   bash new-article.sh "best toothpaste for sensitive teeth" review
#   bash new-article.sh "how to floss properly" howto
#   bash new-article.sh "10 dental myths debunked" list
# ==============================================================

TITLE="$1"
TYPE="${2:-howto}"  # Default to how-to guide

if [ -z "$TITLE" ]; then
    echo "Usage: bash new-article.sh \"article title\" [review|howto|list]"
    echo ""
    echo "Templates:"
    echo "  review  - Product review / comparison"
    echo "  howto   - How-to guide / tutorial"
    echo "  list    - Listicle (X things that...)"
    exit 1
fi

# Generate filename from title
FILENAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

# Count existing articles for numbering
COUNT=$(ls content/articles/*.md 2>/dev/null | wc -l | tr -d ' ')
NUM=$(printf "%02d" $((COUNT + 1)))

FILEPATH="content/articles/${NUM}-${FILENAME}.md"

# Pick template
case "$TYPE" in
    review)  TEMPLATE="content/templates/product-review.md" ;;
    howto)   TEMPLATE="content/templates/how-to-guide.md" ;;
    list)    TEMPLATE="content/templates/listicle.md" ;;
    *)       TEMPLATE="content/templates/how-to-guide.md" ;;
esac

cp "$TEMPLATE" "$FILEPATH"

echo "Created: $FILEPATH"
echo "Template: $TYPE"
echo ""
echo "Next steps:"
echo "  1. Edit the article: nano $FILEPATH"
echo "  2. Publish it:       bash publish.sh ${NUM}-${FILENAME}.md"
