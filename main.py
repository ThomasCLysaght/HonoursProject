from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI


class UserTopology(Topo):
    """
    Class for the user-defined topology.
    """

    def __init__(self, topology):
        super(UserTopology, self).__init__()

        # Create root node
        root = self.addSwitch('s1')

        if topology[0] == 'tree':
            self.build_tree(root, topology[1])
        elif topology[0] == 'mesh':
            self.build_mesh(root, topology[1])
        else:
            self.build_hybrid(root, topology[1])

    def build_tree(self, root, levels):
        # I'm either going to do with recursive or with for loops
        # Each level will have 2 host, with each switch connecting to the previous level switch
        pass

    def build_mesh(self, root, levels):
        pass

    def build_hybrid(self, root, levels):
        self.build_mesh(root, levels)
        self.build_tree(root, levels)



def run_topology(topology):
    # Create the Mininet network
    net = Mininet(topo=UserTopology(topology))

    # Start the network
    net.start()

    # Ping all devices
    for host in net.hosts:
        result = net.ping([host])
        print(result)

    # Start the CLI
    CLI(net)

    # Stop the network
    net.stop()


if __name__ == '__main__':
    # input for creating topology
    topology = ['', 0]
    valid = False
    while not valid:
        topology[0] = input("Enter topology type (tree, mesh, hybrid): ").lower()
        if topology[0] == ("mesh" or "tree" or "hybrid"):
            valid = True
    valid = False
    while not valid:
        topology[1] = int(input("Enter topology level (1-4):"))
        if 0 < topology[1] < 5:
            valid = True
    run_topology(topology)
