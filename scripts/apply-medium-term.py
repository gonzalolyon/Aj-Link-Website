#!/usr/bin/env python3
"""Apply medium-term SEO and performance fixes across AJ Link HTML pages."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = 'https://www.ajlink.com'
OG_IMAGE = f'{BASE_URL}/img/aj-link-hero-image-y.jpg'

ORG_JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "AJ Link Inc",
    "url": "https://www.ajlink.com/",
    "logo": "https://www.ajlink.com/img/AjLink_Logo.svg",
    "description": "Miami-based hotel and restaurant supplier with offices in Venezuela, Panama, Chile, Peru, and Colombia.",
    "telephone": "+1-305-461-0283",
    "email": "alejandro@ajlink.com",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "5975 Sunset Drive #506",
      "addressLocality": "South Miami",
      "addressRegion": "FL",
      "postalCode": "33143",
      "addressCountry": "US"
    },
    "sameAs": [
      "https://www.facebook.com/ajlink1",
      "https://twitter.com/AJLink7"
    ]
  }
  </script>'''

ORG_JSONLD_ES = ORG_JSONLD.replace(
    'Miami-based hotel and restaurant supplier with offices in Venezuela, Panama, Chile, Peru, and Colombia.',
    'Proveedor de equipos y productos para hoteles y restaurantes con oficinas en Miami, Venezuela, Panamá, Chile, Perú y Colombia.'
)


def page_url(filename):
    return f'{BASE_URL}/' if filename == 'index.html' else f'{BASE_URL}/{filename}'


def extract_meta(content, name):
    match = re.search(
        rf'<meta name="{re.escape(name)}" content="([^"]*)"',
        content,
        re.IGNORECASE,
    )
    return html.unescape(match.group(1)) if match else ''


def extract_title(content):
    match = re.search(r'<title>([^<]*)</title>', content, re.IGNORECASE)
    return html.unescape(match.group(1).strip()) if match else 'AJ Link'


def strip_existing_seo(content):
    content = re.sub(r'\s*<link rel="canonical"[^>]*>\n?', '', content)
    content = re.sub(r'\s*<meta property="og:[^"]+"[^>]*>\n?', '', content)
    content = re.sub(r'\s*<meta name="twitter:[^"]+"[^>]*>\n?', '', content)
    content = re.sub(
        r'\s*<script type="application/ld\+json">.*?</script>\n?',
        '',
        content,
        flags=re.DOTALL,
    )
    return content


def build_seo_block(filename, content):
    title = extract_title(content)
    description = extract_meta(content, 'description') or title
    url = page_url(filename)
    lang = 'es' if re.search(r'<html lang="es"', content) else 'en'
    locale = 'es_US' if lang == 'es' else 'en_US'

    block = f'''  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="AJ Link">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:locale" content="{locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{OG_IMAGE}">
'''

    if filename == 'index.html':
        block += ORG_JSONLD + '\n'
    elif filename == 'home-espanol.html':
        block += ORG_JSONLD_ES + '\n'

    return block


def inject_seo(content, filename):
    content = strip_existing_seo(content)
    seo = build_seo_block(filename, content)
    if re.search(r'<meta name="keywords"', content, re.IGNORECASE):
        return re.sub(
            r'(<meta name="keywords"[^>]*>\n?)',
            r'\1' + seo,
            content,
            count=1,
            flags=re.IGNORECASE,
        )
    if re.search(r'<meta name="description"', content, re.IGNORECASE):
        return re.sub(
            r'(<meta name="description"[^>]*>\n?)',
            r'\1' + seo,
            content,
            count=1,
            flags=re.IGNORECASE,
        )
    return re.sub(r'(</title>\n?)', r'\1\n' + seo, content, count=1)


def fix_hreflang(content):
    return content.replace('http://www.ajlink.com', BASE_URL)


def remove_jquery(content):
    content = re.sub(
        r'\s*<script src="https?://[^"]*jquery[^"]*\.js"></script>\n?',
        '',
        content,
        flags=re.IGNORECASE,
    )
    return content


def fix_external_targets(content):
    def repl(match):
        tag = match.group(0)
        if 'target="_blank"' in tag and 'rel=' in tag:
            return tag
        tag = re.sub(r'\s*target="https?://[^"]*"', '', tag)
        if 'target="_blank"' not in tag:
            tag = tag.replace('<a ', '<a target="_blank" rel="noopener noreferrer" ', 1)
        elif 'rel=' not in tag:
            tag = tag.replace('target="_blank"', 'target="_blank" rel="noopener noreferrer"')
        return tag

    return re.sub(r'<a\b[^>]*href="https?://[^"]*"[^>]*>', repl, content)


def update_site_map_footer_links(content):
    content = content.replace('>Website Site Map</a>', '>Sitemap</a>')
    content = content.replace('>Mapa Sitio Web</a>', '>Mapa del sitio</a>')
    content = re.sub(
        r'(<div><a href=")about\.html(">Sitemap</a></div>)',
        r'\1sitemap.xml\2',
        content,
    )
    content = re.sub(
        r'(<div><a href=")#(">Mapa del sitio</a></div>)',
        r'\1sitemap.xml\2',
        content,
    )
    return content


def process_file(path):
    text = path.read_text(encoding='utf-8')
    updated = text
    updated = fix_hreflang(updated)
    updated = inject_seo(updated, path.name)
    updated = remove_jquery(updated)
    updated = fix_external_targets(updated)
    updated = update_site_map_footer_links(updated)
    if updated != text:
        path.write_text(updated, encoding='utf-8')
        return True
    return False


def main():
    for path in sorted(ROOT.glob('*.html')):
        if path.name == '404-not-found.html':
            continue
        if process_file(path):
            print('updated', path.name)


if __name__ == '__main__':
    main()
