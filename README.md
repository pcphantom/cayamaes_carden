# Cayamae's Ancient Garden

This version keeps the site's copy and catalog in `content.json`, while publishing a normal static `index.html` that GitHub Pages can serve.

## Publish an update

1. Install the dependency: `pip install -r requirements.txt`
2. Start the local editor: `python server.py`
3. Open <http://localhost:5050/admin.html> and sign in.
4. Save your changes. The server updates both `content.json` and the generated `index.html`.
5. Commit and push both changed files to GitHub.

The default local credentials are `admin` / `change-me`. Set `CAG_ADMIN_USERNAME`, `CAG_ADMIN_PASSWORD`, and `CAG_SECRET_KEY` before using the editor on any public server. The editor is a local Flask tool; GitHub Pages only hosts the generated public site.

You can also edit `content.json` directly and run:

```powershell
python build.py
```

That command regenerates `index.html`, `sitemap.xml`, and `robots.txt`.

## Project structure

```text
content.json        Editable site copy, products, links, and SEO
site_template.html  Jinja source template
index.html          Generated static page published by GitHub Pages
admin.html          Local editing interface
server.py           Local preview and editing server
build.py            Static-site build command
css/style.css       Site styling
js/main.js          Navigation, filters, and scroll behavior
```

Do not edit generated `index.html` by hand. Make content changes in `content.json` or layout changes in `site_template.html`, then run `python build.py`.

## Product photos

Optimized product photos live in `images/products/`. The originals remain in their individual product folders outside this website repository.

Each photographed product in `content.json` has `image`, `image_alt`, `image_width`, and `image_height` fields. New photos should be converted to WebP, resized to no more than 900 pixels on the longest side, placed in `images/products/`, and referenced through those fields. Products without a photo continue to use their built-in botanical artwork.

## Notes

- Fonts load from Google Fonts and require internet access.
- Product inquiry buttons currently show a confirmation message; there is no shopping cart.
- Patreon, Etsy, and Facebook links still contain placeholders in `content.json` and should be replaced before launch.
