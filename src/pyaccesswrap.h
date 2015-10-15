int create_graphs(int n);
int create_graph(
    int id, int numnodes, int * nodeids, float * nodexy,
    int numedges, int numimpedances, int * edges, float * edgeweights,
    int twoway);
int initialize_pois(int nc, double md, int mi);
int initialize_category(int id, int numpois, float * pois);
