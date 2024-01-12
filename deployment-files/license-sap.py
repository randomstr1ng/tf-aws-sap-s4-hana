#!/usr/bin/env python3

import requests, json
from argparse import ArgumentParser

URL = 'https://go.support.sap.com/minisap/odata/bkey/minisap/'
INSTALLATION_ID = {
        "a4h": "025",
        "hdb": "023"
}
LIC_PATH_HDB = "/opt/s4-hana-trial/HDB_license"
LIC_PATH_A4H = "/opt/s4-hana-trial/ASABAP_license"

def parse_options():
        description = "This Script will automaticaly generate a Trial Licenses File for either a S/4HANA (SID: A4H) or the HANA Database (SID: HDB) and write it into a file into the current directory."
        usage = "%(prog)s [options]"
        parser = ArgumentParser(usage=usage, description=description)
        target = parser.add_argument_group("Target")
        target.add_argument("--hwkey", dest="HWKEY", help="Hardware Key of your SAP deployment", required=True)
        target.add_argument("--type", dest="TYPE", help="Please select the Instance: a4h or hdb", required=True)
        options = parser.parse_args()
        return options

def get_license(URL, HWKEY, TYPE):
        payload = {"Type":TYPE,"Name":"Mr Max Mustermann","Email":"muster@mann.corp","Hwkey":HWKEY,"HostID":"","HostName":""}
        XSRF = ""
        session = requests.session()
        session.get(URL)
        response = session.get(URL, allow_redirects=True, headers = {"X-Csrf-Token":"Fetch"})
        XSRF = response.headers['x-csrf-token']
        response = session.post(url = URL + "LicenseKey", json = payload, headers = {"X-Csrf-Token":XSRF, "Accept":"application/json"}).json()
        return response["d"]["Licensekey"], response["d"]["LicenseName"]

def write_keyfile(name, license):
        f = open(name, "w")
        f.write(license)
        f.close()
        print(f"[+] Licensekey written to file: {name}")

def main():
        options = parse_options()
        if str(options.TYPE).lower() in INSTALLATION_ID:
                licensekey, filename = get_license(URL = URL, HWKEY = options.HWKEY, TYPE = INSTALLATION_ID[str(options.TYPE).lower()])
                if filename == "A4H_Multiple.txt":
                    write_keyfile(name = LIC_PATH_A4H, license = licensekey)
                else:
                    write_keyfile(name = LIC_PATH_HDB, license = licensekey)
        else:
                print(f"[-] ERROR: Type {options.TYPE} not found or supported")
        print("[+] Done")
        print("[+] Please restart your SAP System now to apply the new licensekey")

main()