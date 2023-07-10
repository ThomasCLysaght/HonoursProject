from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI


class UserTopology(Topo):
    """
    Class for the user-defined topology.
    """

    def __init__(self, topology):
        super(UserTopology, self).__init__()

        # Parse the topology string
        switches, hosts, links = topology.split(';')
        switches = switches.split(',')
        hosts = hosts.split(',')
        links = links.split(',')

        # Add switches to topology
        for switch in switches:
            self.addSwitch(switch)

        # Add hosts to topology
        for host in hosts:
            self.addHost(host)

        # Add links to topology
        for link in links:
            src, dst = link.split('-')
            self.addLink(src, dst)

    def build(self):
        pass


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
    topology = input("Enter topology (switches,hosts,links): ")
    run_topology(topology)