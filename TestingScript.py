import csv
from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from time import sleep
import math
import random


class TestingScript():
    def __init__(self, network, interval, topo, level, out):
        self.network = network
        self.output = out
        self.interval = interval
        self.topo = topo
        self.level = level
        self.host_table = []
        for host in self.network.hosts:
            self.host_table.append([host.name, host.IP()])

    def run_test(self):
        """
        Run the test
        :return:
        """
        # I'm assuming you will set up the topology elsewhere and pass it as a parameter
        # For this example, I'm just creating a simple topology here.

        print(self.host_table)
        rel=0
        iteration = 0
        with open('{topo}_level_{level}_test_{number}_output'.format(topo=self.topo, level=self.level, number=self.output), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['iteration', 'Source', 'Target', 'Packets Transmitted', 'Packets Received',
                             'Packet Loss (%)', 'RTT Min (ms)', 'RTT Avg (ms)', 'RTT Max (ms)', 'RTT Mdev (ms)'])

            while len(self.network.links) > 0 and rel < 1:

                self.remove_link(iteration)

                results = self.ping_all_hosts()
                print(results)
                loss_total = 0
                for (source, target), result in results.items():
                    transmitted, received, loss, rtt_min, rtt_avg, rtt_max, rtt_mdev = self.parse_ping_result(result)
                    loss_total += loss
                    writer.writerow([iteration, source, target, transmitted, received, loss, rtt_min, rtt_avg, rtt_max, rtt_mdev])
                rel = (loss_total)/(len(self.network.hosts)*(len(self.network.hosts)-1))
                print(rel)
                iteration = iteration + 1
                sleep(self.interval)



    def remove_link(self, iteration):
        """
        Remove the
        :param iteration:
        :return:
        """
        removal = []
        hazard_rate = self.cal_hazard_chance(iteration)
        # loops through all links in the network calculating a random value, if it above the success rate then it fails
        # i.e hazard_rate = 0.8, link will fail if failure_result is above 0.8
        # For now only one link can fail at a time though can be configured to allow more
        for link in self.network.links:
            failure_result = random.uniform(0, 1)
            if failure_result > hazard_rate:
                print("Fail result = ", failure_result)
                removal.append(link)
        if len(removal) > 0:
            print("Link removed")
            self.network.delLink(random.choice(removal))

    def cal_hazard_chance(self, iteration):
        return math.exp(-0.25 * float(iteration))


    def parse_ping_result(self, result):
        """
        Parse the ping result to extract useful statistics.
        """
        transmitted, received, loss = 0, 0, 0.0
        rtt_min, rtt_avg, rtt_max, rtt_mdev = 0.0, 0.0, 0.0, 0.0

        for line in result:
            if "packets transmitted" in line:
                details = line.split(",")
                transmitted = int(details[0].split()[0])
                received = int(details[1].split()[0])
                loss = float(details[2].split("%")[0].strip().split()[0])
                if loss > 1:
                    loss = loss/100
            if "rtt min/avg/max/mdev" in line:
                rtt = line.split('=')[1].strip().split()[0].split('/')
                rtt_min, rtt_avg, rtt_max, rtt_mdev = map(float, rtt)
            if "Network is unreachable" in line:
                transmitted = 1
                loss = 1.0


        return transmitted, received, loss, rtt_min, rtt_avg, rtt_max, rtt_mdev

    def ping_all_hosts(self):
        """
        Ping between all hosts in the network.
        Returns a dictionary with the results.
        """
        #print(self.network.pingAll())
        results = {}
        # Using a List to hold hostname and IP so that the network is still tested with unreachable hosts
        for source in self.host_table:
            for target in self.host_table:
                if source[0] != target[0]:
                    # We can use the cmd method of a host to run a ping command
                    result = self.network.get(source[0]).cmd('ping -c 1 %s' % target[1]).split('\n')[-3:]
                    results[(source[0], target[0])] = result
        return results


def remove_links(link):
    """
    Remove all links that aren't connected to hosts.
    """
    network.delLink(link)





if __name__ == "__main__":
    # This is just a basic example. In a real-world scenario, you'd want to
    # design your topology or load it from a file.
    # For the sake of demonstration, let's use a simple linear topology
    from mininet.topo import LinearTopo


    topo = LinearTopo(k=3)  # 3 hosts and 2 switches connected linearly
    print(topo.links())
    network = Mininet(topo=topo, switch=OVSSwitch)
    test = TestingScript(network, 20, 'linear', 1, 1)
    network.start()
    sleep(20)
    try:
        test.run_test()
    except Exception as e:
        print("error: ", e)
    finally:
        network.stop()
