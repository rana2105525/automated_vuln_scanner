import os
import json
from datetime import datetime

def write_report(results):
    os.makedirs("report", exist_ok=True)
    with open("report/scan_report.txt", "w") as f:
        for entry in results:
            f.write(f"\nURL: {entry['url']}\n")
            f.write("-" * 50 + "\n")
            for r in entry["results"]:
                status = r["status"]
                vuln_type = r["type"]
                f.write(f"{vuln_type}: {status}\n")
            f.write("-" * 50 + "\n")
    print("[+] Report saved to report/scan_report.txt")


def write_log(target_url, scan_results):
    os.makedirs("data", exist_ok=True)
    log_path = "data/logs.json"

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target_url,
        "results": []
    }

    for entry in scan_results:
        result_obj = {"url": entry["url"]}
        for r in entry["results"]:
            result_obj[r["type"]] = r["status"]
        log_entry["results"].append(result_obj)

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=4)

    print("[+] Log updated in data/logs.json")
