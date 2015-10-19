int create_graphs(int n);
int create_graph(
    int id, int numnodes, int * nodeids, float * nodexy,
    int numedges, int numimpedances, int * edges, float * edgeweights,
    int twoway);
int initialize_pois(int nc, double md, int mi);
int initialize_category(int id, int numpois, double * pois);
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
