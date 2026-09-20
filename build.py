"""Build the static files published by GitHub Pages."""

from datetime import date

from server import BASE_DIR, load_content, write_static_site


def main() -> None:
    content = load_content()
    output_path = write_static_site(content)
    base_url = content["seo"]["canonical_url"].strip().rstrip("/")

    (BASE_DIR / "sitemap.xml").write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <lastmod>{date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
''',
        encoding="utf-8",
    )
    (BASE_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /admin.html\nDisallow: /api/\n\nSitemap: {base_url}/sitemap.xml\n",
        encoding="utf-8",
    )

    print(f"Built {output_path.name}, sitemap.xml, and robots.txt")


if __name__ == "__main__":
    main()
