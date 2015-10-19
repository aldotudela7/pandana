from ._accesswrap import ffi, lib


def create_graphs(num):
    lib.create_graphs(num)


def create_graph(id_, nodes, edges, impedance_names, twoway):
    num_nodes = len(nodes)
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
        id_, num_nodes, nodeids_ptr, nodexy_ptr, numedges, numimpedances,
        edges_ptr, edge_weights_ptr, twoway)


def precompute_range(distance, graph_num):
    lib.precompute_range(distance, graph_num)


def initialize_pois(num_categories, max_dist, max_pois):
    lib.initialize_pois(num_categories, max_dist, max_pois)


def initialize_category(id_, xys):
    numpois = len(xys)
    xys = xys.as_matrix().astype('float64')
    xys_ptr = ffi.cast('double *', xys.ctypes.data)

    lib.initialize_category(id_, numpois, xys_ptr)


def initialize_acc_vars(graph_num, num_vars):
    lib.initialize_acc_vars(graph_num, num_vars)


def initialize_acc_var(graph_num, id_, nodeids, metric):
    num_nodes = len(nodeids)
    nodeids = nodeids.values.astype('int32')
    nodeids_ptr = ffi.cast('int *', nodeids.ctypes.data)
    metric = metric.values.astype('float64')
    metric_ptr = ffi.cast('double *', metric.ctypes.data)

    lib.initialize_acc_var(graph_num, id_, num_nodes, nodeids_ptr, metric_ptr)
