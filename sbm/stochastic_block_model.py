"""
Several methods for generating graphs from the stochastic block model.
"""
import math
import random
import scipy.sparse
import numpy as np


def _get_edge_from_sample_num(edge_num, c1_size, c2_size, same_cluster, self_loops, directed):
    """
    Given the index edge_num of a sampled edge in the virtual 'list' of possible edges between two clusters, return
    the indices of the vertices which define this edge.

    :param edge_num: The edge number in the virtual 'list' of possible edges between these clusters.
    :param c1_size: The size of the first cluster
    :param c2_size: The size of the second cluster
    :param same_cluster: Whether these are the same cluster
    :param self_loops: Whether we will generate self loops
    :param directed: Whether we are generating a directed graph
    :return:
    """
    # If the clusters are not the same, then this is relatively straightforward.
    # The straightforward case also applies to the same cluster, directed case with self-loops.
    if not same_cluster or (directed and self_loops):
        # The virtual 'list' of possible edges has c1_size blocks each of length c2_size.
        u_cidx = int(edge_num / c2_size)
        v_cidx = edge_num % c1_size
        return u_cidx, v_cidx
    else:
        # The clusters are the same.
        if directed and not self_loops:
            # The directed case is the most straightforward. (We can assume not self_loops since the other case is
            # handled above.
            # There are now c1_size blocks of size (c2_size - 1).
            u_cidx = int(edge_num / (c2_size - 1))
            v_cidx = edge_num % (c1_size - 1)

            # Update the second index for indices greater than the first index since we skipped the self-loop case.
            if v_cidx >= u_cidx:
                v_cidx += 1
            return u_cidx, v_cidx

        # Now, we consider the undirected case
        elif not directed:
            if self_loops:
                # In this case, the 'virtual list' has a kind of triangular shape. For example:
                #     (0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0)...
                #
                # So, to get the first number, we need to find the nearest triangular number to the edge_number.
                # Solving the quadratic formula, we get:
                n = (1 + math.sqrt(1 + 8 * edge_num)) / 2

                # The largest triangular number less than edge_num is
                u_cidx = math.floor(n) - 1

                # Now, to get the other vertex, we can just look at the remainder
                v_cidx = edge_num - ((math.floor(n) * (math.floor(n) - 1)) / 2)
                return u_cidx, v_cidx
            else:
                # In this case, the 'virtual list' has a kind of triangular shape. For example:
                #     (1, 0), (2, 0), (2, 1), (3, 0)...
                #
                # So, to get the first number, we need to find the nearest triangular number to the edge_number.
                # Solving the quadratic formula, we get:
                n = (1 + math.sqrt(1 + 8 * edge_num)) / 2

                # The largest triangular number less than edge_num is
                u_cidx = math.floor(n)

                # Now, to get the other vertex, we can just look at the remainder
                v_cidx = edge_num - ((u_cidx * (u_cidx - 1)) / 2)
                return u_cidx, v_cidx
        else:
            # We should never get here!
            raise(Exception("This case should be impossible. There is a horrible bug in the SBM code."))


def _get_num_pos_edges(c1_size, c2_size, same_cluster, self_loops, directed):
    """
    Compute the number of possible edges between two clusters.

    :param c1_size: The size of the first cluster
    :param c2_size: The size of the second cluster
    :param same_cluster: Whether these are the same cluster
    :param self_loops: Whether we will generate self loops
    :param directed: Whether we are generating a directed graph
    :return: the number of possible edges between these clusters
    """
    if not same_cluster:
        # The number is simply the product of the number of vertices
        return c1_size * c2_size
    else:
        # The base number is n choose 2
        possible_edges_between_clusters = int((c1_size * (c1_size - 1)) / 2)

        # If we are allowed self-loops, then add them on
        if self_loops:
            possible_edges_between_clusters += c1_size

        # The number is normally the same for undirected and directed graphs, unless the clusters are the same, in which
        # case the number for the directed graph is double since we need to consider both directions of each edge.
        if directed:
            possible_edges_between_clusters *= 2

        # But if we are allowed self-loops, then we shouldn't double them since there is only one 'direction'.
        if directed and self_loops:
            possible_edges_between_clusters -= c1_size

        return possible_edges_between_clusters


