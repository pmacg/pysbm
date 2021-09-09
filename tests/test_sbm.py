"""
Unit tests for the stochastic_block_model functions.
"""
import sbm.stochastic_block_model


def test_get_edge_from_sample_num():
    ##########
    # TEST 1 #
    ##########
    # Let's start with two clusters which are not equal to each other, and each have length 5.
    #    c1_indices = [0, 1, 2, 3, 4]
    #    c2_indices = [0, 1, 2, 3, 4]
    # Then, our virtual list will look like:
    c1_size = 5
    c2_size = 5
    virtual_list = [(x, y) for x in range(c2_size) for y in range(c1_size)]
    assert(len(virtual_list) == sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, False, False, False))

    # The behaviour in this case should be the same regardless of whether the graph is directed or whether self-loops
    # are allowed
    for i in range(len(virtual_list)):
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, False, False, False) == virtual_list[i])
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, False, False, True) == virtual_list[i])
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, False, True, False) == virtual_list[i])
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, False, True, True) == virtual_list[i])

    ##########
    # TEST 2 #
    ##########
    # Now, let's assume c1 and c2 are the same cluster. They still have 5 vertices.
    c1_size = 5
    c2_size = 5

    # There are 4 cases: self-loops allowed and not allowed
    #                    and directed or undirected

    ## TEST 2a - directed, self-loops allowed
    # The virtual list looks the same as the different cluster case.
    virtual_list = [(x, y) for x in range(c2_size) for y in range(c1_size)]
    assert(len(virtual_list) == sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, True, True, True))

    for i in range(len(virtual_list)):
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, True, True, True) == virtual_list[i])

    ## TEST 2b - directed, self-loops not allowed
    # The virtual list looks as before, but skipping the self-loops
    virtual_list = [(x, y) for x in range(c2_size) for y in range(c1_size) if x != y]
    assert(len(virtual_list) == sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, True, False, True))

    for i in range(len(virtual_list)):
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, True, False, True) == virtual_list[i])

    ## TEST 2c - undirected, self-loops allowed
    # The virtual list has a triangular shape
    virtual_list = []
    for i in range(c1_size):
        for j in range(0, i + 1):
            virtual_list.append((i, j))
    assert(len(virtual_list) == sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, True, True, False))

    for i in range(len(virtual_list)):
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, True, True, False) == virtual_list[i])

    ## TEST 2d - undirected, no self-loops
    # The virtual list has a compressed triangular shape
    virtual_list = []
    for i in range(c1_size):
        for j in range(0, i):
            virtual_list.append((i, j))
    assert(len(virtual_list) == sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, True, False, False))

    for i in range(len(virtual_list)):
        assert(sbm.stochastic_block_model._get_edge_from_sample_num(
            i, c1_size, c2_size, True, False, False) == virtual_list[i])


def test_get_num_pos_edges():
    ##########
    # TEST 1 #
    ##########
    # Suppose we have two different clusters of different sizes
    c1_size = 5
    c2_size = 3

    # Regardless of self-loops or directed/undirected, the answer should always be c1 * c2.
    assert (sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, False, False, False) == 15)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, False, False, True) == 15)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, False, True, False) == 15)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c1_size, c2_size, False, True, True) == 15)

    ##########
    # TEST 2 #
    ##########
    # Now, we consider the same cluster
    c_size = 5

    # Work these out by hand :)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c_size, c_size, True, False, False) == 10)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c_size, c_size, True, True, False) == 15)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c_size, c_size, True, False, True) == 20)
    assert (sbm.stochastic_block_model._get_num_pos_edges(c_size, c_size, True, True, True) == 25)
