from flask import Flask, request, jsonify
from scanner import crawler, sql_injection, xss, csrf, report
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target_url = data.get('url')

    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    print(f"[*] Crawling target: {target_url}")
    urls = crawler.crawl(target_url)
    urls.append(target_url)  # Ensure the root URL is tested

    vulns = []

    for url in set(urls):
        print(f"\n[*] Testing {url}")
        result = {"url": url, "results": []}

        # SQL Injection
        if sql_injection.test_sql_injection(url):
            result["results"].append({"type": "SQL Injection", "status": "Vulnerable"})
        else:
            result["results"].append({"type": "SQL Injection", "status": "Safe"})

        # XSS
        if xss.test_xss(url):
            result["results"].append({"type": "XSS", "status": "Vulnerable"})
        else:
            result["results"].append({"type": "XSS", "status": "Safe"})

        # CSRF
        try:
            r = requests.get(url, timeout=5)
            if csrf.test_csrf(r):
                result["results"].append({"type": "CSRF", "status": "Vulnerable"})
            else:
                result["results"].append({"type": "CSRF", "status": "Safe"})
        except Exception as e:
            result["results"].append({"type": "CSRF", "status": f"Error: {e}"})

        vulns.append(result)

    # Write the report and logs as usual
    report.write_report(vulns)
    report.write_log(target_url, vulns)

    # Return scan results as JSON
    return jsonify(vulns)


if __name__ == '__main__':
    app.run(debug=True)
