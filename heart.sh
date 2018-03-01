#!/bin/sh
screen -d -m -S testing0 | sudo tcpdump -i eth1 -s 65535 > eth1.txt &
screen -d -m -S testing1 | sudo tcpdump -i eth2 -s 65535 > eth2.txt &
screen -d -m -S testing2 | sudo tcpdump -i eth3 -s 65535 > eth3.txt &
screen -d -m -S testing2 | sudo tcpdump -i eth3 -s 65535 > eth4.txt &
