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
    include_dirs=include_dirs,
    sources=source_files,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args)

# declare the functions, variables, etc. from the stuff in set_source
# that you want to access from your C extension:
# https://cffi.readthedocs.org/en/latest/cdef.html#ffi-cdef-declaring-types-and-functions
ffi.cdef(
    """
    """)
