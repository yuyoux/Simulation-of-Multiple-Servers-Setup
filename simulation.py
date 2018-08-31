from random import random, uniform
import math

#import matplotlib.pyplot as plt


def simulation(mode, arrival_times, service_times, m, setup_time, delayedoff_time, time_end = 0): #added time_end for random mode

    if mode == 'random': #random mode
        time_counter = 0
        lmd = arrival_times
        miu = service_times
        arrival_times = []
        service_times = []
        while time_counter - math.log(1 - uniform(0,1)) / lmd < time_end:
            # inter-arrival probability distribution
            time_counter -= math.log(1 - uniform(0,1)) / lmd
            arrival_times.append(time_counter)
            # service time distribution
            sum_k = 0
            for i in range(0,3):
                s = - math.log(1 - uniform(0,1)) / miu
                sum_k += s
            service_times.append(sum_k)
        # print(arrival_times)
        # print(service_times)
        result = process(arrival_times, service_times, m, setup_time, delayedoff_time, time_end)

        #try to find steady state - draw pictures
        draw_material1 = result[1]
        mk_mean = []
        mk_nb = 1
        for i in range(len(draw_material1)):
            per_mean = float(draw_material1[i][1]) - float(draw_material1[i][0])
            mk_mean.append([mk_nb, per_mean])
            mk_nb += 1
        # print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # print(mk_mean)
        # print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
        mk_x = []
        mk_y = []
        for i in mk_mean:
            mk_x.append(i[0])
            mk_y.append(i[1])
        mk_smooth = []
        w = 1000
        for i in range(len(mk_y)):
            if i > w and i < (len(mk_y) - w):
                if len(mk_y[i - w:i + w]) != 0:
                    mk_smooth.append(sum(mk_y[i - w:i + w]) / len(mk_y[i - w:i + w]))
            elif i >= 1 and i <= w:
                mk_smooth.append(sum(mk_y[:2*i-1]) / len(mk_y[:2*i-1]))
            elif i == 0:
                mk_smooth.append(mk_y[0])
        for others in range(len(mk_y) - w, len(mk_y)):
            mk_smooth.append(sum(mk_y[others-w:]) / len(mk_y[others-w:]))
        # plt.plot(mk_x,mk_smooth)
        # plt.xlabel("endtime = 8000, w = 1000")
        # plt.show()

        #comput steady state mean response time
        steady_point = 601
        steady_list = []
        for i in mk_mean:
            if i[0] >= steady_point:
                steady_list.append(i[1])
        steady_mean = sum(steady_list[:steady_point]) / len(steady_list[:steady_point])
        print(steady_mean)
        print()

        return result

    else: #trace mode
        result = process(arrival_times, service_times, m, setup_time, delayedoff_time)
        return result

