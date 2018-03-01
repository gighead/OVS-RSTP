#This program parses the xml topo file and creates a readable Topo file


from xml.dom import minidom
from time import gmtime, strftime
import paramiko
import sys
import os
import re
import time
import subprocess
import pdb
import paramiko
import pdb


global ip_int
ip_int = []

def hostInfo(node):
    '''
    Extract the hostname and Port number under the node tag
    :return:
    '''
    #pdb.set_trace()
    host_all = []
    login_info = node.getElementsByTagName("login") #login is the tag name
    for elem in login_info:
        hostname = (elem.attributes["hostname"]).value
        port = (elem.attributes["port"]).value

    host = str(hostname),str(port)

    return host


def ipStrip(node):
    ''' arc
    Extract the IP address from each node
    :param node:
    :param ip:
    :return:
    '''
    #pdb.set_trace()
    cat = []
    int_lst = node.getElementsByTagName("interface")
    print "No of interface: {0}".format(len(int_lst))
    #print int_lst
    for item in int_lst:
        intr = (item.attributes["client_id"]).value
        cat.append(intr)

    ip_lst = node.getElementsByTagName("ip")
    #print "No of IP: {0}".format(len(ip_lst))


    for ip in ip_lst:
        ip_address = (ip.attributes["address"]).value
        cat.append(ip_address)

    #print cat
    #print ip_int
    return tuple(cat)


def formKeys(node, client_id):

    '''
        Extract the information about
        1. Node name + portnumber
        2.IP address of the node
        3.Interface (client_IP)
    :return:
    '''
    must_keys = []


    node_lst = xmldoc.getElementsByTagName(node)
    #print "Number of Nodes: {0}".format(len(node_lst))
    for node in node_lst:
        interface = node.attributes[client_id]
        must_keys.append(interface.value)

    return must_keys

def formValues(node, interface, ip, mac):
    '''
    Extract the hostname,portnum,interface,ip and mac for forming tuples of values
    :param node:
    :param interface:
    :param ip:
    :param mac:
    :return:
    '''

    must_values = []
    node_lst = xmldoc.getElementsByTagName(node)
    #pdb.set_trace()
    for node in node_lst:
        hostname = hostInfo(node)
        #must_values.append(hostname)
        ipaddr = ipStrip(node)
        #print ipaddr
        full = hostname + ipaddr
        must_values.append(full)

    return must_values

def dumpInFile(dev_info, time):
    '''
    :return:
    '''
    #print dev_info
    file_name = "info" + "_" +  str(time)
    file = open(file_name, 'w')
    file.write(str(dev_info))
    file.close()

    return file_name


def connect_args(full_dict, node):
    '''
    It Returns three parameters
    :param full_dict:
    :return: hostname, port
    '''
    tmp_host = full_dict[node]
    host,port = tmp_host[0],tmp_host[1]


    return host,port

def trigger_MNLR(info_dict, user, password):

    '''
    Execute appropriate MNLR commands on each nodes
    :return:
    '''
    #read the command file
    nodes = []
    for node in info_dict:
        nodes.append(node)


    #Maintain a list for the hostnames
    ssh = []
    for i in range(0, len(info_dict)):
        ssh.append(paramiko.SSHClient())
	#pdb.set_trace()
        tmp_info = info_dict[node]
        ssh[i].set_missing_host_key_policy(paramiko.AutoAddPolicy())

        mykey = paramiko.RSAKey.from_private_key_file('/Users/SVP/.ssh/id_geni_ssh_rsa',password=password)
        sys.stdout.write("\rConnecting: %s" % (nodes[i]))
        sys.stdout.flush()

        #call the command args function
	
        host, port = connect_args(info_dict, nodes[i])
        ssh[i].connect(host, username= user, pkey=mykey, port=int(port))
	#stdin, stdout, stderr = ssh[i].exec_command('mkdir Shashank')
	#stdin, stdout, stderr = ssh[i].exec_command('sudo chmod 777 /users/sr1632/code_repository_for_GENI/collectConverge.sh')
	stdin, stdout, stderr = ssh[i].exec_command('sudo pip install pexpect')
	print stdout.readlines()
	print stderr.readlines()
	#print 'Expect is installed'
	stdin1, stdout1, stderr1 = ssh[i].exec_command('python ~/code_repository_for_GENI/converge_telnet_ospf.py > converge.txt &')
	#stdin, stdout, stderr = ssh[i].exec_command('pwd')
	print stdout1.readlines()
	#print stdout1.readlines()
	#print stderr.readlines()

        print 'collect converge is running'


def collect_info(info_file, user, code_dir):
    '''
    Read the dev info from the file and form a dictionary
    :return:
    '''
    my_dict = eval(open(info_file).read())
    print "Number of Nodes: {0}".format(len(my_dict))
    print "RIT username : {0}".format(user)

    #try to copy the latest MNLR code from the execution server to each of the
    #nodes in the GENI
    #print my_dict
    for node in my_dict:
        conn_info = my_dict[node]
        scp_cmd = "scp -i ~/.ssh/id_geni_ssh_rsa -P {0} -r {1} {2}@{3}:/users/{4}".format(conn_info[1], code_dir, user, conn_info[0], user)
        #print scp_cmd
        proc = subprocess.Popen(scp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        op, err = proc.communicate()
        print op, err
        time.sleep(3)
        match = re.search("(yes/no)", op)
        if match:
            print match.group()
            os.system("yes")
            time.sleep(10)
        print "Copied the OSPF Code to {0}".format(node)
	
    return my_dict

if __name__ == "__main__":
    rspec_file = raw_input("Enter the rspec file name:")
    #rspec_file = '/home/sr1632/Shashank/scripts/more/'+rspec_name
    #rspec_file = 'DC-FINAL-MANIFEST-rspec.xml'
    xmldoc = minidom.parse(rspec_file)
    keys = formKeys('node', 'client_id')
    vals = formValues('node', 'interface', 'address', 'mac_address')
    map = dict(zip( keys, vals))
    time_now = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    info_file = dumpInFile(map, time_now)

    #ipStrip('interface')
    #uname = raw_input("Enter the username: ")
    uname = 'ss997901'
    code_dir = '/Users/SVP/Documents/Capstone-OVS/OVS-install/'#raw_input("Enter the code directory:")
    #code_dir = '/Users/SVP/Documents/MNLR/MNLR_LATEST/'
    info_dict = collect_info(info_file, uname, code_dir)
    trigger_MNLR(info_dict,uname, password = 'citrix123')



