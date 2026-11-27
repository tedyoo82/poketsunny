#!/usr/bin/env python3
"""Generate sitemap.xml with all individual Pokémon pages."""

import os
import glob

BASE_URL = "https://pokesunny.com"
POKEDEX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokedex")

def generate_sitemap():
    # Find all pokemon pages
    pattern = os.path.join(POKEDEX_DIR, "pokemon-*.html")
    pages = sorted(glob.glob(pattern))
    
    # Build XML
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             '  <url>',
             '    <loc>https://pokesunny.com/</loc>',
             '    <lastmod>2026-11-27</lastmod>',
             '    <changefreq>weekly</changefreq>',
             '    <priority>1.0</priority>',
             '  </url>',
             '  <url>',
             '    <loc>https://pokesunny.com/pokemon.html</loc>',
             '    <lastmod>2026-11-27</lastmod>',
             '    <changefreq>weekly</changefreq>',
             '    <priority>0.8</priority>',
             '  </url>']
    
    for page in pages:
        filename = os.path.basename(page)
        # pokedex/pokemon-1-bulbasaur.html -> /pokedex/pokemon-1-bulbasaur.html
        rel_path = os.path.join("pokedex", filename)
        url = f"{BASE_URL}/{rel_path}"
        lines.append(f'  <url>')
        lines.append(f'    <loc>{url}</loc>')
        lines.append(f'    <lastmod>2026-11-27</lastmod>')
        lines.append(f'    <changefreq>monthly</changefreq>')
        lines.append(f'    <priority>0.6</priority>')
        lines.append(f'  </url>')
    
    lines.append('</urlset>')
    
    sitemap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    
    print(f"Generated sitemap.xml with {len(pages)} Pokémon pages")

if __name__ == "__main__":
    generate_sitemap()
