# Stochastic Block Model in Python
This is the repository for `sbm`, a simple python package for generating graphs from
the stochastic block model.

## Installation
Installation is as easy as `pip install sbm`.

## Usage
For usage examples, see `example_usage.py`.

The package provides three methods for generating graphs. Each one returns
a scipy `sparse.csr_matrix` object representing the adjacency matrix of the
generated graph.
* `sbm.sbm_adjmat(cluster_sizes, probability_matrix)` - this generates a graph with `len(cluster_sizes)` clusters, where
`cluster_sizes[i]` gives the number of vertices in each cluster. For a vertex `u` in cluster `i` and `v` in cluster `j`,
there is an edge `(u, v)` with probability `probability_matrix[i][j]`.
* `sbm.sbm_adjmat_equal_clusters(n, k, probability_matrix)` - this generates a graph with `n` vertices and `k` equal-sized
clusters.
* `sbm.ssbm_adjmat(n, k, p, q)` - this generates a graph with `n` vertices and `k` equal sized clusters. For any vertices
`u` and `v`, there is an edge between them with probability `p` if they are in the same cluster, and probability `q` if 
they are in different clusters.

## Help!
Feel free to contact me directly with any questions you have about using this package, using the contact details
on my GitHub account.