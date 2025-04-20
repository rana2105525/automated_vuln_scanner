from scanner import crawler, sql_injection, xss, csrf, report
import requests

TARGET_URL = "http://example.com"  # Change to your test app URL

def main():
    print("[*] Crawling target...")
    urls = crawler.crawl(TARGET_URL)
    urls.append(TARGET_URL)  # Ensure root is tested too

    vulns = []

    for url in set(urls):
        print(f"[*] Testing {url}")

        if sql_injection.test_sql_injection(url):
            vulns.append({"type": "SQL Injection", "url": url})
        
        if xss.test_xss(url):
            vulns.append({"type": "XSS", "url": url})

        try:
            r = requests.get(url, timeout=5)
            if csrf.test_csrf(r):
                vulns.append({"type": "CSRF", "url": url})
        except:
            continue

    report.write_report(vulns)

if __name__ == "__main__":
    main()
