"""
Several methods for generating graphs from the stochastic block model.
"""
import math
import random
import scipy.sparse


def _generate_sbm_edges(cluster_sizes, prob_mat_q, directed=False, self_loops=False):
    """
    Given a list of cluster sizes, and a square matrix Q, generates edges for a graph in the following way.

    For two vertices u and v where u is in cluster i and v is in cluster j, there is an edge between u and v with
    probability Q_{i, j}.

    For the undirected case, we assume that the matrix Q is symmetric (and in practice look only at the upper triangle).
    For the directed case, we generate edges (u, v) and (v, u) with probabilities Q_{i, j} and Q_{j, i} respectively.

    Returns edges as pairs (u, v) where u and v are integers giving the index of the respective vertices.

    :param cluster_sizes: a list giving the number of vertices in each cluster
    :param prob_mat_q: A square matrix where Q_{i, j} is the probability of each edge between clusters i and j. Should
                       be symmetric in the undirected case.
    :param directed: Whether to generate a directed graph (default is false).
    :param self_loops: Whether to generate self-loops (default is false).
    :return: Edges (u, v).
    """
    # We will iterate over the clusters. This variable keeps track of the index of the first vertex in the current
    # cluster_1.
    c1_base_index = 0

    for cluster_1 in range(len(cluster_sizes)):
        # Keep track of the index of the first vertex in the current cluster_2
        c2_base_index = c1_base_index

        # If we are constructing a directed graph, we need to consider all values of cluster_2.
        # Otherwise, we will consider only the clusters with an index >= cluster_1.
        if directed:
            second_clusters = range(len(cluster_sizes))
        else:
            second_clusters = range(cluster_1, len(cluster_sizes))

        for cluster_2 in second_clusters:
            # Iterate through every pair of vertices in these two clusters.
            for u_cidx in range(cluster_sizes[cluster_1]):
                for v_cidx in range(cluster_sizes[cluster_2]):
                    # Check whether there is an edge between these two vertices
                    if random.random() < prob_mat_q[cluster_1][cluster_2]:
                        # There is an edge between these two vertices
                        # Get their true index.
                        u_idx = c1_base_index + u_cidx
                        v_idx = c2_base_index + v_cidx

                        # Double check whether we should add a self-loop
                        if u_idx != v_idx or self_loops:
                            yield u_idx, v_idx

            # Update the base index for the second cluster
            c2_base_index += cluster_sizes[cluster_2]

        # Update the base index of this cluster
        c1_base_index += cluster_sizes[cluster_1]


def sbm_adjmat(cluster_sizes, prob_mat_q, directed=False, self_loops=False):
    """
    Generate a graph from the stochastic block model.

    The list cluster_sizes gives the number of vertices inside each cluster and the matrix Q gives the probability of
    each edge between pairs of clusters.

    For two vertices u and v where u is in cluster i and v is in cluster j, there is an edge between u and v with
    probability Q_{i, j}.

    For the undirected case, we assume that the matrix Q is symmetric (and in practice look only at the upper triangle).
    For the directed case, we generate edges (u, v) and (v, u) with probabilities Q_{i, j} and Q_{j, i} respectively.

    Returns the adjacency matrix of the graph as a sparse scipy matrix in the CSR format.

    :param cluster_sizes: The number of vertices in each cluster.
    :param prob_mat_q: A square matrix where Q_{i, j} is the probability of each edge between clusters i and j. Should
                       be symmetric in the undirected case.
    :param directed: Whether to generate a directed graph (default is false).
    :param self_loops: Whether to generate self-loops (default is false).
    :return: The sparse adjacency matrix of the graph.
    """
    # Initialize the adjacency matrix
    adj_mat = scipy.sparse.lil_matrix((sum(cluster_sizes), sum(cluster_sizes)))

    # Generate the edges in the graph
    for (u, v) in _generate_sbm_edges(cluster_sizes, prob_mat_q, directed=directed, self_loops=self_loops):
        # Add this edge to the adjacency matrix.
        adj_mat[u, v] = 1

        if not directed:
            adj_mat[v, u] = 1

    # Reformat the output matrix to the CSR format
    return adj_mat.tocsr()


def ssbm_adjmat(n, k, p, q):
    """
    Generate a graph from the symmetric stochastic block model.

    Generates a graph with n vertices and k clusters. Every cluster will have floor(n/k) vertices. The probability of
    each edge inside a cluster is given by p. The probability of an edge between two different clusters is q.

    :param n: The number of vertices in the graph.
    :param k: The number of clusters.
    :param p: The probability of an edge inside a cluster.
    :param q: The probability of an edge between clusters.
    :return: The sparse adjacency matrix of the graph.
    """
    # Every cluster has the same size.
    cluster_sizes = [int(math.floor(n/k))] * k

    # Construct the k*k probability matrix Q. The off-diagonal entries are all q and the diagonal entries are all p.
    prob_mat_q = []
    for row_num in range(k):
        new_row = [q] * k
        new_row[row_num] = p
        prob_mat_q.append(new_row)

    # Call the general sbm method.
    return sbm_adjmat(cluster_sizes, prob_mat_q)
