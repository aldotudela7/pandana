import numpy as np

from ._accesswrap import ffi, lib

# Several functions from pyaccesswrap.cpp have not been wrapped here because
# they are not used in Pandana:
#
# get_nodes_in_range
# sample_nodes
# sample_all_nodes_in_range
# get_all_model_results


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


def get_all_aggregate_accessibility_variables(
        distance, varnum, agg_type, decay, graph_num, imp_num, num_nodes):
    agg_arr = np.empty(num_nodes, dtype='float64')
    agg_ptr = ffi.cast('double *', agg_arr.ctypes.data)

    lib.get_all_aggregate_accessibility_variables(
        distance, varnum, agg_type, decay, graph_num, imp_num, num_nodes,
        agg_ptr)

    return agg_arr


def xy_to_node(xys, distance, graph_num):
    num_xys = len(xys)
    xys = xys.as_matrix().astype('float64')
    xys_ptr = ffi.cast('double *', xys.ctypes.data)
    nodes_arr = np.empty(num_xys, dtype='int32')
    nodes_ptr = ffi.cast('int *', nodes_arr.ctypes.data)

    lib.xy_to_node(num_xys, xys_ptr, distance, graph_num, nodes_ptr)

    return nodes_arr


def find_all_nearest_pois(
        distance, num_pois, varnum, graph_num, imp_num, num_nodes):
    out_arr = np.empty((num_nodes, num_pois), dtype='float64')
    out_ptr = ffi.cast('double *', out_arr.ctypes.data)

    lib.find_all_nearest_pois(
        distance, num_pois, varnum, graph_num, imp_num, out_ptr)

    return out_arr


def route_distance(source_node, dest_node, graph_num, imp_num):
    return lib.route_distance(source_node, dest_node, graph_num, imp_num)
