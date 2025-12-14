from flask import Flask, render_template, request
import re
from urllib.parse import urlparse

app = Flask(__name__)

PHISH_KEYWORDS = ["login", "verify", "secure", "account", "update", "confirm", "password"]


def analyze_url(url):
    result = {}
    url = (url or "").strip()
    # Ensure a scheme is present so hostname is parsed correctly
    to_parse = url if urlparse(url).scheme else f"http://{url}"
    parsed = urlparse(to_parse)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    result["url_length"] = len(url)
    result["too_long"] = len(url) > 80

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    result["is_ip"] = bool(re.match(ip_pattern, hostname))

    result["contains_at"] = "@" in url

    subdomain_parts = hostname.split(".")
    result["subdomain_count"] = len(subdomain_parts)
    result["too_many_subdomains"] = len(subdomain_parts) >= 4

    result["domain_length"] = len(hostname)
    result["domain_too_long"] = len(hostname) > 30

    lower_url = url.lower()
    result["keyword_hits"] = [k for k in PHISH_KEYWORDS if k in lower_url]
    result["has_keywords"] = len(result["keyword_hits"]) > 0

    score = (
        result["too_long"]
        + result["is_ip"]
        + result["contains_at"]
        + result["too_many_subdomains"]
        + result["domain_too_long"]
        + result["has_keywords"]
    )

    result["risk_score"] = int(score)
    result["risk_level"] = (
        "High" if score >= 4 else "Medium" if score >= 2 else "Low"
    )

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = (request.form.get("url") or "").strip()
        if not url:
            return render_template("index.html", error="Please provide a URL to scan.")

        analysis = analyze_url(url)
        return render_template("result.html", analysis=analysis, url=url)

    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
