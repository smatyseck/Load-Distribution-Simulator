import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import os


def animated_barplot():
    '''
        Function used by a canvas to turn a csv sim file into a pseudo-animated graph (has no history and
        is quite primitive).
        It uses a global filename declare within this file.
        Ideally not to be used outside of this file since the script below sets up everything in a specific way.
    :return:
    '''
    global filename
    file = open(filename)
    try:
        num_lines = sum(1 for line in open(filename))  # Count the number of lines so the number of frames is known
        v = int(filename.split(sep="_")[1])  # Determines simulation arguments from the filename where v=num processors
        rects = plt.bar(range(v), int(filename.split(sep="_")[2]), align='center') # Creates v rectangles
        for i in range(num_lines):  # Iterates through each recorded cycle in the simulation (frames)
            if i == 1:
                plt.savefig('{}_before.png'.format(v))
            if i == num_lines - 1:
                plt.savefig('{}_after.png'.format(v))
            x = file.readline().strip().split(sep=',')  # Current Time is the first value in a line
            plt.title('Time: {}'.format(x[0]), fontsize=12)  # Uses current time to format title
            x = x[1:]  # Need to remove the time so that only load units remain
            for rect, h in zip(rects, x):  # Iterates through all rectangles, updating their load unit values
                rect.set_height(int(h))
            fig.canvas.draw()
            plt.pause(0.001 / v)
        file.close()
    except:
        file.close()
        exit(0)


'''
    A bit of command line interface. Scans current directory for csv files and lists them out.
    User can then select the file with the number that appears next to the file.

    I.E.

    What CSV file would you like to animate?
    (1) Simulation_100_1000_100000.csv
    (2) Simulation_10_1000_100000.csv
    (3) Simulation_5_1000_100000.csv
    Enter your choice: 1

    This chooses the file Simulation_100_1000_100000.csv.

    The file is then animated on a bar graph
'''

csvs = []
for f in os.listdir("."):
    if f.endswith(".csv"):
        csvs.append(f)
while True:
    try:
        print("What CSV file would you like to animate?")
        for i in range(len(csvs)):
            print("({i}) {filename}".format(i=i + 1, filename=csvs[i]))

        num = int(input("Enter your choice: ")) - 1
        filename = csvs[num]
        break
    except:
        print("Invalid Input")
fig = plt.figure()
plt.xlabel('Processor Number', fontsize=12)
plt.ylabel('Load Units', fontsize=12)
plt.title('Time: 0', fontsize=16)
win = fig.canvas.manager.window
win.after(100, animated_barplot)
plt.show()

