"""
This file contains an example usage of the sbm package.
"""
import sbm


def main():
    # Create a sparse adjacency matrix of a graph with 1000 vertices and 5 equal sized clusters.
    # The probability of each edge inside a cluster is 0.3 and the probability of edges between clusters is 0.03.
    adj_mat = sbm.ssbm_adjmat(10000, 5, 0.3, 0.03, directed=False)
    print(adj_mat)

    # Create an adjacency matrix for a directed graph with 500 vertices, 4 clusters of equal size, and the following
    # probability matrix
    prob_mat_q = [[0.4, 0.1, 0.01, 0], [0.2, 0.4, 0.01, 0], [0.01, 0.3, 0.6, 0.2], [0, 0.2, 0.1, 0.6]]
    n = 500
    k = 4
    adj_mat = sbm.sbm_adjmat_equal_clusters(n, k, prob_mat_q, directed=True)
    print(adj_mat)

    # Create a graph from the SBM, specifying differently sized clusters
    adj_mat = sbm.sbm_adjmat([100, 50, 20, 100], prob_mat_q, directed=True)
    print(adj_mat)


if __name__ == "__main__":
    main()