def _get_number_of_edges(c1_size, c2_size, prob, same_cluster, self_loops, directed):
    """
    Compute the number of edges there will be between two clusters.

    :param c1_size: The size of the first cluster
    :param c2_size: The size of the second cluster
    :param prob: The probability of an edge between the clusters
    :param same_cluster: Whether these are the same cluster
    :param self_loops: Whether we will generate self loops
    :param directed: Whether we are generating a directed graph
    :return: the number of edges to generate between these clusters
    """
    # We need to compute the number of possible edges
    possible_edges_between_clusters = _get_num_pos_edges(c1_size, c2_size, same_cluster, self_loops, directed)

    # Sample the number of edges from the binomial distribution
    return np.random.binomial(possible_edges_between_clusters, prob)


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
            c2_base_index = 0
        else:
            second_clusters = range(cluster_1, len(cluster_sizes))

        for cluster_2 in second_clusters:
            print(f"Considering {cluster_1}, {cluster_2}")
            # Compute the number of edges between these two clusters
            num_edges = _get_number_of_edges(cluster_sizes[cluster_1],
                                             cluster_sizes[cluster_2],
                                             prob_mat_q[cluster_1][cluster_2],
                                             cluster_1 == cluster_2,
                                             self_loops,
                                             directed)

            # Sample this number of edges from the possible edges between these two clusters
            number_pos_edges = _get_num_pos_edges(cluster_sizes[cluster_1],
                                                  cluster_sizes[cluster_2],
                                                  cluster_1 == cluster_2,
                                                  self_loops,
                                                  directed)
            edges_added = set()

            for i in range(num_edges):
                while True:
                    u_cidx = random.choice(range(cluster_sizes[cluster_1]))
                    v_cidx = random.choice(range(cluster_sizes[cluster_2]))

                    if cluster_1 == cluster_2 and not self_loops:
                        while v_cidx == u_cidx:
                            v_cidx = random.choice(range(cluster_sizes[cluster_2]))

                    if (u_cidx, v_cidx) not in edges_added:
                        break

                # Make sure not to duplicate this edge.
                edges_added.add((u_cidx, v_cidx))

                # Get their true index.
                u_idx = c1_base_index + u_cidx
                v_idx = c2_base_index + v_cidx
                yield u_idx, v_idx

            # print(f"sampling edges...")
            # sampled_edges = random.sample(range(number_pos_edges), num_edges)
            #
            # # iterate through the sampled edges and generate the edge this corresponds to
            # print(f"adding edges...")
            # for edge in sampled_edges:
            #     u_cidx, v_cidx = _get_edge_from_sample_num(edge,
            #                                                cluster_sizes[cluster_1],
            #                                                cluster_sizes[cluster_2],
            #                                                cluster_1 == cluster_2,
            #                                                self_loops,
            #                                                directed)
            #
            #     # get their true index.
            #     u_idx = c1_base_index + u_cidx
            #     v_idx = c2_base_index + v_cidx
            #     yield u_idx, v_idx

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


def ssbm_adjmat(n, k, p, q, directed=False):
    """
    Generate a graph from the symmetric stochastic block model.

    Generates a graph with n vertices and k clusters. Every cluster will have floor(n/k) vertices. The probability of
    each edge inside a cluster is given by p. The probability of an edge between two different clusters is q.

    :param n: The number of vertices in the graph.
    :param k: The number of clusters.
    :param p: The probability of an edge inside a cluster.
    :param q: The probability of an edge between clusters.
    :param directed: Whether to generate a directed graph.
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
    return sbm_adjmat(cluster_sizes, prob_mat_q, directed=directed)
