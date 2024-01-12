#!/usr/bin/env python3

import docker,re,requests,json,time

URL = 'https://go.support.sap.com/minisap/odata/bkey/minisap/'
LIC_PATH_HDB = "/opt/s4-hana-trial/HDB_license"
LIC_PATH_A4H = "/opt/s4-hana-trial/ASABAP_license"
LIC_PROGRESS = 0
DEBUG = True

def write_license(path, content):
        f = open(path, "w")
        f.write(content)
        f.close()
        print(f"[+] Licensekey written to file: {path}")

def hdb_license(hwkey):
        payload = {"Type":"023","Name":"Mr Max Mustermann","Email":"muster@mann.corp","Hwkey":hwkey,"HostID":"","HostName":""}
        XSRF = ""
        session = requests.session()
        session.get(URL)
        response = session.get(URL, allow_redirects=True, headers = {"X-Csrf-Token":"Fetch"})
        XSRF = response.headers['x-csrf-token']
        response = session.post(url = URL + "LicenseKey", json = payload, headers = {"X-Csrf-Token":XSRF, "Accept":"application/json"}).json()
        write_license(path=LIC_PATH_HDB, content=response["d"]["Licensekey"])
        print("[*] HDB license updated successfully")

def a4h_license(hwkey):
        payload = {"Type":"025","Name":"Mr Max Mustermann","Email":"muster@mann.corp","Hwkey":hwkey,"HostID":"","HostName":""}
        XSRF = ""
        session = requests.session()
        session.get(URL)
        response = session.get(URL, allow_redirects=True, headers = {"X-Csrf-Token":"Fetch"})
        XSRF = response.headers['x-csrf-token']
        response = session.post(url = URL + "LicenseKey", json = payload, headers = {"X-Csrf-Token":XSRF, "Accept":"application/json"}).json()
        write_license(path=LIC_PATH_A4H, content=response["d"]["Licensekey"])
        print("[*] A4H license updated successfully")

while True:
        client = docker.from_env()
        container = client.containers.get("a4h")
        hdb_hardware_key = re.findall(r"HDB.*([A-Z0-9]{11})", container.logs().decode())
        a4h_hardware_key = re.findall(r":.([A-Z0-9]{11}).*\(", container.logs().decode())
        if DEBUG:
                print(f"[DEBUG] HDB keys: {len(hdb_hardware_key)}")
                print(f"[DEBUG] A4H keys: {len(a4h_hardware_key)}")
                print(f"[DEBUG] Stage: {LIC_PROGRESS}")
        if len(a4h_hardware_key) <= 0 and len(hdb_hardware_key) == 1 and LIC_PROGRESS == 0:
                print(f"[*] HDB HW Key: {hdb_hardware_key[-1]}")
                hdb_license(hdb_hardware_key[-1])
                LIC_PROGRESS = 1
                container.restart()
        elif len(a4h_hardware_key) == 1 and len(hdb_hardware_key) == 2 and LIC_PROGRESS == 1:
                print(f"[*] A4H HW Key: {a4h_hardware_key[-1]}")
                a4h_license(a4h_hardware_key[-1])
                LIC_PROGRESS = 2
                container.restart()
        elif len(a4h_hardware_key) >= 1 and len(hdb_hardware_key) > 2 and LIC_PROGRESS == 2:
                print("[+] All licenses generated and system restarted...")
                print("[+] Check \"docker logs -f a4h\" for any issues or details. ")
                break
        else:
                print("[*] Waiting for Container to come back online...")
                time.sleep(120) # sleep 4min