'''
Light-weight stats gathering tool to display cpu usage and network traffic.
Typical use through an SSH window from a host, so we want both the cpu and
network load to be minimal.  This program is kept simple with minimal bells
and whistles.
'''
import sys
import time

# set up paths to various system components
CPU_FILE = "/proc/stat"
GPU_FILE = "/sys/devices/gpu.0/load"
MEM_FILE = "/proc/meminfo"
NET_RX = "/sys/class/net/wlan0/statistics/rx_bytes"
NET_TX = "/sys/class/net/wlan0/statistics/tx_bytes"

NET_AVE = 2     # number of seconds to average network data

'''
Accumulate cpu statistics for reporting
'''
class CpuUsage():
    def __init__(self):
        self.cpu_busy = 0   # cpu busy cycles since power up (10 ms intervals)
        self.cpu_total = 0  # total cpu cycles since power up (10 ms intervals)
        self.cur_usage = 0  # usage in %

    def update(self, cur_stats):
        # cur_stats is a string for the cpu containing various cycle counts
        # strip out the list of cpu cycles in string
        cycles = [int(n) for n in cur_stats.split() if n.isdigit()]

        # first four numbers represent USER, NICE, SYS, IDLE cpu operations
        cpu_busy = sum(cycles[0:3])
        cpu_total = sum(cycles[0:4])
        if cpu_total == self.cpu_total:
            return      # processor updates didn't occur, ignore updating ours
        self.cur_usage = int(100 * (cpu_busy-self.cpu_busy) /
                                   (cpu_total-self.cpu_total))
        # save values for differencing the next pass
        self.cpu_busy = cpu_busy
        self.cpu_total = cpu_total

    def getUsage(self):
        return self.cur_usage

'''
Accumulate network traffic information for reporting
'''
class NetStat():
    def __init__(self):
        self.net_data = [[0,0]] * NET_AVE
        self.rate = [0,0]       # rx, tx rate in KB/s

    def update(self, rx_bytes, tx_bytes):
        self.rate[0] = (rx_bytes - self.net_data[NET_AVE-1][0]) // \
                        (NET_AVE * 1000)
        self.rate[1] = (tx_bytes - self.net_data[NET_AVE-1][1]) // \
                        (NET_AVE * 1000)
        # insert the new net data at beginning of list
        self.net_data.insert(0, [rx_bytes, tx_bytes])
        # remove last item on list
        del self.net_data[-1]

    def getUsage(self):
            return self.rate

def main():
    print("starting...")

    net_stat = NetStat()
    cpu_list = dict([(i, CpuUsage()) for i in range(4)])
    time.sleep(2.1)

    while True:
        # grab the cpu data
        with open(CPU_FILE, "r") as f:
            f.readline()            # Read and discard first line.
            for i in range(4):      # Read each cores information
                s = f.readline()    # get line of cpu data
                cpu_list[i].update(s)

        # grab the GPU data
        with open(GPU_FILE) as f:
            gpu_line = int(f.read()) // 10  # Usage in %

        # Get memory utilization
        # In the memory file the following line contain wanted information
        #    0 - MemTotal
        #    2 - MemAvailable
        #   14 - SwapTotal
        #   15 - SwapFree
        mem_data = list()
        with open(MEM_FILE, "r") as f:
            for i, line in enumerate (f):
                if i in [0, 2, 14, 15]:
                    # Extract numerical data, the first (only) number is value
                    # wanted. It's in KB.
                    numlist = [int(n) for n in line.split() if n.isdigit()]
                    mem_data.append(numlist[0] // 1024)
                if i >= 15:
                    break

        # grab the network data
        with open(NET_RX) as f:
            rx_bytes = int(f.read())
        with open(NET_TX) as f:
            tx_bytes = int(f.read())
        net_stat.update(rx_bytes, tx_bytes)

        # format and output the usage data
        if sys.stdout.isatty():
            # Clear screen & move cursor to home postion then print title
            print ("\033[H\033[J   NVIDIA JETSON NANO STATS   ")
        rate = net_stat.getUsage()
        print("wlan0 rx:{:5d} (KB/s)  tx:{:5d} (KB/s)\n".format(rate[0], rate[1]))

        print("CPU ", end='')
        for i in range(4):
             print("({}): {:3d} %  ".format(i, cpu_list[i].getUsage()), end='')

        print("\n\nGPU: {:3d} %".format(gpu_line))

        print("\nRAM:  {:4d}/{:4d} MB".format(mem_data[0]-mem_data[1], \
                                              mem_data[0]))
        print("SWAP: {:4d}/{:4d} MB".format(mem_data[2]-mem_data[3], \
                                            mem_data[2]))

        time.sleep(1)

if __name__ == '__main__':
    main()

