## wrapper file ##
## shows how to run the code ##
## python version: python 3.6

from simulation import simulation
from random import seed

with open('num_tests.txt','r') as f: #how many tests
    nboftests = int(f.readline())
seed_needed = 1

for i in range(1,nboftests+1): #loop through all tests
    mode_reader = 'mode_' + str(i) + '.txt'
    para_reader = 'para_' + str(i) + '.txt'
    arrival_reader = 'arrival_' + str(i) + '.txt'
    service_reader = 'service_' + str(i) + '.txt'
    mrt_reader = 'mrt_' + str(i) + '.txt'
    departure_reader = 'departure_' + str(i) + '.txt'
    with open(mode_reader, 'r') as f:
        mode = f.readline() #get the mode information
        #print(mode)
    if mode == 'trace':
        with open(para_reader, 'r') as f: #3 parameters
            buffer = f.readlines()
            m = int(buffer[0].replace(' ',''))
            setup_time = float(buffer[1].replace(' ',''))
            t_c = float(buffer[2].replace(' ',''))
            # print(m)
            # print(setup_time)
            # print(t_c)
        with open(arrival_reader,'r') as fp:
            # contains the arrival times of the jobs with one arrival time occupying one line
            arrival_times = fp.readlines()
            for a in range(len(arrival_times)):
                arrival_times[a] = float(arrival_times[a])

        with open(service_reader, 'r') as fp2:
            service_times = fp2.readlines() #contains one service time per line
            for s in range(len(service_times)):
                service_times[s] = float(service_times[s])

        result = simulation(mode, arrival_times, service_times, m, setup_time, t_c)

        with open(mrt_reader, 'w') as fp3:
            fp3.write(str(result[0]))
        with open(departure_reader, 'w') as fp4:
            for i in result[1]:
                fp4.write(i[0] + '\t' + i[1])
                fp4.write('\n')


    elif mode == 'random':
        seed(seed_needed)
        seed_needed = seed_needed + 1 #renew seed number for next one
                                    #using different sets of random numbers
        with open(para_reader, 'r') as f: #4 parameters
            buffer = f.readlines()
            m = int(buffer[0].replace(' ',''))
            setup_time = float(buffer[1].replace(' ',''))
            t_c = float(buffer[2].replace(' ',''))
            time_end = float(buffer[3].replace(' ',''))
        with open(arrival_reader, 'r') as fp:
            arrival_times = float(fp.readline()) #a string for a floating point number: lambda
        with open(service_reader, 'r') as fp2:
            service_times = float(fp2.readline()) #a string for a floating point number: u

        result = simulation(mode, arrival_times, service_times, m, setup_time, t_c, time_end)

        with open(mrt_reader, 'w') as fp3:
            fp3.write(str(result[0]))
        with open(departure_reader, 'w') as fp4:
            for i in result[1]:
                fp4.write(i[0] + '\t' + i[1])
                fp4.write('\n')

    else: #only trace and random mode are allowed
        print('Wrong mode given.')
