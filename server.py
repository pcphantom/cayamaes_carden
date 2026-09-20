"""
Cayamae's Ancient Garden — Web Server
=====================================
Serves the homepage, exposes a password-protected admin API,
and persists all editable site copy and SEO in content.json.

Setup:
    pip install -r requirements.txt
    python server.py

Default admin credentials:
    username: admin
    password: change-me

Change CAG_ADMIN_USERNAME and CAG_ADMIN_PASSWORD before going live.
"""

import json
import os
import secrets
import shutil
from datetime import date, datetime
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    Response,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
    session,
)

CONFIG = {
    "ADMIN_USERNAME": os.environ.get("CAG_ADMIN_USERNAME", "admin"),
    "ADMIN_PASSWORD": os.environ.get("CAG_ADMIN_PASSWORD", "change-me"),
    "SECRET_KEY": os.environ.get("CAG_SECRET_KEY", secrets.token_hex(32)),
    "PORT": int(os.environ.get("CAG_PORT", 5050)),
    "DEBUG": os.environ.get("CAG_DEBUG", "true").lower() == "true",
}

BASE_DIR = Path(__file__).parent
CONTENT_FILE = BASE_DIR / "content.json"
CONTENT_BACKUP_DIR = BASE_DIR / "content_backups"
TOP_LEVEL_KEYS = (
    "site",
    "nav",
    "hero",
    "philosophy",
    "products",
    "spiritual",
    "support",
    "testimonials",
    "footer",
    "seo",
)

CONTENT_BACKUP_DIR.mkdir(exist_ok=True)

app = Flask(__name__, template_folder=str(BASE_DIR))
app.secret_key = CONFIG["SECRET_KEY"]
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def load_content() -> dict:
    with open(CONTENT_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_content_file(data: dict) -> None:
    if CONTENT_FILE.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = CONTENT_BACKUP_DIR / f"content_{timestamp}.json"
        shutil.copy2(CONTENT_FILE, backup_path)
        backups = sorted(CONTENT_BACKUP_DIR.glob("content_*.json"))
        for old_backup in backups[:-30]:
            old_backup.unlink(missing_ok=True)

    with open(CONTENT_FILE, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


def validate_content_structure(data: dict) -> str | None:
    if not isinstance(data, dict):
        return "Content payload must be a JSON object."

    missing = [key for key in TOP_LEVEL_KEYS if key not in data]
    if missing:
        return f"Missing top-level sections: {', '.join(missing)}"

    for key in TOP_LEVEL_KEYS:
        if not isinstance(data[key], dict):
            return f"Top-level section '{key}' must be an object."

    return None


def require_admin(handler):
    @wraps(handler)
    def decorated(*args, **kwargs):
        if not session.get("admin_authenticated"):
            return jsonify({"error": "Unauthorized"}), 401
        return handler(*args, **kwargs)

    return decorated


def resolve_base_url(content: dict) -> str:
    canonical = str(content.get("seo", {}).get("canonical_url", "")).strip()
    if canonical:
        return canonical.rstrip("/")
    return request.url_root.rstrip("/")


def build_schema_json(content: dict, base_url: str) -> str:
    seo = content.get("seo", {})
    site = content.get("site", {})

    graph = []
    organization = {
        "@type": seo.get("schema_type", "Organization"),
        "@id": f"{base_url}/#organization",
        "name": seo.get("business_name") or site.get("brand_name", ""),
        "url": base_url,
        "description": seo.get("business_description") or seo.get("description", ""),
    }

    if site.get("phone"):
        organization["telephone"] = site["phone"]
    if site.get("email"):
        organization["email"] = site["email"]

    locality = seo.get("address_locality", "")
    region = seo.get("address_region", "")
    postal_code = seo.get("postal_code", "")
    if locality or region or postal_code:
        organization["address"] = {
            "@type": "PostalAddress",
            "addressLocality": locality,
            "addressRegion": region,
            "postalCode": postal_code,
        }

    same_as = [url for url in seo.get("same_as", []) if str(url).strip()]
    if same_as:
        organization["sameAs"] = same_as

    area_served = [area for area in seo.get("area_served", []) if str(area).strip()]
    if area_served:
        organization["areaServed"] = area_served

    graph.append(organization)

    faq_entries = []
    for entry in seo.get("faq", []):
        if not isinstance(entry, dict):
            continue
        question = str(entry.get("question", "")).strip()
        answer = str(entry.get("answer", "")).strip()
        if question and answer:
            faq_entries.append(
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": answer,
                    },
                }
            )

    if faq_entries:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{base_url}/#faq",
                "mainEntity": faq_entries,
            }
        )

    payload = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


@app.route("/")
@app.route("/index.html")
def index():
    content = load_content()
    base_url = resolve_base_url(content)
    schema_json = build_schema_json(content, base_url)
    return render_template(
        "index.html",
        content=content,
        base_url=base_url,
        schema_json=schema_json,
        current_year=datetime.now().year,
    )


@app.route("/admin")
@app.route("/admin.html")
def admin():
    return send_from_directory(BASE_DIR, "admin.html")


@app.route("/content.json")
def content_json():
    return send_from_directory(BASE_DIR, "content.json")


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if secrets.compare_digest(username, CONFIG["ADMIN_USERNAME"]) and secrets.compare_digest(
        password, CONFIG["ADMIN_PASSWORD"]
    ):
        session["admin_authenticated"] = True
        return jsonify({"ok": True})

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/admin/check")
def admin_check():
    if session.get("admin_authenticated"):
        return jsonify({"ok": True})
    return jsonify({"error": "Not authenticated"}), 401


@app.route("/api/admin/save", methods=["POST"])
@require_admin
def admin_save():
    data = request.get_json(silent=True)
    error = validate_content_structure(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        save_content_file(data)
    except Exception as exc:
        app.logger.error("Save failed: %s", exc)
        return jsonify({"error": "Save failed"}), 500

    return jsonify({"ok": True, "saved_at": datetime.now().isoformat()})


@app.route("/sitemap.xml")
def sitemap():
    content = load_content()
    base_url = resolve_base_url(content)
    today = date.today().isoformat()
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
    return Response(xml, mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    content = load_content()
    base_url = resolve_base_url(content)
    txt = f"""User-agent: *
Allow: /
Disallow: /admin
Disallow: /admin.html
Disallow: /api/

Sitemap: {base_url}/sitemap.xml
"""
    return Response(txt, mimetype="text/plain")


@app.route("/<path:path>")
def static_files(path: str):
    if path.startswith("api/"):
        abort(404)

    candidate = (BASE_DIR / path).resolve()
    try:
        candidate.relative_to(BASE_DIR.resolve())
    except ValueError:
        abort(404)

    if candidate.is_file():
        return send_from_directory(BASE_DIR, path)

    abort(404)


if __name__ == "__main__":
    print(
        f"""
╔══════════════════════════════════════════════════╗
║    Cayamae's Ancient Garden — Web Server        ║
╠══════════════════════════════════════════════════╣
║  Site:   http://localhost:{CONFIG['PORT']}                   ║
║  Admin:  http://localhost:{CONFIG['PORT']}/admin.html        ║
╠══════════════════════════════════════════════════╣
║  Username: {CONFIG['ADMIN_USERNAME']:<35}║
║  Password: {CONFIG['ADMIN_PASSWORD']:<35}║
╚══════════════════════════════════════════════════╝

Change CAG_ADMIN_USERNAME and CAG_ADMIN_PASSWORD before going live.
"""
    )
    app.run(host="0.0.0.0", port=CONFIG["PORT"], debug=CONFIG["DEBUG"])
