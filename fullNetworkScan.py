import subprocess
import logging


def scanNetwork(ip):
    try:
        # run nmap scan
        subprocess.run(["sudo", "nmap", "-T4", "-F", ip + "/24"])
        logging.info("The nmap scan was running without errors")
    # exception when nmap is not installed
    except Exception as e:
        logging.warning("The following error raise when running nmap: " + str(e))
        print("Error: please install nmap before run this full network scan. (Run 'sudo apt-get install nmap')")


