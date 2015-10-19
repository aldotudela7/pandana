from ._accesswrap import ffi, lib


def create_graphs(num):
    lib.create_graphs(num)


def create_graph(id, nodes, edges, impedance_names, twoway):
    numnodes = len(nodes)
    numedges = len(edges)
    numimpedances = len(impedance_names)

    nodeids = nodes.index.values.astype('int32')
    nodeids_ptr = ffi.cast('int *', nodeids.ctypes.data)
    nodexy = nodes.as_matrix().astype('float32')
    nodexy_ptr = ffi.cast('float *', nodexy.ctypes.data)
    edges_arr = edges[['from', 'to']].as_matrix().astype('int32')
    edges_ptr = ffi.cast('int *', edges_arr.ctypes.data)
    edge_weights = (
        edges[impedance_names].transpose().as_matrix().astype('float32'))
    edge_weights_ptr = ffi.cast('float *', edge_weights.ctypes.data)
    twoway = ffi.cast('int', twoway)

    lib.create_graph(
        id, numnodes, nodeids_ptr, nodexy_ptr, numedges, numimpedances,
        edges_ptr, edge_weights_ptr, twoway)


def precompute_range(distance, graph_num):
    lib.precompute_range(distance, graph_num)
