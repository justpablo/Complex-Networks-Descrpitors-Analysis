
"""
Name: Structural Descriptors of Complex Networks
Author: Pablo Eliseo Reynoso Aguirre
Date: March 19, 2017
Desrcription: The task involves the calculation of the following structural descriptors of complex networks:

                a) Number of nodes
                b) Number of edges
                c) Minimum, maximum and average degree
                d) Average clustering coefficient (average of the clustering coefficients of each node)
                e) Assortativity
                f) Average path length (average distance between all pairs of nodes)
                g) Diameter (maximum distance between nodes in the network)

                NOTE: The descriptors should be extracted from the networks from the three categories:
                toy (sample networks), model (networks generated from models), and real (real networks).



"""


import networkx as nx;
import matplotlib.pyplot as plt;
import csv;
import os;
import numpy as np;



class NetworksDescriptors():

    def graph_descriptor_extractor(self, network_path):

        G = nx.read_pajek(network_path);

        G_is_directed = nx.is_directed(G);

        if G_is_directed:
            G = nx.DiGraph(G);
        else:
            G = nx.Graph(G);

        G_nodes = G.nodes();
        G_edges = G.edges();

        G_num_nodes = len(G_nodes); "Descriptor a) number of nodes"
        G_num_edges = len(G_edges); "Descriptor b) number of edges"

        sorted_degrees = sorted(nx.degree(G).values());
        G_min_degree = sorted_degrees[0];  "Descriptor c.i) minimum"
        G_max_degree = sorted_degrees[-1]; "Descriptor c.ii) maximum"

        if G_is_directed:
            G_avg_degree = G_num_edges / float(G_num_nodes); "Descriptor c.iii) average"
        else:
            G_avg_degree = 2.0 * G_num_edges / float(G_num_nodes); "Descriptor c.iii) average"

        G_assortativity = nx.degree_pearson_correlation_coefficient(G); "Descriptor e) Assortativity"
        G_avg_clustering = nx.average_clustering(G); "Descriptor d) Average clustering coefficient"
        G_avg_path_length = nx.average_shortest_path_length(G); "Descriptor f) Average path length"
        G_diameter = nx.diameter(G); "Descriptor g) Diameter"

        return [G_num_nodes, G_num_edges, G_min_degree, G_max_degree, G_avg_degree, G_assortativity, G_avg_clustering, G_avg_path_length, G_diameter];

    def print_graph_descriptors(self, graph_descriptors, descriptor_labels):

        print "-------------------------------------"
        for i in range(len(graph_descriptors)):
            print "| " + descriptor_labels[i] +": "+ str(graph_descriptors[i]);
        print "-------------------------------------"

    def generate_descriptors_csv(self, descriptors_labels, network_descriptors):

        file_path = "A1_nets/networks_descriptors.csv";
        if os.path.isfile(file_path):

            with open(file_path, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(network_descriptors)
        else:

            with open(file_path, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(descriptors_labels)
                writer.writerow(network_descriptors)


    def graph_printer(self, network_path):

        G = nx.read_pajek(network_path);
        nx.draw(G);
        plt.show();


    def network_plotting(self, network_name ,x_data, y_data, degrees_, is_cumulative):

        plt.bar(x_data, y_data, width=0.4);
        plt.yscale('log');
        plt.xticks(x_data, [round(i, 2) for i in degrees_]);
        plt.xlabel('K');
        plt.ylabel(+is_cumulative+'p(K)');
        plt.title('Network: ' + network_name);
        plt.show()



    def graph_degree_analysis(self, network_path, network_name, network_ext):

        network_full_path = network_path+network_name+network_ext;

        G = nx.read_pajek(network_full_path);

        G_is_directed = nx.is_directed(G);

        if G_is_directed:
            G = nx.DiGraph(G);
        else:
            G = nx.Graph(G);

        G_nodes = G.nodes();

        G_num_nodes = len(G_nodes);

        network_degrees = sorted(nx.degree(G).values());
        "Sorted degrees in a graph"
        k_min_degree = network_degrees[0];
        "Minimum degree of the graph"
        k_max_degree = network_degrees[-1];
        "Maximum degree of the graph"

        nBins = 15;
        degrees_log = np.linspace(np.log(k_min_degree), np.log(k_max_degree + 1), nBins);

        # degree distribution
        degree_freqs = nx.degree_histogram(G);

        degrees_ = np.exp(degrees_log);
        degrees_[0] = network_degrees[0];
        pdf_ = np.zeros(nBins);

        for i in xrange(len(degrees_)):
            for j in xrange(len(degree_freqs)):
                if j>=degrees_[i] and j<degrees_[i+1]:
                    pdf_[i] += degree_freqs[j];

        degrees_pdf = np.asarray(pdf_) / float(G_num_nodes);
        degrees_ccdf = [sum(degree_freqs[int(np.ceil(k)):]) for k in degrees_];


        "a)pdf-plotting"
        self.network_plotting(network_name, degrees_log, degrees_pdf, degrees_ , "");


        "b)ccdf-plotting"
        self.network_plotting(network_name, degrees_log,degrees_ccdf, degrees_, "Cumulative ");


    def calculate_network_descriptors(self, networks_names, networks_path, descriptor_labels, graph_printed = True):

        for i in range(len(networks_names)):
            for network in networks_names[i]:

                net_full_path = networks_path[i] + network + ".net";
                graph_descriptors = self.graph_descriptor_extractor(net_full_path);
                graph_descriptors.insert(0, network);
                self.generate_descriptors_csv(descriptor_labels, graph_descriptors);
                self.print_graph_descriptors(graph_descriptors, descriptor_labels);
                if graph_printed: self.graph_printer(net_full_path);




networks_path = ["A1_nets/toy/","A1_nets/model/","A1_nets/real/"];
descriptor_labels = ["Network","Number of nodes","Number of edges","Minimum degree","Maximum degree","Average degree","Assortativity","Average clustering","Average path length","Diameter"];
networks_names = [["20x2+5x2","circle9","graph3+1+3","graph3+2+3","grid-p-6x6","rb25","star","wheel"],
                  ["256_4_4_2_15_18_p","256_4_4_4_13_18_p","BA1000","ER1000k8","ER5000-kmed8","homorand_N1000_K4_0","homorand_N1000_K6_0","rb125","SF_500_g2.7","SF_1000_g2.5","SF_1000_g2.7","SF_1000_g3.0","ws1000","ws2000"],
                  ["airports_UW","dolphins","PGP","zachary_unwh"]];


ND = NetworksDescriptors();

"---------Task 1: csv table------------------"

"ND.calculate_network_descriptors(networks_names, networks_path, descriptor_labels, False);"



"---------Task 2: generate graphs pdf and ccdf plots------------"


network_paths = ["A1_nets/model/","A1_nets/real/"];
selected_networks = ["ER1000k8","SF_1000_g2.7","ws1000","airports_UW"];

"A)Poisson Dists"
"ND.graph_degree_analysis(network_paths[0],selected_networks[0],'.net');"
"ND.graph_degree_analysis(network_paths[0],selected_networks[2],'.net');"

"B)Power Law Dists"
"ND.graph_degree_analysis(network_paths[0],selected_networks[1],'.net');"
"ND.graph_degree_analysis(network_paths[1],selected_networks[3],'.net');"










