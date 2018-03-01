import os
import re

import subprocess

eth_list =[]
def get_ethernetports_eth():
    ports = []
    ip_address = []
    source_document_node = "/var/emulab/boot/nickname"
    if os.stat(source_document_node)[6] != 0:
        readdata = file(source_document_node, 'r')
        line = readdata.read()

        for matched in re.finditer(re.compile("node-\d{1,3}"), line):
            node_nickname = matched.group()
    if os.stat("/var/emulab/boot/ifmap")[6] != 0:
        readdata = file("/var/emulab/boot/ifmap", 'r')

        # Using regular expression extract the ethernet ports that are to be used

        for matched in re.finditer(re.compile('eth\d{1,2}'), readdata.read()):
            eth_list.append(matched.group())
    #os.system("sudo mkdir ~/tcpdumps")
    #os.system("sudo chmod -R 777 /users/ss997901/tcpdumps/")
    cmd = ''
    for i in range(0, len(eth_list)):
        #file_name = "tcpdump"+node_nickname+eth_list[i]+".txt"
        #os.system("sudo touch ~/tcpdumps/"+file_name)
    #os.system("sudo chmod 777 ~/tcpdumps/*")
    #os.system("screen -S screen+"+node_nickname+eth_list[i])
    #cmd = "sudo nohup tcpdump -n -i "+eth_list[i]+" > ~/tcpdumps/"+file_name+" &"
    #proc = subprocess.call(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #op, err = proc.communicate()
        #print op, err
    #os.system('screen -S testing'+str(i))
        cmd = 'screen -d -m -S testing'+str(i)+' | sudo tcpdump -i '+eth_list[i] +' -s 65535' + ' > ' +eth_list[i]+ '.txt &'
        cmd_tmp = 'pwd'

        print(cmd)
    #cmd = 'screen -d -m -S testing'+str(i)+'sudo tcpdump -i '+eth_list[i]+'>~/tcpdumps/'+file_name+' &'
        os.system(cmd)
        os.system(cmd_tmp)
        #proc = subprocess.call('\n',stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #op,err = proc.communicate()
        #print op, err

    #os.system('a')
    #subprocess.call('screen -X -S screen'+node_nickname+eth_list[i]+'+sudo tcpdump -i '+eth_list[i]+'>~/tcpdumps/'+file_name+' & ', shell=True)
    #time.sleep(3)
    #cmd += 'nohup sudo tcpdump -i '+eth_list[i]+'>~/tcpdumps/'+file_name+' & '
    #print(cmd)
    #proc = subprocess.call(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #op, err = proc.communicate()
    #print op, err

    #os.system(cmd)
    #os.system('a')
    #print (eth_list)


if __name__ == "__main__":
    get_ethernetports_eth()