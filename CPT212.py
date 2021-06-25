import random
import sys
import networkx as nx
import matplotlib.pyplot as plt

class Graph:

    def __init__(self):
        self.graph = {
            "Reykjavík, Iceland": [],
            "Kingston, Jamaica": [],
            "Brasília, Brazil": [],
            "Montevideo, Uruguay": [],
            "Zürich, Switzerland": []}

        self.city_list = list(self.graph.keys())
        self.distance = {

            "Reykjavík, Iceland": [("Kingston, Jamaica", 6548.22), ("Brasília, Brazil", 9160.93),
                                   ("Montevideo, Uruguay", 11416.36), ("Zürich, Switzerland", 2620.18)],
            "Kingston, Jamaica": [("Reykjavík, Iceland", 6548.22), ("Brasília, Brazil", 4905.16),
                                  ("Montevideo, Uruguay", 6268.65), ("Zürich, Switzerland", 8200.47)],
            "Brasília, Brazil": [("Reykjavík, Iceland", 9160.93), ("Kingston, Jamaica", 4905.16),
                                 ("Montevideo, Uruguay", 2280.56), ("Zürich, Switzerland", 8983.79)],
            "Montevideo, Uruguay": [("Reykjavík, Iceland", 11416.36), ("Kingston, Jamaica", 6268.65),
                                    ("Brasília, Brazil", 2280.56), ("Zürich, Switzerland", 11185.49)],
            "Zürich, Switzerland": [("Reykjavík, Iceland", 2620.18), ("Kingston, Jamaica", 8200.47),
                                    ("Brasília, Brazil", 8983.79), ("Montevideo, Uruguay", 11185.49)]}

    def add_edge(self, source, adjacent_city):

        edge_to_add = []
        edge_to_add.append(adjacent_city)

        for distance_city in self.distance[source]:
            if adjacent_city == distance_city[0]:
                distance = distance_city[1]
                edge_to_add.append(distance)
        distance_pair = tuple(edge_to_add)
        self.graph[source].append(distance_pair)

    def print_graph(self):

        for city in self.graph.keys():
            print(city)
            for all_city in self.graph[city]:
                print(all_city)
            print("\n")

        
    def visualize_graph(self):
        
        all_edges = []
        for depart in self.graph.keys():
            for destinate_dist in self.graph[depart]:
                temp = [depart, destinate_dist[0], destinate_dist[1]]
                all_edges.append(temp)
        
        G = nx.DiGraph()
        G.add_weighted_edges_from(all_edges) #define G
        fixed_positions = {"Reykjavík, Iceland":(3,3) , "Kingston, Jamaica":(1,2), "Brasília, Brazil":(2,1), "Montevideo, Uruguay":(4,1), "Zürich, Switzerland":(5,2)}#dict with two of the positions set
        fixed_nodes = fixed_positions.keys()
        pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
        nx.draw_networkx(G, pos, font_size=8)
        edge_labels = dict()
        for i in range(len(all_edges)):
            data = {(all_edges[i][0], all_edges[i][1]): all_edges[i][2]}
            edge_labels.update(data)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        plt.show()
        
#--------------------------------------------------------

    def check_connectivity(self)->bool:

        visited=["unexplored"]*len(self.city_list)
        self.check_connectivity_dfs(self.city_list[0],visited)
        for visit in visited:
            if visit == "unexplored":
                return False
        return True

    def check_connectivity_dfs(self,source,visit_track)->None:
        visit_track[self.city_list.index(source)]=True
        current=self.graph[source]

        for city in current:
            if visit_track[self.city_list.index(city[0])]=="visited":
                return
            elif visit_track[self.city_list.index(city[0])]=="unexplored":
                visit_track[self.city_list.index(city[0])]="visited"
                self.check_connectivity_dfs(city[0],visit_track)

    def generate_random_edge(self)->None:

        list_of_city = self.city_list.copy()
        source = random.choice(list_of_city)
        list_of_city.remove(source)
        edge=list_of_city.copy()

        for random_edge in list_of_city:
            if self.adjacent_to(source,random_edge):
                edge.remove(random_edge)

        if len(edge)==0:
            return
        else:
            chosen_edge=random.choice(edge)
            self.add_edge(source,chosen_edge)

    def adjacent_to(self,source,random_edge)->bool:
        current=self.graph[source]

        for city in current:
            if city[0]==random_edge:
                return True

    def get_current(self):
        return self.graph

    def reverse_graph(self,ref_graph):

        for city in self.city_list:
            #print(city)
            for adjacent_city in ref_graph.get_current()[city]:
                if ref_graph.adjacent_to(city,adjacent_city[0]) and not self.adjacent_to(adjacent_city[0],city) and city != adjacent_city[0] :
                    self.add_edge(adjacent_city[0],city)