def process(arrival_times, service_times, m, setup_time, delayedoff_time, time_end = 0):
    ## initialization ##
    departure_times = []
    for i in range(len(arrival_times)):
        departure_times.append(0)

    server_status = []
    for i in range(m):
        single_server = []
        #0 ID of this server
        single_server.append(i)
        #1 status of this server - default as 'OFF'
        single_server.append('OFF')
        #2 setup_time of this server
        single_server.append(setup_time)
        #delayedoff_time of this server
        single_server.append(delayedoff_time)
        #current countdown time
        single_server.append(delayedoff_time)
        #delayedoff start point - default as 0
        single_server.append(0)
        server_status.append(single_server)
    #server: 0 ID of this server, 1 status of this server, 2 setup_time of this server
    # 3 delayedoff_time of this server, 4 current countdown time, 5 delayedoff start point

    buffer_content = []
    #job: 0 index of this job, 1 begin time of this job, 2 service time of this job
    # 3 'MARKED' or 'UNMARKED', 4 telling which server responsible for this job

    master_clock = []
    #event type: 0: departure  1: arrival  2:finished_delayedoff  3:finished_setup
    for i in range(len(arrival_times)):
        cur_event = [i,'ARRIVAL',arrival_times[i],service_times[i],-1]
        master_clock.append(cur_event)
    #event: 0 index of this event, 1 status of this event, 2 (happen at)current time of this event
    # 3 service time of this event, 4 telling which server responsible for this happened event

    ##  main loop ##
    while master_clock:
        event = master_clock.pop(0) #dealing with events one by one

        if event[1] == 'ARRIVAL': #arrival event
            delayedoff_flag = -1
            off_flag = -1
            #check for delayedoff server and locate it
            for s in server_status:
                if s[1] == 'DELAYEDOFF'and delayedoff_flag == -1:
                    delayedoff_flag = s[0]
                if s[1] == 'DELAYEDOFF' and delayedoff_flag != -1:
                    #compare the countdown time
                    #to find the index of the longest remaining time server
                    if s[4] > server_status[delayedoff_flag][4]:
                        delayedoff_flag = s[0]
            #check for off server and locate it
            for s in server_status:
                if s[1] == 'OFF' and off_flag == -1:
                    off_flag = s[0]

            if delayedoff_flag != -1: #at least one delayedoff
                # cancell timer
                server_status[delayedoff_flag][4] = server_status[delayedoff_flag][3]
                # change to busy
                server_status[delayedoff_flag][1] = 'BUSY'
                happen_at = event[2] + event[3]
                relevant_event = [event[0], 'DEPARTURE', happen_at, event[3], delayedoff_flag]
                master_clock.append(relevant_event)
            else: #delayedoff_flag == -1
                if off_flag == -1: #no delayed off and no off server
                    #put job at end of queue as unmarked
                    cur_job = [event[0], event[2], event[3], 'UNMARKED', -1]
                    buffer_content.append(cur_job)
                else: #no delayedoff and at leat one off server
                    happen_at = event[2] + setup_time
                    relevant_event = [-1, 'SETUP', happen_at, setup_time, off_flag]
                    master_clock.append(relevant_event)
                    # select one and turn on
                    server_status[off_flag][1] = 'SETUP'
                    # marked job waiting for setup
                    cur_job = [event[0], event[2], event[3], 'MARKED',off_flag]
                    #put job at the end of the queue
                    buffer_content.append(cur_job)


        elif event[1] == 'SETUP': #finished_setup event
            cur_job = buffer_content.pop(0)
            server_status[cur_job[4]][1] = 'BUSY' #change to busy
            happen_at = event[2] + cur_job[2]
            relevant_event = [cur_job[0],'DEPARTURE', happen_at, cur_job[2], event[4]]
            master_clock.append(relevant_event)


        elif event[1] == 'DEPARTURE':
            if time_end != 0: #random - check whether departure time exceed the time_end
                if event[2] <= time_end:
                    departure_times[event[0]] = event[2]  # collect departure information
            else: #trace - no check for time_end needed
                departure_times[event[0]] = event[2] #collect departure information

            if not buffer_content: #if empty queue
                # counter initialization
                server_status[event[4]][5] = event[2]
                #change to delayedoff
                server_status[event[4]][1] = 'DELAYEDOFF'
            else: #at least one job in queue
                #take job at the head of queue to server
                cur_job = buffer_content.pop(0)
                #whether the sent job is marked
                if cur_job[3] == 'UNMARKED':
                    happen_at = event[2] + cur_job[2]
                    relevant_event = [cur_job[0],'DEPARTURE', happen_at, cur_job[2], event[4]]
                    master_clock.append(relevant_event)
                else: #if it is marked job
                    #has to decide whether setup process should continue
                    #check whether an unmarked job in queue
                    unmarked_flag = -1
                    setup_flag = -1
                    for i in range(len(buffer_content)):
                        if unmarked_flag == -1 and buffer_content[i][3] == 'UNMARKED':
                            unmarked_flag = i
                    for i in range(len(master_clock)):
                        if master_clock[i][1] == 'SETUP':
                            setup_flag = i

                    if unmarked_flag != -1: #at least one unmarked job
                        #change first unmarked job to marked job
                        buffer_content[unmarked_flag][3] = 'MARKED'
                        buffer_content[unmarked_flag][4] = cur_job[4]
                    else: #no unmarked job
                        server_to_off = master_clock.pop(setup_flag)
                        #turns off the server
                        server_status[server_to_off[4]][1] = 'OFF'
                    happen_at = event[2] + cur_job[2]
                    relevant_event = [cur_job[0], 'DEPARTURE', happen_at, cur_job[2], event[4]]
                    master_clock.append(relevant_event)

        for s in server_status: #whether finished_delayedoff - renew the countdown time
            if s[1] == 'DELAYEDOFF':
                #calculate the current countdown timer
                countdown = s[3] - (event[2] - s[5])
                # if count to 0, changing from delayedoff to off, cancelling timer
                if countdown <= 0:
                    s[1] = 'OFF'
                    s[4] = s[3]
                else: # otherwise renew the value
                    s[4] = countdown

        #sorting of the master_clock
        master_clock.sort(key=lambda x: x[2])

        #check correctness of simulation: #marked job = #setup server
        correct_flag = False
        nb_of_setup_server = 0
        nb_of_marked_job = 0
        for m in server_status:
            if m[1] == 'SETUP':
                nb_of_setup_server += 1
        for n in buffer_content:
            if n[3] == 'MARKED':
                nb_of_marked_job += 1
        if nb_of_setup_server == nb_of_marked_job:
            correct_flag = True

        ## help for testing ##
        print(event[2], correct_flag)
        print(buffer_content)
        for s in server_status:
            print(s[1])
        print('\n')

    #calculation and formatting
    final_info = []
    for i in range(len(departure_times)):
        if departure_times[i] != 0: #if equal to 0, meaning departure time > time_end
            final_info.append(['{0:.3f}'.format(arrival_times[i]),'{0:.3f}'.format(departure_times[i])])

    final_info.sort(key=lambda x: float(x[1]))  #sorting the output information

    sum_response = 0
    for i in range(len(final_info)):
        per = float(final_info[i][1]) - float(final_info[i][0])
        sum_response += per
    mean_response = '{0:.3f}'.format(round(float(sum_response / len(final_info)), 3))

    print(mean_response)
    #print(final_info)
    print('-------------------------------------------------------------------------------')

    return [mean_response, final_info]
