import os
import platform
import sys
import sysconfig

from cffi import FFI


ffi = FFI()

include_dirs = [
    'src/',
    'src/ann_1.1.2/include'
]

source_files = [
    'src/accessibility.cpp',
    'src/graphalg.cpp',
    'src/nearestneighbor.cpp',
    'src/pyaccesswrap.cpp',
    'src/contraction_hierarchies/src/libch.cpp',
    'src/ann_1.1.2/src/ANN.cpp',
    'src/ann_1.1.2/src/brute.cpp',
    'src/ann_1.1.2/src/kd_tree.cpp',
    'src/ann_1.1.2/src/kd_util.cpp',
    'src/ann_1.1.2/src/kd_split.cpp',
    'src/ann_1.1.2/src/kd_dump.cpp',
    'src/ann_1.1.2/src/kd_search.cpp',
    'src/ann_1.1.2/src/kd_pr_search.cpp',
    'src/ann_1.1.2/src/kd_fix_rad_search.cpp',
    'src/ann_1.1.2/src/bd_tree.cpp',
    'src/ann_1.1.2/src/bd_search.cpp',
    'src/ann_1.1.2/src/bd_pr_search.cpp',
    'src/ann_1.1.2/src/bd_fix_rad_search.cpp',
    'src/ann_1.1.2/src/perf.cpp'
]

extra_compile_args = [
    '-w',
    '-std=c++0x',
    '-O3',
    '-fpic',
    '-g',
]
extra_link_args = None

# separate compiler options for Windows
if sys.platform.startswith('win'):
    extra_compile_args = ['/w', '/openmp']
# Use OpenMP if directed or not on a Mac
elif os.environ.get('USEOPENMP') or not sys.platform.startswith('darwin'):
    extra_compile_args += ['-fopenmp']
    extra_link_args = [
        '-lgomp'
    ]

# recent versions of the OS X SDK don't have the tr1 namespace
# and we need to flag that during compilation.
# here we need to check what version of OS X is being targeted
# for the installation.
# this is potentially different than the version of OS X on the system.
if platform.system() == 'Darwin':
    mac_ver = sysconfig.get_config_var('MACOSX_DEPLOYMENT_TARGET')
    if mac_ver:
        mac_ver = [int(x) for x in mac_ver.split('.')]
        if mac_ver >= [10, 9]:
            extra_compile_args += ['-D NO_TR1_MEMORY']

# set_source is where you specify all the include statements necessary
# for your code to work and also where you specify additional code you
# want compiled up with your extension, e.g. custom C code you've written
#
# set_source takes mostly the same arguments as distutils' Extension, see:
# https://cffi.readthedocs.org/en/latest/cdef.html#ffi-set-source-preparing-out-of-line-modules
# https://docs.python.org/3/distutils/apiref.html#distutils.core.Extension
ffi.set_source(
    'pandana._accesswrap',
    """
    #include "pyaccesswrap.h"
    """,
    source_extension='.cpp',
    include_dirs=include_dirs,
    sources=source_files,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args)

# declare the functions, variables, etc. from the stuff in set_source
# that you want to access from your C extension:
# https://cffi.readthedocs.org/en/latest/cdef.html#ffi-cdef-declaring-types-and-functions
ffi.cdef(
    """
    int create_graphs(int n);
    int create_graph(
        int id, int numnodes, int * nodeids, float * nodexy,
        int numedges, int numimpedances, int * edges, float * edgeweights,
        int twoway);
    int initialize_pois(int nc, double md, int mi);
    int initialize_category(int id, int numpois, float * pois);
    int find_all_nearest_pois(
        double radius, int num, int varind, int gno, int impno, double * returnobj);
    int initialize_acc_vars(int gno, int nc);
    int initialize_acc_var(int gno, int id, int num, int * nodeids, double * accvars);
    int get_all_aggregate_accessibility_variables(
        double radius, int varind, int aggtyp, int decay, int graphno, int impno,
        int len, double * returnobj);
    int xy_to_node(int num, double * xys, double distance, int gno, int * nodes);
    int get_nodes_in_range(
        int nodeid, double radius, int gno, int impno,
        int num, int * nodes, double * dists);
    int sample_nodes(
        int *inodes, int inumnodes, int samplesize,
        double radius, int *skipnodeids, int gno, int impno,
        int num, int * numnodes, int * nodes, double * dists);
    int sample_all_nodes_in_range(
        int samplesize, double radius, int gno, int impno,
        int num, int * numnodes, int * nodes, double * dists);
    int get_all_model_results(
        double radius, int numvars, int * varindexes, float * varcoeffs, double distcoeff,
        double asc, double denom, double nestdenom, double mu, int graphno, int impno,
        int len, double * returnobj);
    int compute_all_design_variables(
        double radius, char * type, int gno, int num, double * nodes);
    int precompute_range(double radius, int gno);
    double route_distance(int srcnode, int destnode, int gno, int impno);
    """)
