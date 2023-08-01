from time import sleep

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.topolib import TreeTopo
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
            self.build_tree(root, topology[1], False)
        elif topology[0] == 'mesh':
            self.build_mesh(root, topology[1])
        else:
            self.build_hybrid(root, topology[1])

    def build_tree(self, root, levels, hybrid):
        """

        :param root:
        :param levels:
        :return:
        """
        # If the tree is for a hybrid topo then increase the starting value by itself plus 1,
        # and increase the max level by 4 times. This leads to the correct outcome at all levels.
        if hybrid:
            i = levels+(levels+1)
            max_level = (levels*4)
        # Else use default starting values
        else:
            i = 1
            max_level = levels*2
        # each pass is equal to halve a level
        while i <= max_level:
            print(i)
            current = self.addSwitch(f's{i + 1}')
            self.addLink(root, current)
            node = self.addNode(f'h{i*2 - 1}')
            self.addLink(current, node)
            node = self.addNode(f'h{i*2}')
            self.addLink(current, node)
            i += 1

    def build_mesh(self, root, levels):
        # Code for a mesh topology
        # Initialise starting value for both switches and hosts
        i = 1
        j = 1
        # loop until the current level, one pass == one level
        while i <= levels:
            print(i)
            # create switch A and B for level in the mesh
            switch_a = self.addSwitch(f's{i*2}')
            switch_b = self.addSwitch(f's{i*2+1}')
            # add the links for the switches between each other and the root
            self.addLink(switch_a, switch_b)
            self.addLink(root, switch_a)
            self.addLink(root, switch_b)
            # Create the hosts and connecting them to the switches, each host is connected to both switches.
            while j <= levels*4:
                node = self.addNode(f'h{j}')
                self.addLink(switch_a, node)
                self.addLink(switch_b, node)
                j += 1
            i += 1

    def build_hybrid(self, root, levels):
        # Mixture or Mesh and tree with both having the same root switch
        # Run the mesh function first
        self.build_mesh(root, levels)
        # run the tree function with hybrid being true, so it increases the starting value and the level
        self.build_tree(root, levels, True)


def run_topology(custom_topology):
    # Create the Mininet network
    net = Mininet(topo=UserTopology(custom_topology))

    # Start the network
    net.start()
    # put a user input here so that I can launch the test when ready

    # Ping all devices, will replace this with a call to the actual testing script
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
        if topology[0] in ["mesh", "tree", "hybrid"]:
            valid = True
    valid = False
    while not valid:
        topology[1] = int(input("Enter topology level (1-4):"))
        if 0 < topology[1] < 5:
            valid = True
    run_topology(topology)
