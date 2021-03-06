import subprocess
import logging
import detectMACvendor


def enter_sniff_duration():
    # ask user to enter duration for network sniffing
    try:
        duration = int(input("Enter the time of the duration of network sniffing in seconds (between 1 and 3600):"))
        # check duration
        if 0 < duration < 3600:
            logging.info("Entered network sniffing duration is: " + str(duration))
            # return duration
            return duration
        # input again when the duration integer is not between 1 and 3600
        else:
            print("Your input cannot be processed. Please enter an integer between 1 and 3600.")
            return enter_sniff_duration()
    # exception when the entered duration is not a int
    except:
        print("Your input cannot be processed. Please enter an integer between 1 and 3600.")
        return enter_sniff_duration()


def sniff_network(duration):
    # sniff network traffic to file
    logging.info("Start sniff network traffic")

    try:
        # run tshark network sniff
        subprocess.call(["sudo", "touch", "networksniff.pcap"])
        subprocess.call(["sudo", "tshark", "-a", "duration:" + duration, "-w", "networksniff.pcap"])
        logging.info("The network traffic of the last " + duration + " seconds is saved to the file networksniff.pcap")
    except Exception as e:
        logging.warning("The following error raise when running tshark: " + str(e))
        print("Error: please install tshark before run this full network scan. "
              "(Run 'sudo apt-get install tshark')\n")

    logging.info("End sniff network traffic")


def detectionmethod1(ip):
    # analyze network sniff file
    logging.info("Start analyze network traffic")

    print("\n#1: Results of the outgoing connections of all the hosts which are on the subnet of the entered "
          "IP address:\n")

    try:
        # run tshark network sniff to variable content
        command = subprocess.Popen(["sudo", "tshark", "-r", "networksniff.pcap", "-Y", "ip.src==" + ip + "/24", "-z",
                                    "ip_hosts,tree"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = command.stdout.read()
        content = output.decode("utf-8")

        # print output
        print(content)

        logging.info("File networksniff.pcap analyzing 1 is done")
    except Exception as e:
        logging.warning("The following error raise when running tshark: " + str(e))
        print("Error: please install tshark before run this full network scan. "
              "(Run 'sudo apt-get install tshark')\n")

    print("\n#1.1: Results of the outgoing connections of the entered IP address " + ip + ":\n")

    try:
        # run tshark network sniff to variable content
        command = subprocess.Popen(["sudo", "tshark", "-r", "networksniff.pcap", "-Y", "ip.src==" + ip],
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = command.stdout.read()
        content = output.decode("utf-8")

        # print content if there are outgoing network connections for ip
        if str(ip) in content:
            logging.info("Outgoing network connections for " + ip + " are printed")
            print(content)
        else:
            logging.info("There are no outgoing network connections for " + ip)
            print("There are no outgoing network connections for " + ip)

        logging.info("File networksniff.pcap analyzing 2 is done")
    except Exception as e:
        logging.warning("The following error raise when running tshark: " + str(e))
        print("Error: please install tshark before run this full network scan. "
              "(Run 'sudo apt-get install tshark')\n")

    logging.info("End analyze network traffic")


def detectionmethod2(ip):
    # detect virtual machine vendor
    logging.info("Start check MAC address vendor")

    vendor = detectMACvendor.mac_vendor(ip)

    print("\n#2: The vendor of the MAC address of the machine is: " + vendor)
    print("Check manually whether this is virtual machine vendor.")
    logging.info("Result of MAC address vendor: " + vendor)

    logging.info("End check MAC address vendor")


def passive(ip):
    # get duration of network sniffing
    duration = str(enter_sniff_duration())
    # sniff entire network for duration
    sniff_network(duration)

    print("\nThe results of the passive honeypot scan on " + ip + ":")
    # run all detection methods
    detectionmethod1(ip)  # analyze network sniff file
    detectionmethod2(ip)  # virtual machine/MAC vendor

    print("\n\nFor details about the process of scanning, check the logfile 'stefanMap.log'.\n")
