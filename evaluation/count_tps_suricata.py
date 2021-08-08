import argparse
import json
import pprint
import re


def main():
    args = parse_args()
    rule_counts = {}
    suricata_alert = re.compile('\[.*\] (.*) \[.*\] \[.*\] .*')
    with open(args.filename, 'r') as f:
        for line in f:
            event = json.loads(line)
            if 'program' in event and event['program'] == 'suricata':
                try:
                    rule = suricata_alert.search(event['message']).group(1)
                    if true_positive(rule):
                        rule_counts[rule] = rule_counts.get(rule, 0) + 1
                except AttributeError:
                    print('WARNING Skipping message: ' + event['message'].strip())
    pprint.pprint(rule_counts)


def parse_args():
    parser = argparse.ArgumentParser(description='Count True Positives')
    parser.add_argument('filename', help='JSONL input file')
    return parser.parse_args()


def true_positive(rule):
    tps = {
        # misc_sqlmap
        'ET SCAN Sqlmap SQL Injection Scan',
        'ET WEB_SERVER Possible SQL Injection Attempt SELECT FROM',
        'ET WEB_SERVER Possible SQL Injection Attempt UNION SELECT',
        'ET WEB_SERVER Script tag in URI Possible Cross Site Scripting Attempt',
        'ET WEB_SERVER Attempt To Access MSSQL xp_cmdshell Stored Procedure Via URI',
        'ET WEB_SERVER Possible MySQL SQLi Attempt Information Schema Access',
        'ET WEB_SERVER SQL Errors in HTTP 200 Response (error in your SQL syntax)',
        'ET WEB_SERVER MYSQL SELECT CONCAT SQL Injection Attempt',
        'ET WEB_SERVER SQL Injection Select Sleep Time Delay',
        'ET WEB_SERVER MYSQL Benchmark Command in URI to Consume Server Resources',
        'ET WEB_SERVER Possible Attempt to Get SQL Server Version in URI using SELECT VERSION',
        'ET WEB_SERVER Possible attempt to enumerate MS SQL Server version',
        'ET WEB_SERVER ATTACKER SQLi - SELECT and Schema Columns',
        # infect_email_exe
        'ET INFO SUSPICIOUS SMTP EXE - EXE SMTP Attachment',
        # c2_take_screenshot
        'ET POLICY PE EXE or DLL Windows file download HTTP',
        'ET INFO Executable Retrieved With Minimal HTTP Headers - Potential Second Stage Download',
        'ET INFO SUSPICIOUS Dotted Quad Host MZ Response',
        'ET INFO EXE IsDebuggerPresent (Used in Malware Anti-Debugging)',
        'ET TROJAN Possible Metasploit Payload Common Construct Bind_API (from server)',
        # c2_exfiltration
        # c2_mimikatz
        # misc_download_malware
        'ET INFO Executable Download from dotted-quad Host',
        'ET POLICY PE EXE or DLL Windows file download HTTP',  # duplicate
        'ET INFO SUSPICIOUS Dotted Quad Host MZ Response',  # duplicate
        # misc_set_autostart
        # misc_execute_malware
    }
    if rule in tps:
        return True
    return False


if __name__ == '__main__':
    main()
