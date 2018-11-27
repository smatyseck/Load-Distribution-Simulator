import SimSystem, sys


def main():
    '''
        Some basic test cases for when the file is ran without any command-line arguments
        Simulated {5,10,100} processors with 10-1000 initialized load units
    :return:
    '''
    S = SimSystem.SimSystem(5, (10, 1000))
    S.simulate()
    S = SimSystem.SimSystem(10, (10, 1000))
    S.simulate()
    S = SimSystem.SimSystem(100, (10, 1000))
    S.simulate()
    S = SimSystem.SimSystem(1000, (10, 1000))
    S.simulate()

if __name__ == '__main__':
    '''
        Simple command line argument parser for when specific cases are to be simulated.
    '''
    if len(sys.argv) == 5:
        S = SimSystem.SimSystem(int(sys.argv[1]),(int(sys.argv[2]),int(sys.argv[3])),int(sys.argv[4]))
        S.simulate()
    elif len(sys.argv) != 1:
        print("Invalid Number of arguments.")
        print('Proper usage is')
        print('"main.py (number of processors) (min load) (max load) (time limit)"')
        print("Or")
        print('"main.py" for default simulations')
    else:
        main()
