import ipaddress
import subprocess
import logging


def scanNetwork():
    print("\nFor this full network scan you need a local nmap installation. (Run 'sudo apt-get install nmap')")
    ip = input("Enter a valid host IP address for scanning the entire network where it participate: ")
    logging.info("Entered host IP is: " + str(ip))

    try:
        # check ip address
        ipaddress.ip_address(ip)

        try:
            # run nmap scan
            subprocess.run(["sudo", "nmap", "-sP", ip + "/24"])

        # exception when nmap is not installed
        except Exception as e:
            logging.warning("The following error raise when running nmap: " + str(e))
            print("Please install nmap before run this full network scan. (Run 'sudo apt-get install nmap')")

    # exception when the entered ip is not a IPv4 or IPv6 address
    except Exception as e:
        logging.warning("The following error raise when checking the IP address: " + str(e))
        print("Your input does not appear to be an IPv4 or IPv6 address, please try again.")
        scanNetwork()
