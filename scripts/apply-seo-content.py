#!/usr/bin/env python3
"""Apply SEO and content fixes across AJ Link HTML pages."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = 'https://www.ajlink.com'

PAGE_PAIRS = {
    'index.html': 'home-espanol.html',
    'about.html': 'quienes-somos.html',
    'products.html': 'productos.html',
    'services.html': 'servicios.html',
    'contact.html': 'contactos.html',
    'food-beverage.html': 'alimentos-bebidas.html',
    'banquet-and-convention.html': 'banquete-convenciones.html',
    'furniture-supplies.html': 'muebles.html',
    'green-supplies.html': 'ecologicos.html',
    'kitchen-equipment.html': 'cocina.html',
    'laundry-equipment.html': 'lavanderia.html',
    'room-supplies.html': 'habitacion.html',
    'software-hotel-management.html': 'software-hotelero.html',
}

SPANISH_PAGES = set(PAGE_PAIRS.values())

CATALOG_PAGES = {
    'food-beverage.html': ('Products', 'Food & Beverage'),
    'banquet-and-convention.html': ('Products', 'Banquet & Convention'),
    'furniture-supplies.html': ('Products', 'Furniture Supplies'),
    'green-supplies.html': ('Products', 'Green Supplies'),
    'kitchen-equipment.html': ('Products', 'Kitchen Equipment'),
    'laundry-equipment.html': ('Products', 'Laundry Equipment'),
    'room-supplies.html': ('Products', 'Room Supplies'),
    'software-hotel-management.html': ('Products', 'Software Hotel Management'),
    'alimentos-bebidas.html': ('Productos', 'Alimentos y Bebidas'),
    'banquete-convenciones.html': ('Productos', 'Banquete y Convenciones'),
    'muebles.html': ('Productos', 'Muebles'),
    'ecologicos.html': ('Productos', 'Ecológicos'),
    'cocina.html': ('Productos', 'Cocina'),
    'lavanderia.html': ('Productos', 'Lavandería'),
    'habitacion.html': ('Productos', 'Habitación'),
    'software-hotelero.html': ('Productos', 'Software Hotelero'),
}

TITLE_FIXES = {
    'green-supplies.html': 'Green Supplies - AJ Link Hotel Suppliers',
    'kitchen-equipment.html': 'Kitchen Equipment - AJ Link Hotel Suppliers',
    'products.html': 'Products - AJ Link Hotel Suppliers',
    'alimentos-bebidas.html': 'Alimentos y Bebidas - AJ Link Suplidores Hoteleros',
    'banquete-convenciones.html': 'Banquete y Convenciones - AJ Link Suplidores Hoteleros',
    'cocina.html': 'Cocina - AJ Link Suplidores Hoteleros',
    'ecologicos.html': 'Ecológicos - AJ Link Suplidores Hoteleros',
    'habitacion.html': 'Habitación - AJ Link Suplidores Hoteleros',
    'lavanderia.html': 'Lavandería - AJ Link Suplidores Hoteleros',
    'muebles.html': 'Muebles - AJ Link Suplidores Hoteleros',
    'software-hotelero.html': 'Software Hotelero - AJ Link Suplidores Hoteleros',
}

H1_FIXES = {
    'kitchen-equipment.html': 'Kitchen Equipment',
    'green-supplies.html': 'Green Supplies',
}

META_FIXES = {
    'contactos.html': (
        'Siin embargo',
        'Sin embargo',
    ),
}

LOCAL_BUSINESS_JSONLD = {
    'contact.html': {
        'name': 'AJ Link Inc',
        'description': 'Miami-based hotel and restaurant supplier. Contact our regional offices across the Americas.',
    },
    'contactos.html': {
        'name': 'AJ Link Inc',
        'description': 'Proveedor de equipos y productos para hoteles y restaurantes. Contáctenos en nuestras oficinas regionales.',
    },
}


def page_url(filename):
    return f'{BASE_URL}/' if filename == 'index.html' else f'{BASE_URL}/{filename}'


def pair_for(filename):
    if filename in PAGE_PAIRS:
        return PAGE_PAIRS[filename]
    for en, es in PAGE_PAIRS.items():
        if es == filename:
            return en
    return None


def strip_hreflang(content):
    return re.sub(r'\s*<link rel="alternate" hreflang="[^"]+"[^>]*>\n?', '', content)


def build_hreflang_block(filename):
    counterpart = pair_for(filename)
    if not counterpart:
        return ''

    en_file = filename if filename not in SPANISH_PAGES else counterpart
    es_file = counterpart if filename not in SPANISH_PAGES else filename
    lines = [
        f'  <link rel="alternate" hreflang="en" href="{page_url(en_file)}" />',
        f'  <link rel="alternate" hreflang="es" href="{page_url(es_file)}" />',
        f'  <link rel="alternate" hreflang="x-default" href="{page_url(en_file)}" />',
        '',
    ]
    return '\n'.join(lines)


def inject_hreflang(content, filename):
    if not pair_for(filename):
        return content
    content = strip_hreflang(content)
    block = build_hreflang_block(filename)
    if re.search(r'<title>', content, re.IGNORECASE):
        return re.sub(r'(<title>[^<]*</title>\n?)', r'\1\n' + block, content, count=1)
    return re.sub(r'(<meta charset[^>]*>\n?)', r'\1' + block, content, count=1)


def set_html_lang(content, filename):
    lang = 'es' if filename in SPANISH_PAGES or filename == 'home-espanol.html' else 'en'
    return re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', content, count=1)


def fix_og_locale(content, filename):
    locale = 'es_US' if filename in SPANISH_PAGES or filename == 'home-espanol.html' else 'en_US'
    return re.sub(
        r'<meta property="og:locale" content="[^"]*">',
        f'<meta property="og:locale" content="{locale}">',
        content,
        count=1,
    )


def replace_title(content, title):
    escaped = html.escape(title, quote=False)
    content = re.sub(r'<title>[^<]*</title>', f'<title>{escaped}</title>', content, count=1)
    content = re.sub(
        r'(<meta property="og:title" content=")[^"]*(">)',
        rf'\1{html.escape(title, quote=True)}\2',
        content,
        count=1,
    )
    content = re.sub(
        r'(<meta name="twitter:title" content=")[^"]*(">)',
        rf'\1{html.escape(title, quote=True)}\2',
        content,
        count=1,
    )
    return content


def fix_h1(content, filename):
    if filename not in H1_FIXES:
        return content
    label = H1_FIXES[filename]
    return re.sub(
        r'(<h1 class="header-title[^"]*"><img class="ajlink-icon"[^>]*>)[^<]*(</h1>)',
        rf'\1{label}\2',
        content,
        count=1,
    )


def strip_structured_data(content):
    content = re.sub(
        r'\s*<script type="application/ld\+json">.*?</script>\n?',
        '',
        content,
        flags=re.DOTALL,
    )
    return content


def build_breadcrumb_jsonld(filename):
    if filename not in CATALOG_PAGES:
        return ''
    section, page_name = CATALOG_PAGES[filename]
    is_spanish = filename in SPANISH_PAGES
    home_name = 'Inicio' if is_spanish else 'Home'
    home_url = page_url('home-espanol.html' if is_spanish else 'index.html')
    section_url = page_url('productos.html' if is_spanish else 'products.html')
    page_url_value = page_url(filename)
    data = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': home_name, 'item': home_url},
            {'@type': 'ListItem', 'position': 2, 'name': section, 'item': section_url},
            {'@type': 'ListItem', 'position': 3, 'name': page_name, 'item': page_url_value},
        ],
    }
    return '  <script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n  </script>\n'


def build_localbusiness_jsonld(filename):
    if filename not in LOCAL_BUSINESS_JSONLD:
        return ''
    info = LOCAL_BUSINESS_JSONLD[filename]
    data = {
        '@context': 'https://schema.org',
        '@type': 'LocalBusiness',
        'name': info['name'],
        'description': info['description'],
        'url': page_url(filename),
        'telephone': '+1-305-461-0283',
        'email': 'alejandro@ajlink.com',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': '5975 Sunset Drive #506',
            'addressLocality': 'South Miami',
            'addressRegion': 'FL',
            'postalCode': '33143',
            'addressCountry': 'US',
        },
    }
    return '  <script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n  </script>\n'


def inject_extra_jsonld(content, filename):
    if filename in ('index.html', 'home-espanol.html'):
        return content
    block = build_breadcrumb_jsonld(filename) or build_localbusiness_jsonld(filename)
    if not block:
        return content
    content = strip_structured_data(content)
    if filename in CATALOG_PAGES:
        # Re-add organization block only on pages that had it stripped; catalog pages never had org.
        pass
    return re.sub(r'(</head>)', block + r'\1', content, count=1)


def add_skip_link(content, filename):
    if filename == '404-not-found.html':
        return content
    is_spanish = filename in SPANISH_PAGES or filename == 'home-espanol.html'
    label = 'Saltar al contenido' if is_spanish else 'Skip to content'
    link = f'  <a class="skip-link" href="#main-content">{label}</a>\n'
    if 'class="skip-link"' in content:
        return content
    return re.sub(r'(<body[^>]*>\n?)', r'\1' + link, content, count=1)


def add_main_content_id(content):
    if 'id="main-content"' in content:
        return content
    if re.search(r'<div class="grid-container"', content):
        return re.sub(
            r'(<div class="grid-container")',
            r'\1 id="main-content"',
            content,
            count=1,
        )
    if re.search(r'<div class="container header"', content):
        return re.sub(
            r'(<div class="container header")',
            r'\1 id="main-content"',
            content,
            count=1,
        )
    return content


def fix_input_types(content):
    return content.replace('type="input"', 'type="text"')


def apply_meta_fixes(content, filename):
    if filename in META_FIXES:
        old, new = META_FIXES[filename]
        content = content.replace(old, new)
    return content


def process_file(path):
    text = path.read_text(encoding='utf-8')
    updated = text
    filename = path.name

    updated = set_html_lang(updated, filename)
    updated = inject_hreflang(updated, filename)
    updated = fix_og_locale(updated, filename)

    if filename in TITLE_FIXES:
        updated = replace_title(updated, TITLE_FIXES[filename])

    updated = fix_h1(updated, filename)
    updated = apply_meta_fixes(updated, filename)

    if filename in CATALOG_PAGES or filename in LOCAL_BUSINESS_JSONLD:
        updated = inject_extra_jsonld(updated, filename)

    updated = add_skip_link(updated, filename)
    updated = add_main_content_id(updated)
    updated = fix_input_types(updated)

    if updated != text:
        path.write_text(updated, encoding='utf-8')
        return True
    return False


def fix_404():
    path = ROOT / '404-not-found.html'
    content = '''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, follow">
  <title>404 Page Not Found - AJ Link Hotel Suppliers</title>
  <link type="text/css" href="/css/styles.css" rel="stylesheet">
</head>

<body class="body-404">
  <div class="wrapper-four">
    <div class="wrapper-message2">
      <div class="align-m">
        <h1><em class="four-o-four">404</em><br>Page Not Found</h1>
        <span class="m-text">The page you were looking for does not exist.</span>
      </div>
    </div>
    <div class="wrapper-message">
      <div class="align-m">
        <img class="logo-four" src="/img/AjLink_Logo.svg" alt="AJ Link Logo">
        <a href="/index.html"><span class="button bck-home">Get me home &gt;&gt;</span></a>
      </div>
    </div>
  </div>
</body>

</html>
'''
    path.write_text(content, encoding='utf-8')
    return True


def build_sitemap():
    pairs = [
        ('index.html', 'home-espanol.html'),
        ('about.html', 'quienes-somos.html'),
        ('products.html', 'productos.html'),
        ('services.html', 'servicios.html'),
        ('contact.html', 'contactos.html'),
        ('food-beverage.html', 'alimentos-bebidas.html'),
        ('banquet-and-convention.html', 'banquete-convenciones.html'),
        ('furniture-supplies.html', 'muebles.html'),
        ('green-supplies.html', 'ecologicos.html'),
        ('kitchen-equipment.html', 'cocina.html'),
        ('laundry-equipment.html', 'lavanderia.html'),
        ('room-supplies.html', 'habitacion.html'),
        ('software-hotel-management.html', 'software-hotelero.html'),
    ]
    lastmod = '2026-06-20'
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    def url_entry(loc, priority, changefreq, en_file=None, es_file=None):
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append(f'    <changefreq>{changefreq}</changefreq>')
        lines.append(f'    <priority>{priority}</priority>')
        if en_file and es_file:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{page_url(en_file)}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{page_url(es_file)}"/>')
        lines.append('  </url>')

    for en, es in pairs:
        if en == 'index.html':
            url_entry(page_url(en), '1.0', 'monthly', en, es)
        elif en in ('about.html', 'contact.html'):
            url_entry(page_url(en), '0.8', 'yearly', en, es)
        elif en == 'products.html':
            url_entry(page_url(en), '0.9', 'monthly', en, es)
        elif en == 'services.html':
            url_entry(page_url(en), '0.7', 'yearly', en, es)
        else:
            url_entry(page_url(en), '0.7', 'monthly', en, es)

        if en != 'index.html':
            if en in ('about.html', 'contact.html'):
                pri, freq = '0.8', 'yearly'
            elif en == 'products.html':
                pri, freq = '0.9', 'monthly'
            elif en == 'services.html':
                pri, freq = '0.7', 'yearly'
            else:
                pri, freq = '0.7', 'monthly'
            url_entry(page_url(es), pri, freq, en, es)

    lines.append('</urlset>')
    lines.append('')
    (ROOT / 'sitemap.xml').write_text('\n'.join(lines), encoding='utf-8')


def main():
    updated = []
    for path in sorted(ROOT.glob('*.html')):
        if path.name == '404-not-found.html':
            continue
        if process_file(path):
            updated.append(path.name)
    fix_404()
    build_sitemap()
    print('updated', len(updated), 'pages')
    for name in updated:
        print(' ', name)


if __name__ == '__main__':
    main()
