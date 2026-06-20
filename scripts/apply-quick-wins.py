#!/usr/bin/env python3
"""Apply quick-win fixes across AJ Link HTML pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EN_HUB = {
    'index.html': 'home',
    'about.html': 'about',
    'products.html': 'products',
    'services.html': 'services',
    'contact.html': 'contacts',
}

ES_HUB = {
    'home-espanol.html': 'inicio',
    'quienes-somos.html': 'sobre',
    'productos.html': 'productos',
    'servicios.html': 'servicios',
    'contactos.html': 'contacto',
}

EN_CATALOG = {
    'banquet-and-convention.html', 'food-beverage.html', 'furniture-supplies.html',
    'green-supplies.html', 'kitchen-equipment.html', 'laundry-equipment.html',
    'room-supplies.html', 'software-hotel-management.html',
}

ES_CATALOG = {
    'alimentos-bebidas.html', 'banquete-convenciones.html', 'cocina.html',
    'ecologicos.html', 'habitacion.html', 'lavanderia.html', 'muebles.html',
    'software-hotelero.html',
}

EN_NAV = {
    'home': ('index.html', 'Home'),
    'about': ('about.html', 'About'),
    'products': ('products.html', 'Products'),
    'services': ('services.html', 'Services'),
    'contacts': ('contact.html', 'Contacts'),
}

ES_NAV = {
    'inicio': ('home-espanol.html', 'Inicio'),
    'sobre': ('quienes-somos.html', 'Sobre'),
    'productos': ('productos.html', 'Productos'),
    'servicios': ('servicios.html', 'Servicios'),
    'contacto': ('contactos.html', 'Contacto'),
}


def fix_main_menu_block(menu, nav_map, active_key):
    for key, (href, text) in nav_map.items():
        pattern = rf'<li(?: class="active")?><a href="{re.escape(href)}">{re.escape(text)}</a>'
        replacement = (
            f'<li class="active"><a href="{href}">{text}</a>'
            if key == active_key
            else f'<li><a href="{href}">{text}</a>'
        )
        menu = re.sub(pattern, replacement, menu, count=1)
    return menu


def set_nav_active(html, nav_map, active_key):
    marker = '<ul id="main-menu">'
    start = html.find(marker)
    if start == -1:
        return html

    i = start + len(marker)
    depth = 1
    while i < len(html) and depth > 0:
        if html[i:i + 4] == '<ul ' or html[i:i + 4] == '<ul>':
            depth += 1
        elif html[i:i + 5] == '</ul>':
            depth -= 1
            if depth == 0:
                end = i + 5
                break
        i += 1
    else:
        return html

    menu = html[start:end]
    fixed_menu = fix_main_menu_block(menu, nav_map, active_key)
    return html[:start] + fixed_menu + html[end:]


def apply_common(html, filename):
    html = html.replace('&copy; 2018 AJ LINK INC', '&copy; 2026 AJ LINK INC')

    html = re.sub(
        r'<li><a href="#"><span class="icon-person-thin"></span>Alejandro Pollier \(President\)</a></li>',
        r'<li><a href="about.html"><span class="icon-person-thin"></span>Alejandro Pollier (President)</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-person-thin"></span>Alejandro Pollier \(Presidente\)</a></li>',
        r'<li><a href="quienes-somos.html"><span class="icon-person-thin"></span>Alejandro Pollier (Presidente)</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-phone-thin"></span>Telefone: 1-305-461-0283</a></li>',
        r'<li><a href="tel:+13054610283"><span class="icon-phone-thin"></span>Telephone: 1-305-461-0283</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-phone-thin"></span>Teléfono: 1-305-461-0283</a></li>',
        r'<li><a href="tel:+13054610283"><span class="icon-phone-thin"></span>Teléfono: 1-305-461-0283</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-printer-thin"></span>Fax: 1-305-665-0175</a></li>',
        r'<li><a href="tel:+13056650175"><span class="icon-printer-thin"></span>Fax: 1-305-665-0175</a></li>',
        html,
    )
    html = re.sub(
        r'target="https://goo\.gl/maps/VRNRDnnGmHA2"',
        r'target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = re.sub(
        r'target="https://www\.facebook\.com/ajlink1"',
        r'target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = re.sub(
        r'target="https://twitter\.com/AJLink7"',
        r'target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = re.sub(
        r'target="https://webmail\.hostway\.com/appsuite/ui"',
        r'target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = re.sub(
        r'target="https://typekit\.com/"',
        r'target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = re.sub(
        r'target="http://www\.gwebdesigner\.com/"',
        r'target="_blank" rel="noopener noreferrer"',
        html,
    )
    html = re.sub(
        r'<li><a href="index\.html"><span class="icon-truck-thin"></span>Services</a></li>',
        r'<li><a href="services.html"><span class="icon-truck-thin"></span>Services</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-blog-thin"></span>Check our Blog</a></li>',
        r'<li><a href="contact.html"><span class="icon-blog-thin"></span>Contact Us</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-blog-thin"></span>Nuestro Blog</a></li>',
        r'<li><a href="contactos.html"><span class="icon-blog-thin"></span>Contáctenos</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-twins-thin"></span>Work With Us</a></li>',
        r'<li><a href="contact.html"><span class="icon-twins-thin"></span>Work With Us</a></li>',
        html,
    )
    html = re.sub(
        r'<li><a href="#"><span class="icon-twins-thin"></span>Trabaje con Nosotros</a></li>',
        r'<li><a href="contactos.html"><span class="icon-twins-thin"></span>Trabaje con Nosotros</a></li>',
        html,
    )
    html = html.replace('Lenguaje Español', 'Español')
    html = html.replace('English Language', 'English')

    if filename in EN_HUB:
        html = set_nav_active(html, EN_NAV, EN_HUB[filename])
    elif filename in ES_HUB:
        html = set_nav_active(html, ES_NAV, ES_HUB[filename])
    elif filename in EN_CATALOG:
        html = set_nav_active(html, EN_NAV, 'products')
    elif filename in ES_CATALOG:
        html = set_nav_active(html, ES_NAV, 'productos')

    return html


def main():
    for path in sorted(ROOT.glob('*.html')):
        if path.name == '404-not-found.html':
            continue
        text = path.read_text(encoding='utf-8')
        updated = apply_common(text, path.name)
        if updated != text:
            path.write_text(updated, encoding='utf-8')
            print('updated', path.name)


if __name__ == '__main__':
    main()