#-----------------------------------------------------------------------------------------
    def cycle_detection(self)->bool:

        visited=["unexplored"]*len(self.city_list)
        list_of_city=[]

        for city in self.city_list:

            if self.cycle_dfs(city,list_of_city,visited):
                self.print_cycle(list_of_city,visited)

                return True
            list_of_city.clear()
            visited=["unexplored"]*len(self.city_list)
        return False

    def cycle_dfs(self,source,path_track,visited)->bool:
        visited[self.city_list.index(source)]="visited"
        current=self.graph[source]
        path_track.append(source)

        for adjacent_city in current:
            if visited[self.city_list.index(adjacent_city[0])]=="unexplored":
                if self.cycle_dfs(adjacent_city[0],path_track,visited):
                    return True
            elif visited[self.city_list.index(adjacent_city[0])]=="visited":
                path_track.append(adjacent_city[0])
                return True
        visited[self.city_list.index(source)]="unreachable"
        return False

    def print_cycle(self,path_track,visited):

        path=len(path_track)
        
        print("\n")
        for city in path_track:

            path=path-1
            if path == 0:
                print(city,end=" ")
                break
            if visited[self.city_list.index(city)]!="unreachable":
                print(city,end=" -> ")
        

#--------------------------------------------------------------------------
    def shortest_path(self,source,destination)->None:

        visited=[False]*len(self.city_list)
        shortest_distance=[sys.maxsize]*len(self.city_list)

        shortest_distance[self.city_list.index(source)]=0
        list_city=self.city_list.copy()
        path_track=["unknown"]*len(self.city_list)

        while len(list_city) > 0:

            selected_city=self.find_min_distance(visited,shortest_distance)
            visited[selected_city]=True

            current=self.graph[self.city_list[selected_city]]

            for adjacent_city in current:
                index=self.city_list.index(adjacent_city[0])
                if visited[index]==False and shortest_distance[selected_city]+adjacent_city[1]<shortest_distance[index]:
                    shortest_distance[index]=shortest_distance[selected_city]+adjacent_city[1]
                    path_track[self.city_list.index(adjacent_city[0])]=self.city_list[selected_city]

            list_city.pop()

        print(shortest_distance)
        self.print_path(path_track,shortest_distance,source,destination)

    def print_path(self,path_track,shortest_distance,source,destination)->None:

        path_store=[]
        path_store.append(destination)
        while True:

            dest = self.city_list.index(destination)
            predecessor = path_track[dest]
            path_store.append(predecessor)
            if predecessor==source:
                break
            else:
                destination=predecessor


        for path in range(len(path_store)):
            if len(path_store)-path-1==0:
                print(path_store[0],end=" ")
                break
            print(format(path_store[len(path_store)-path-1]),end='->')
        print("\n")

    def find_min_distance(self,visited,shortest_distance)->int:

        min=sys.maxsize
        min_index=0

        for city in self.city_list:

            if visited[self.city_list.index(city)]==False and shortest_distance[self.city_list.index(city)]<min:
                min=shortest_distance[self.city_list.index(city)]
                min_index=self.city_list.index(city)
        return min_index

    def clear(self)->None:

        for city in self.city_list:
            self.graph[city].clear()



def initialize():

    default_graph.add_edge("Reykjavík, Iceland","Zürich, Switzerland")
    default_graph.add_edge("Kingston, Jamaica","Reykjavík, Iceland")
    default_graph.add_edge("Brasília, Brazil","Kingston, Jamaica")
    default_graph.add_edge("Montevideo, Uruguay","Reykjavík, Iceland")
    default_graph.add_edge("Montevideo, Uruguay","Brasília, Brazil")
    default_graph.add_edge("Montevideo, Uruguay","Zürich, Switzerland")

default_graph=Graph()
initialize()
reverse_graph_image = Graph()
reverse_graph_image.reverse_graph(default_graph)

while True:

    print("----------------------------------------------------------")
    print("|   1. Graph Connectivity                                |")
    print("|   2. Cycle detection                                   |")
    print("|   3. Shortest path                                     |")
    print("|   4. Reset                                             |")
    print("|   5. exit                                              |")
    print("----------------------------------------------------------")
    choice=int(input("Enter your choice:"))
    if choice == 1:
        i=0

        while not default_graph.check_connectivity() or not reverse_graph_image.check_connectivity():
            if i==0:
                print("not strongly connected")
                print("generating random edge...")
                i=i+1
            default_graph.generate_random_edge()
            reverse_graph_image.reverse_graph(default_graph)

        default_graph.print_graph()
        default_graph.visualize_graph()
        print("---------------")

        reverse_graph_image.print_graph()
        reverse_graph_image.visualize_graph()
        
    if choice == 2:
        
        default_graph.visualize_graph()
        while not default_graph.cycle_detection():
            if (default_graph.cycle_detection() == False):
                print("The graph has no cycle.")
                default_graph.generate_random_edge()
                input("Press enter to continue generating an new edge :)")
                print("Start generating an new edge...")
        print("\nCycle found! Above is the path of the cycle detected.\n")
        default_graph.visualize_graph()

    if choice == 3:

        while not default_graph.check_connectivity() or not reverse_graph_image.check_connectivity() :
            default_graph.generate_random_edge()
            reverse_graph_image.reverse_graph(default_graph)
        #source=int(input("Enter your source vertex"))
        #destination=int(input("Enter your destination vertex"))

        default_graph.shortest_path("Reykjavík, Iceland", "Brasília, Brazil")
        default_graph.print_graph()
        default_graph.visualize_graph()

    if choice == 4:

        default_graph.clear()
        reverse_graph_image.clear()

        initialize()
        reverse_graph_image.reverse_graph(default_graph)
        default_graph.visualize_graph()

    if choice == 5:
        break

