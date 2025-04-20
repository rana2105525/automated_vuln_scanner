def test_csrf(response):
    if "csrf" not in response.text.lower():
        print(f"[+] Possible CSRF vulnerability found at {response.url}")
        return True
    return False
