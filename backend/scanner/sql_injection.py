import requests

def test_sql_injection(url):
    payload = "' OR '1'='1"
    try:
        r = requests.get(url, params={'input': payload}, timeout=5)
        if any(error in r.text.lower() for error in ['sql', 'syntax', 'query', 'mysql', 'warning']):
            print(f"[+] SQL Injection vulnerability found at {url}")
            return True
    except Exception as e:
        print(f"[!] Error testing SQLi on {url}: {e}")
    return False
