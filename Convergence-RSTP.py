import csv
from datetime import datetime


def main():
    #fileName = 'node1_tcpdump.txt'
    fileName = raw_input("Enter the File:")
    data = open(fileName,'r')
    lines = data.readlines()
    flags =[]
    for line in lines:
        if '[' in line:
            beforeFlags = line.split('[')
            if ']' in beforeFlags[-1]:
                afterflags = beforeFlags[-1].split(']')
                current_flag = afterflags[0]
                flags.append(current_flag)
                if len(flags) > 1:
                    previous_flag = flags[-2]
                    if current_flag != previous_flag:
                        starttime = (beforeFlags[0].split(' ')[0])
                        print('Start time is :'+starttime)
                        normalized_starttime = (int(starttime.split('.')[-1])/1000000)+int(starttime.split('.')[0].split(':')[0])*3600+int(starttime.split('.')[0].split(':')[1])*60+int(starttime.split('.')[0].split(':')[2])
                        #print(normalized_starttime)
                        #bridge_id= afterflags[-1].split(' ')[2].split(',')[0]
                        with open('./' + fileName.split('.')[0] + '.csv','w') as csvfile:  # Create csv files inside the folder created
                            filewriter = csv.writer(csvfile,delimiter=',',
                                                    quotechar='|',
                                                    quoting=csv.QUOTE_MINIMAL)  # Creating the fileWriter object to write to the file
                            filewriter.writerow([starttime, current_flag, previous_flag])
                        break
    flagsRev = []
    for line in reversed(lines):
        if '[' in line:
            beforeFlags = line.split('[')
            if ']' in beforeFlags[-1]:
                afterflags = beforeFlags[-1].split(']')
                current_flag = afterflags[0]
                flagsRev.append(current_flag)
                if len(flagsRev) > 1:
                    previous_flag = flagsRev[-2]
                    if current_flag != previous_flag:
                        endtime = (beforeFlags[0].split(' ')[0])
                        print('End time is '+endtime)
                        normalized_endtime = int(endtime.split('.')[-1]) / 1000000 + int(
                            endtime.split('.')[0].split(':')[0]) * 3600 + int(endtime.split('.')[0].split(':')[1]) * 60 + int(
                            endtime.split('.')[0].split(':')[2])
                        bridge_id= afterflags[-1].split(' ')[2].split(',')[0]
                        with open('./' + fileName.split('.')[0] + '.csv','a') as csvfile:  # Create csv files inside the folder created
                            filewriter = csv.writer(csvfile, delimiter=',',
                                                    quotechar='|',
                                                    quoting=csv.QUOTE_MINIMAL)  # Creating the fileWriter object to write to the file
                            filewriter.writerow([endtime, current_flag,previous_flag])
                        break
    print('Convergence time :'+str(normalized_endtime-normalized_starttime)+' seconds')

if __name__==('__main__'):
    main()
