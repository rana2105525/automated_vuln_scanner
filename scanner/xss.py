import requests

def test_xss(url):
    payload = "<script>alert('XSS')</script>"
    try:
        r = requests.get(url, params={'q': payload}, timeout=5)
        if payload in r.text:
            print(f"[+] XSS vulnerability found at {url}")
            return True
    except Exception as e:
        print(f"[!] Error testing XSS on {url}: {e}")
    return False
