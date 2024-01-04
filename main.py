from mininet.cli import CLI
from CreateTopology import run_topology
from TestingScript import TestingScript
from time import sleep
if __name__ == '__main__':
    # input for creating topology
    topology = ['', 0]
    valid = False
    while not valid:
        topology[0] = input("Enter topology type (tree, mesh, hybrid): ").lower()
        if topology[0] in ["mesh", "tree", "hybrid"]:
            valid = True
    valid = False
    while not valid:
        topology[1] = int(input("Enter topology level (1-4):"))
        if 0 < topology[1] < 5:
            valid = True
    valid = False
    while not valid:
        runs = int(input("Enter number of times you want the program to run: "))
        if runs > 0:
            valid = True
    out = 1
    while runs > 0:
        network = run_topology(topology)

        test = TestingScript(network, 20, topology[0], topology[1], out)
        network.start()
        sleep(30)
        try:
            test.run_test()

        except Exception as e:
            print("An error occurred: ", e)
        finally:
            network.stop()
        runs -= 1
        out += 1



