from scanner import crawler, sql_injection, xss, csrf, report
import requests

def main():
    target_url = input("Enter the target URL (e.g. http://testphp.vulnweb.com): ").strip()

    print("[*] Crawling target...")
    urls = crawler.crawl(target_url)
    urls.append(target_url)  # Ensure root is tested

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

    report.write_report(vulns)
    report.write_log(target_url, vulns)


if __name__ == "__main__":
    main()
