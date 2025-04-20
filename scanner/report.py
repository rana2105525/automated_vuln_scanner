import os

def write_report(vulns):
    os.makedirs("report", exist_ok=True)
    with open("report/scan_report.txt", "w") as f:
        if not vulns:
            f.write("No vulnerabilities found.\n")
        else:
            for vuln in vulns:
                f.write(f"{vuln['type']} found at {vuln['url']}\n")
    print("[+] Report saved to report/scan_report.txt")
