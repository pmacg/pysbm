"""
This file contains an example usage of the sbm package.
"""
import sbm


def main():
    # Create a sparse adjacency matrix of a graph with 1000 vertices and 5 equal sized clusters.
    # The probability of each edge inside a cluster is 0.5 and the probability of edges between clusters is 0.05.
    adj_mat = sbm.ssbm_adjmat(10000, 5, 0.5, 0.05)

    print(adj_mat)


if __name__ == "__main__":
    main()
