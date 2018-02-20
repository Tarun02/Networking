#Network Assignment-2
#By Tarun Prasad Yerneni and Vidika Badal

from math import *
from collections import *
import sys


global successful_packets
global blocked_packets
global blocked_counter

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def adjacent_list(self):
        return [x.id for x in self.adjacent.keys()]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


def file_opening(file):
    file_open = open(file,'r').readlines()
    some_tuples = []
    for i in file_open:
        x = i.rstrip()
        some_tuples.append(tuple(x.split(" ")))
    return some_tuples

def getting_vertices(s):
    vertex_list = []
    for i in s:
        for j in range(2):
            if i[j] not in vertex_list:
                vertex_list.append(i[j])
    return vertex_list

def delay_graph(v,w):
    network_graph = Graph()
    for i in v:
        network_graph.add_vertex(i)
    for j in w:
        network_graph.add_edge(j[0],j[1],int(j[2]))
    return network_graph

def dijkstra_algorithm(type_of_routing,network_delay_graph,work_tup,
                       update_dict,p,c):\

    if type_of_routing == "SHP":
        success,blocked,hops,bc,cd = shp(network_delay_graph,work_tup,update_dict,p)
    elif type_of_routing == "SDP":
        success,blocked,hops,bc,cd = sdp(network_delay_graph,work_tup,update_dict,p)
    elif type_of_routing == "LLP":
        success,blocked,hops,bc,cd = llp(network_delay_graph,work_tup,update_dict,p,c)
    return success,blocked,hops,bc,cd  

def path_find(graph,source,destination,path):
    source = graph.get_vertex(source)
    s = source.get_id()
    destination = graph.get_vertex(destination)
    d = destination.get_id()
    path = path+[s]
    if source == destination:
        return [path]

    if not source.adjacent_list():
        return []
    paths = []
    adj = source.adjacent_list()
    for node in adj:
        if node not in path:
            all_paths = path_find(graph,node,d,path)
            for p in all_paths:
                paths.append(p)
    return paths

def shp(g,w,u,pr):
    blocked_counter = 0
    successful_packets = 0
    blocked_packets = 0
    hops = 0
    cummulative_delay = 0
    for i in w:
        shortest_path = None
        path_needed = path_find(g,i[1],i[2],[])
        for j in path_needed:
            if not shortest_path or (len(j) < len (shortest_path)):
                shortest_path = j
        
        u,Flag,packets,h,cummulative = evaluating_path(g,shortest_path,i,u,pr)
        if Flag == 0:
            successful_packets += packets
            hops += h
            cummulative_delay += cummulative
        elif Flag == 1:
            blocked_packets += packets
            blocked_counter += 1
                   
    return successful_packets,blocked_packets,hops,blocked_counter,cummulative_delay

def sdp(g,w,u,pr):
    blocked_counter = 0
    successful_packets = 0
    blocked_packets = 0
    hops = 0
    cummulative_delay = 0
    for i in w:
        shortest_path = None
        path_needed = path_find(g,i[1],i[2],[])
        for j in path_needed:
            weight = 0
            for k in range(len(j)-1):
                ains = g.get_vertex(j[k])
                tyree = g.get_vertex(j[k+1])
                weight = weight + ains.get_weight(tyree)
            if not shortest_path or (weight < min_weight):
                min_weight = weight
                shortest_path = j

        u,Flag,packets,h,cummulative = evaluating_path(g,shortest_path,i,u,pr)
        if Flag == 0:
            successful_packets += packets
            hops += h
            cummulative_delay += cummulative
        elif Flag == 1:
            blocked_packets += packets
            blocked_counter += 1

    return successful_packets,blocked_packets,hops,blocked_counter,cummulative_delay

def llp(g,w,u,pr,cd):
    blocked_counter = 0
    successful_packets = 0
    blocked_packets = 0
    hops = 0
    cummulative_delay = 0
    for i in w:
        shortest_path = None
        path_needed = path_find(g,i[1],i[2],[])
        for j in path_needed:
            load = 0
            for k in range(len(j)-1):
                path_key = tuple(sorted([j[k],j[k+1]])) 
                active_circuits = cd[path_key] - u[path_key][0]
                load = load + active_circuits/cd[path_key]
            if not shortest_path or load < least_load:
                least_load = load
                shortest_path = j

        u,Flag,packets,h,cummulative = evaluating_path(g,shortest_path,i,u,pr)
        if Flag == 0:
            successful_packets += packets
            hops += h
            cummulative_delay += cummulative
        elif Flag == 1:
            blocked_packets += packets
            blocked_counter += 1

    return successful_packets,blocked_packets,hops,blocked_counter,cummulative_delay
        
