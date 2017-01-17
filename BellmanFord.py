"""
This class is for BellmanFord Algorithm Calculations
 Pooya Khandel, Mohammad Hussein Tavakoli Bina
"""

from socket import *
import math
import re


class BFA:
    def __init__(self, r_count, first_cost, my_name, which_port, adr_to_name):
        self.use_who = dict()
        self.new_pm = None
        self.pm_adr = None
        self.first_cost = first_cost
        self.old_pm = {}
        self.ports = which_port
        self.my_port = which_port[my_name]
        self.name = my_name
        self.r_count = r_count
        self.adr_to_name = adr_to_name
        self.table = []
        self.lie_table = []
        self.init_tables()
        self.bf_show()
        self.permission = []
        self.router_sock = socket(AF_INET, SOCK_DGRAM)
        self.router_sock.bind(('', self.my_port))
        self.sock_ip = '127.0.0.1'
        self.router_sock.settimeout(0.5)

    def init_tables(self):
        for m in range(self.r_count):
            self.table.append([])
            self.lie_table.append([])
            for n in range(self.r_count):
                self.table[m].append('N')
                self.lie_table[m].append(self.first_cost[n])
        for m in range(self.r_count):
            self.table[int(self.name) - 1][m] = self.first_cost[m]
            if self.first_cost[m] == 'N':
                self.use_who[m + 1] = '@N'
            else:
                self.use_who[m + 1] = str(m + 1)

    def who_to_send(self):
        self.permission.clear()
        for m in range(self.r_count):
            if self.table[int(self.name) - 1][m] == 'N':
                self.permission.append(False)
            else:
                self.permission.append(True)

    def send(self):
        message = str()
        for sending_router in range(self.r_count):
            if self.permission[sending_router]:
                if not(sending_router + 1 == int(self.name)):
                    for m in range(self.r_count):
                        message = message + self.lie_table[sending_router][m] + '@'
                    self.router_sock.sendto(bytes(message, 'UTF-8'),
                                            (self.sock_ip, self.ports[str(sending_router + 1)]))
                    message = str()

    def receive(self):
        try:
            message, client_address = self.router_sock.recvfrom(2048)
            self.new_pm = re.split("@", message.decode())
            self.new_pm.remove('')
            self.pm_adr = client_address[1]
            if self.pm_adr in list(self.old_pm.keys()):
                if not(self.old_pm[self.pm_adr] == self.new_pm):
                    self.old_pm[self.pm_adr] = self.new_pm
                    self.table[self.adr_to_name[self.pm_adr] - 1] = self.new_pm
                    print("router {} send new update: {}".format(self.pm_adr, self.new_pm))
                    self.do_alg()
            else:
                self.old_pm[self.pm_adr] = self.new_pm
                self.table[self.adr_to_name[self.pm_adr] - 1] = self.new_pm
                print("router {} send new update: {}".format(self.pm_adr, self.new_pm))
                self.do_alg()
        except:
            pass

    def do_alg(self):
        distance = []
        for d_r_iter in range(self.r_count):
            if not(int(self.name) - 1 == d_r_iter):
                # Determine current cost to destination router
                if self.table[int(self.name) - 1][d_r_iter] == 'N':
                    temp = math.inf
                else:
                    temp = float(self.table[int(self.name) - 1][d_r_iter])
                for c_r_iter in range(self.r_count):
                    if self.first_cost[c_r_iter] == 'N':
                        cost1 = math.inf
                    else:
                        cost1 = float(self.first_cost[c_r_iter])
                    if self.table[c_r_iter][d_r_iter] == 'N':
                        cost2 = math.inf
                    else:
                        cost2 = float(self.table[c_r_iter][d_r_iter])
                    distance.append(cost1 + cost2)
                min_dis = min(distance)
                if min_dis < temp:
                    self.table[int(self.name) - 1][d_r_iter] = str(int(min_dis))
                    for m in range(self.r_count):
                        self.lie_table[m][d_r_iter] = str(int(min_dis))
                    min_through = distance.index(min_dis)
                    self.use_who[d_r_iter + 1] = str(min_through + 1)
                    lie_to = min_through
                    self.lie_table[lie_to][d_r_iter] = 'N'
                distance.clear()
        self.bf_show()

    def bf_show(self):
        print("\nThe Cost Tabel of router {} is :".format(self.name))
        print("        ", end="")
        for h in range(self.r_count):
                print("{:<5}".format(h + 1), end="")
        print("\n---------------------------------")
        for row in range(self.r_count):
            print("{}|      ".format(row + 1), end="")
            for col in range(self.r_count):
                if row == int(self.name) - 1:
                    print("{:<2}\{:<5}".format(self.table[row][col], self.use_who[col + 1]), end="")
                else:
                    print("{:<8}".format(self.table[row][col]), end="")
            print()
        print("--------------------------------------------------------")

    def check_cost(self, new_cost):
        if self.table[int(self.name) - 1] == new_cost:
            print("No Cost Change!")
        else:
            # 1- update its row for new costs
            # 2- update lie table
            # 3- update use who
            # 4- update permissions
            # 5- solve pp cost
            # 6- do alg()
            # 7- show the results
            print("link costs of router {} is changed!".format(self.name))
            self.table[int(self.name) - 1] = new_cost
            self.lie_table = []
            for m in range(self.r_count):
                self.lie_table.append([])
                for n in range(self.r_count):
                    self.lie_table[m].append(new_cost[n])
            for m in range(self.r_count):
                if new_cost[m] == 'N':
                    self.use_who[m + 1] = '@N'
                else:
                    self.use_who[m + 1] = str(m + 1)
            self.who_to_send()
            self.do_alg()
