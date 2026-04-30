# OralCareHub - Complete Setup Guide

Everything you need to go from zero to publishing across multiple platforms.

## Project Structure

```
OralCareHub/
├── site/                  # Your website (deploy this folder)
│   ├── index.html         # Landing page
│   ├── blog/              # Article pages
│   ├── reviews/           # Product review pages
│   ├── resources/         # Free guides (with content lockers)
│   ├── css/style.css      # Styling
│   └── js/main.js         # Content locker logic
├── automation/            # Auto-publisher scripts
│   ├── publisher.py       # Main script - publishes to ALL platforms
│   ├── platforms/         # Platform-specific modules
│   ├── config.json        # Your API keys (DO NOT share)
│   └── publish_log.json   # Log of everything published
├── content/
│   ├── articles/          # Ready-to-publish articles (.md)
│   ├── templates/         # Article templates to create new content
│   └── keywords.csv       # Target keywords database
└── SETUP.md               # This file
```

---

## STEP 1: Deploy Your Website (Free)

Your website is a static HTML site — no server needed. Deploy it for free on Netlify:

### Option A: Netlify (Recommended)

1. Go to https://app.netlify.com
2. Sign up with email (no personal info required — use your brand email)
3. Click "Add new site" > "Deploy manually"
4. Drag and drop the `site/` folder onto the page
5. Done! You get a URL like `random-name.netlify.app`
6. (Optional) Click "Domain settings" > "Change site name" to `oralcarehub.netlify.app`

### Option B: Vercel

1. Go to https://vercel.com
2. Sign up, import the `site/` folder
3. Deploy — you get `oralcarehub.vercel.app`

### Option C: GitHub Pages (most anonymous)

1. Create a GitHub account (use brand email)
2. Create a new repository called `oralcarehub`
3. Upload the contents of the `site/` folder
4. Go to Settings > Pages > Source: main branch
5. Your site is at `username.github.io/oralcarehub`

### Custom Domain (Optional, ~$10/year)

Buy a domain like `oralcarehub.com` from Namecheap or Porkbun (cheapest).
Point it to your Netlify/Vercel/GitHub Pages site. This looks more professional.

---

## STEP 2: Set Up MyLead Affiliate Links

1. Log into https://pub.mylead.global/dashboard
2. Go to **Affiliate Programs** > Browse by category
3. Apply to programs in: **Health**, **Beauty**, **E-commerce**
4. Once approved, get your affiliate links
5. Replace the `href="#"` placeholder links in:
   - `site/reviews/index.html` — product "Check Price" buttons
   - `site/blog/teeth-whitening-guide.html` — affiliate boxes
   - `site/index.html` — top picks section

### Setting Up Content Lockers

1. In MyLead dashboard, go to **Tools** > **Content Locker**
2. Create a new CPA Locker
3. Copy the locker URL
4. In `site/resources/index.html`, replace `data-locker-url="#"` with your locker URL
5. Now every time someone "unlocks" a resource, you earn money

---

## STEP 3: Create Platform Accounts (One-Time)

Create anonymous accounts on each platform. Use your brand name "OralCareHub" everywhere.

### Blogger (Google)
1. Go to https://www.blogger.com
2. Sign in with a Google account (create a new one for the brand)
3. Create a new blog: "OralCareHub"
4. Note your Blog ID (visible in the URL when you're on the blog dashboard)
5. For API access:
   - Go to https://console.cloud.google.com
   - Create a new project
   - Enable "Blogger API v3"
   - Create OAuth 2.0 credentials (Desktop app)
   - Download the JSON file to `automation/credentials/blogger_credentials.json`

### Medium
1. Go to https://medium.com — sign up with email
2. Set display name to "OralCareHub"
3. Go to Settings > Security and applications > Integration tokens
4. Generate a token and save it

### Tumblr
1. Go to https://www.tumblr.com — sign up
2. Create a blog named "oralcarehub"
3. Go to https://www.tumblr.com/oauth/apps
4. Register a new application
5. Get your Consumer Key, Consumer Secret, OAuth Token, OAuth Secret

### WordPress.com
1. Go to https://wordpress.com — create a free account
2. Create a site: "oralcarehub.wordpress.com"
3. Go to https://wordpress.com/me/security/two-step
4. At the bottom, create an Application Password
5. Save the username and app password

---

## STEP 4: Configure the Auto-Publisher

1. Install Python dependencies:
```bash
cd automation
pip install -r requirements.txt
```

2. Create your config file:
```bash
cp config.example.json config.json
```

3. Edit `config.json` with your API keys from Step 3:
```bash
nano config.json   # or open with any text editor
```

4. Fill in all the fields with your actual credentials.

---

## STEP 5: Publish Your First Article

### Test with a dry run first:
```bash
cd automation
python publisher.py --dry-run ../content/articles/01-teeth-whitening-complete-guide.md
```

### Publish to all platforms:
```bash
python publisher.py ../content/articles/01-teeth-whitening-complete-guide.md
```

### Publish to specific platforms only:
```bash
python publisher.py --platforms blogger,medium ../content/articles/01-teeth-whitening-complete-guide.md
```

### Publish ALL articles at once:
```bash
python publisher.py ../content/articles/*.md
```

### Check what platforms are configured:
```bash
python publisher.py --list-platforms
```

---

## STEP 6: Create New Articles

### Using templates:
1. Open a template from `content/templates/` (product-review, how-to-guide, or listicle)
2. Copy it to `content/articles/` with a descriptive filename
3. Fill in the brackets with your content
4. Update the frontmatter (title, tags, description)
5. Publish with `python publisher.py`

### Using keywords.csv:
1. Open `content/keywords.csv`
2. Pick a keyword with status "todo"
3. Note the recommended template
4. Write the article using that template
5. Update the status to "written"
6. Publish

### Article frontmatter format:
```yaml
---
title: "Your Article Title"
tags: [tag1, tag2, tag3]
description: "SEO meta description under 160 characters"
affiliate_link: "https://your-specific-mylead-link"
---

Article content in markdown here...
```

---

## STEP 7: Daily Workflow

### The 30-minute daily routine:

1. **Write or edit 1 article** (15 min)
   - Use a template from `content/templates/`
   - Pick a keyword from `keywords.csv`
   - Add your MyLead affiliate link in the frontmatter

2. **Publish to all platforms** (1 min)
   ```bash
   python publisher.py content/articles/your-new-article.md
   ```

3. **Share on Pinterest** (10 min)
   - Create a pin with a dental tip related to your article
   - Link the pin to your article on your website
   - Use relevant keywords in the pin description

4. **Check MyLead dashboard** (4 min)
   - See if any conversions came in
   - Check which programs are performing
   - Adjust your article topics toward what converts

---

## Tips for Staying Anonymous

- Never use your real name anywhere — always "OralCareHub" or "OralCareHub Team"
- Use a separate email for all brand accounts (ProtonMail is free and private)
- Don't link any personal social media
- Use a VPN if you want extra privacy
- Pay for domain with crypto if you want maximum anonymity
- All platform accounts should use the brand name and brand email

---

## Scaling Up

Once you're making consistent income:

1. **More articles** = more search traffic = more affiliate clicks
2. **More platforms** = wider reach (add Pinterest, Reddit, Quora)
3. **Better keywords** = target higher-volume terms from keywords.csv
4. **Content lockers** = passive income from your resources page
5. **Email list** = add a newsletter signup to capture repeat visitors

The system compounds: every article you publish keeps earning money forever as long as it ranks. After 50+ articles across all platforms, you'll have a traffic machine running on autopilot.
