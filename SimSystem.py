from random import randrange
from collections import defaultdict
from statistics import mean,median
from math import ceil
import csv


class SimSystem():
    def __init__(self, nump_proc, load_interval, time_limit=100000, print=True):
        '''
        :param nump_proc: number of processors, get saved into self.k
        :param load_interval: a tuple where the 1st value is the min initial load and 2nd is max
        :param time_limit: hard time limit for the system, ends simulation after this many simulated cycles
        :param print: boolean value for if the simulation should be exported to a CSV file
        :return:
        '''
        self.loads = []
        self.processors = defaultdict(set) # A dictionary where the key is the absolute time and
                                           # the value is a set of processors scheduled to load balance at that time
        self.k = nump_proc
        self.running = []  # List for determining if a processor should stop scheduling load balancing
        self.time = 0
        self.time_limit = time_limit

        if print:
            # Sets up a file to export to and a csvWriter to simplify writing the values
            filename = "Simulation_{k}_{max_load}_{time}.csv".format(
                    k=self.k, max_load = load_interval[1], time=self.time_limit)
            self.file = open(filename, 'w', newline='')
            self.writer = csv.writer(self.file, delimiter=',')
        for i in range(nump_proc):
            # Initializes run times, loads, and cutoff(running) list
            self.processors[randrange(100, 1000)].add(i)
            self.running.append(1)
            self.loads.append(randrange(load_interval[0], load_interval[1]))

    def simulate(self):
        print("---------------------------SIMULATING---------------------------")
        self.time = min(self.processors.keys())  # Finds the lowest key (absolute time) in the schedule dictionary
        while self.time < self.time_limit:
            if self.running.count(-1) >= self.k/2:
                #  If 50% or more of the processors are done load balancing, end simulation
                print("---------------------------STABILIZED---------------------------")
                if print:
                    self.file.close()
                return
            n = self.processors[self.time]  # Need to make sure that neighbors are not running at the same time
            marked = set()
            for i in n:  # Mark neighbors that can not run during this cycle
                if i not in marked:  # Need to be sure that neighbors do not mark each other
                    if ((i + 1) % self.k) in n:
                        marked.add((i + 1) % self.k)
                    if ((i - 1) % self.k) in n:
                        marked.add((i - 1) % self.k)
            for i in marked:  # Remove marked processors from current cycle and schedule them on the next cycle
                self.processors[self.time].remove(i)
                self.processors[self.time + 1].add(i)
            ch = False  # Value to determine if anything meaningful has happened this cycle
                        # Used to determine if the cycle should be exported to the CSV file
            for i in n:
                # C = mean of processor and its neighbors
                c = mean([self.loads[i - 1], self.loads[i], self.loads[(i + 1) % self.k]])

                if self.loads[i] >= c and self.running[i] != -1:
                    # If less load than average, should not run.
                    # Second conditional should never be used but is there to be sure
                    # that no processor that has stopped scheduling runs
                    if self.loads[i - 1] < self.loads[i] and self.loads[i] > self.loads[i - 1] \
                            and (ceil(c - self.loads[(i + 1) % self.k]) + ceil(c - self.loads[i - 1])) > 10:
                        # If both processors are lower and the total amount needed to equalize is more than 10
                        ch = True
                        self.running[i] = 1  # Reset counter for meaningless cycles

                        # Next lines take load units from processor and distribute them to neighbors
                        self.loads[i] -= ceil(c - self.loads[(i + 1) % self.k]) + ceil(c - self.loads[i - 1])
                        self.loads[i - 1] += ceil(c - self.loads[i - 1])
                        self.loads[(i + 1) % self.k] += ceil(c - self.loads[(i + 1) % self.k])
                    elif self.loads[i - 1] < self.loads[i] and ceil(c - self.loads[i - 1]) > 5:
                        # If only left neighbor is lower and needs at least 5 to equalize
                        ch = True
                        self.running[i] = 1  # Reset counter for meaningless cycles
                        self.loads[i] -= ceil(c - self.loads[i - 1])
                        self.loads[i - 1] += ceil(c - self.loads[i - 1])
                    elif self.loads[i] > self.loads[i - 1] and ceil(c - self.loads[(i + 1) % self.k]) > 5:
                        # If only right neighbor is lower and needs at least 5 to equalize
                        ch = True
                        self.running[i] = 1  # Reset counter for meaningless cycles
                        self.loads[i] -= ceil(c - self.loads[(i + 1) % self.k])
                        self.loads[(i + 1) % self.k] += ceil(c - self.loads[(i + 1) % self.k])
                    else:
                        # Nothing is done this cycle, so it is meaningless
                        # (increment counter and check if it should stop)
                        self.running[i] += 1
                        if self.running[i] >= 10:
                            self.running[i] = -1
                else:
                    # Same as lines above but used for when the processor is less than the average
                    # Necessary to check since many processors get stuck not doing anything
                    # and they end up continuously rescheduling when it is not needed
                    # 10 is arbitrary and just seems to be a good cutoff in practice
                    self.running[i] += 1
                    if self.running[i] >= 10:
                        self.running[i] = -1
                if self.running[i] != -1:
                    self.processors[self.time + randrange(100, 1000)].add(i)
            self.processors.pop(self.time)  # Need to entirely remove the current time from the dictionary keys
            if print and ch:
                self.printCSV()
            self.time = min(self.processors.keys())  # Determine the next time processors are load balancing
        # Simulation will only get here if it exceeds the time limit
        print("---------------------------DID NOT STABILIZE---------------------------")
        if print:
            self.file.close()

    def printCSV(self):
        '''
        Exports the current load units in CSV format. Places the current time as the first value in the line.
        :return:
        '''
        x = [self.time]
        x.extend(self.loads)
        self.writer.writerow(x)