def evaluating_path(g,sp,op,pd,r):
    stack_path_time = Stack()
    Flag = 0
    hops = 0
    c_d = 0
    for k in range(len(sp)-1):
        path_key = tuple(sorted([sp[k],sp[k+1]]))
        if len(pd[path_key]) > 1:
            pd[path_key] = [pd[path_key][0]] + sorted(pd[path_key][1:])

        index = 0
        counter = 0
        for t in range(1,len(pd[path_key])):
            if float(op[0]) > pd[path_key][t]:
                counter += 1
            else:
                index = t
                break

        pd[path_key][0] = pd[path_key][0] + counter
        pd[path_key] = [pd[path_key][0]] + pd[path_key][index:]
        if pd[path_key][0] != 0:
            stack_path_time.push([path_key,float(op[0])+float(op[3])])
        else:
            Flag = 1
            break

    if Flag == 0:
        while not stack_path_time.isEmpty():
            req_path_time = stack_path_time.pop()
            vidika = g.get_vertex(req_path_time[0][0])
            tarun = g.get_vertex(req_path_time[0][1])
            c_d = c_d + vidika.get_weight(tarun)
            pd[req_path_time[0]].append(req_path_time[1])
            pd[req_path_time[0]][0] -= 1
        packets = int(float(op[3])*r)
        hops = len(sp) - 1
    elif Flag == 1:
        packets = int(float(op[3])*r)
        while not stack_path_time.isEmpty():
            blocked_path_time = stack_path_time.pop()
            pd[blocked_path_time[0]][0] += 1

    return pd,Flag,packets,hops,c_d    


network_scheme = str(sys.argv[1])
routing_scheme = str(sys.argv[2])
file_name = sys.argv[3]
workload_file = sys.argv[4]
packet_rate = int(sys.argv[5])


####Topology File
topology_tuples = file_opening(file_name)
resources_dict = defaultdict(list)
capacity_dict = {}
for i in topology_tuples:
    key = tuple(sorted([i[0],i[1]]))
    resources_dict[key].append(int(i[3]))
    capacity_dict[key] = int(i[3])
vertices = getting_vertices(topology_tuples)
network_delay_graph = delay_graph(vertices, topology_tuples)
####
vc = 0
if network_scheme == "CIRCUIT":
    workload_tuples = file_opening(workload_file)
    vc = len(workload_tuples)
    s_packets,b_packets,total_hops,blocked_counter,delay =dijkstra_algorithm(routing_scheme,
                                                network_delay_graph,workload_tuples,resources_dict,packet_rate,capacity_dict) \

elif network_scheme == "PACKET":
    file_open = open(workload_file,'r').readlines()
    workload_tuples = []
    for i in file_open:
        x = i.rstrip()
        vc += 1
        list_unknown = x.split(" ")
        number_of_packets = floor(float(list_unknown[3])*packet_rate)
        for j in range(number_of_packets):
            list_unknown[0] = round(float(list_unknown[0]),2)
            final_time = round(1/packet_rate,2)
            list_unknown[3] = final_time
            workload_tuples.append(tuple(list_unknown))
            list_unknown[0] = list_unknown[0] + final_time

    s_packets,b_packets,total_hops,blocked_counter,delay =dijkstra_algorithm(routing_scheme,
                                                network_delay_graph,workload_tuples,resources_dict,packet_rate,capacity_dict) \

    

###Printing all the statments											
print("total number of virtual circuit requests:",vc)
print("total number of packets:",s_packets + b_packets)
print("number of successfully routed packets:",s_packets)
print("percentage of successfully routed packets:",round((s_packets*100)/(s_packets+b_packets),2))
print("number of blocked packets:",b_packets)
print("percentage of blocked packets:",round((b_packets*100)/(s_packets+b_packets),2))
print("average number of hops per circuit:",round(total_hops/(len(workload_tuples)-blocked_counter),2))
print("average cumulative propagation delay (ms) per circuit:",round(delay/(len(workload_tuples)-blocked_counter),2))
####


        
