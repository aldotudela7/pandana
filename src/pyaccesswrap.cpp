#include "accessibility.h"
#include "graphalg.h"
#include "pyaccesswrap.h"

std::vector<std::shared_ptr<MTC::accessibility::Accessibility> > sas;


int create_graphs(int n) {
    for(int i=0;i<n;i++) {
        std::shared_ptr<MTC::accessibility::Accessibility>
            aptr(new MTC::accessibility::Accessibility);
        sas.push_back(aptr);
    }
    return 0;
}


int create_graph(
    int id, int numnodes, int * nodeids, float * nodexy,
    int numedges, int numimpedances, int * edges, float * edgeweights,
    int twoway)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[id];

    for(int i = 0 ; i < numimpedances ; i++) {
        std::shared_ptr<MTC::accessibility::Graphalg>
            ptr(new MTC::accessibility::Graphalg);
        sa->ga.push_back(ptr);
        sa->ga[i]->Build(nodeids, nodexy, numnodes, edges,
            edgeweights + (numedges * i), numedges, twoway);
    }

    sa->numnodes = sa->ga[0]->numnodes;

    return 0;
}


int initialize_pois(int nc, double md, int mi)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[0];

    sa->initializePOIs(nc,md,mi);

    return 0;
}


int initialize_category(int id, int numpois, double * pois)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[0];

    MTC::accessibility::accessibility_vars_t av;
    av.resize(sa->numnodes);
    for(int i = 0 ; i < numpois ; i++) {
        // XXX this should really only respond to node ids and use the xy
		// conversion function below
        int nodeid = sa->ga[0]->NearestNode(pois[i*2+0],pois[i*2+1],NULL);
		//assert(nodeid < sa->ga[0].numpois);
        av[nodeid].push_back(nodeid);
    }

    sa->initializeCategory(id,av);

    return 0;
}


int find_all_nearest_pois(
    double radius, int num, int varind, int gno, int impno, double * returnobj)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    std::vector<std::vector<float> > nodes =
        sa->findAllNearestPOIs(radius, num, varind, impno);
    int size = nodes.size();

    for(int i = 0 ; i < size ; i++) {
        for(int j = 0 ; j < num ; j++) {
            returnobj[i * size + j] = (double) nodes[i][j];
        }
    }

	return 0;
}


int initialize_acc_vars(int gno, int nc)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    sa->initializeAccVars(nc);

    return 0;
}


int initialize_acc_var(int gno, int id, int num, int * nodeids, double * accvars)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    MTC::accessibility::accessibility_vars_t av;
    av.resize(sa->numnodes);

    int cnt = 0;
    for(int i = 0 ; i < num ; i++) {
        if(nodeids[i] == -1) {
             cnt++;
             continue;
        }
        av[nodeids[i]].push_back(accvars[i]);
    }

    sa->initializeAccVar(id,av);

    return 0;
}


int get_all_aggregate_accessibility_variables(
    double radius, int varind, int aggtyp, int decay, int graphno, int impno,
    int len, double * returnobj)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[graphno];

    std::vector<double> nodes = sa->getAllAggregateAccessibilityVariables(
                                radius,
								varind,
								(MTC::accessibility::aggregation_types_t)aggtyp,
								(MTC::accessibility::decay_func_t)decay,
								impno);

    for(int i = 0 ; i < len ; i++) {
        returnobj[i] = (double) nodes[i];
    }

	return 0;
}


int xy_to_node(int num, double * xys, double distance, int gno, int * nodes)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    //#pragma omp parallel for
    for(int i = 0 ; i < num ; i++) {
        double d;
		// now that we have multiple subgraphs, the nearest neighbor should
		// really be moved to the accessibility object
		int nodeid = sa->ga[0]->NearestNode(xys[i*2+0],xys[i*2+1],&d);
        if(distance != -1.0 && d > distance) {
            nodes[i] = -1;
            continue;
        }
        nodes[i] = nodeid;
    }

	return 0;
}


int get_nodes_in_range(
    int nodeid, double radius, int gno, int impno,
    int num, int * nodes, double * dists)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    MTC::accessibility::DistanceVec dm = sa->Range(nodeid,radius,impno);

    for(int i = 0 ; i < num ; i++) {
        nodes[i] = dm[i].first;
        dists[i] = (double) dm[i].second;
    }

    return 0;
}


int sample_nodes(
    int *inodes, int inumnodes, int samplesize,
    double radius, int *skipnodeids, int gno, int impno,
    int num, int * numnodes, int * nodes, double * dists)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    int nodeid;

    #pragma omp parallel for
    for(int i = 0 ; i < num ; i++) {
        if (inodes) nodeid = inodes[i];
        else nodeid = i;

        MTC::accessibility::DistanceVec dm = sa->Range(nodeid,radius,impno);

        numnodes[i] = dm.size();

        std::random_shuffle(dm.begin(),dm.end());

        for(int j = 0, skipped = 0 ; j < samplesize+skipped; j++) {

            // skip the chosen nodeid if we find it
           if(skipnodeids && skipnodeids[i] != -1 && j < dm.size() &&
              skipnodeids[i] == dm[j].first) {
                skipped++;
                continue;
            }

            if(j >= dm.size()) {
                nodes[i*samplesize+j-skipped] = -1;
                dists[i*samplesize+j-skipped] = -1.0;
                continue;
            }

            nodes[i*samplesize+j-skipped] = dm[j].first;
            dists[i*samplesize+j-skipped] = (double) dm[j].second;
        }
    }

    return 0;
}


/* this function samples a certain number of nodes from the available range
   for a given graph */
int sample_all_nodes_in_range(
    int samplesize, double radius, int gno, int impno,
    int num, int * numnodes, int * nodes, double * dists)
{
    sample_nodes(
        NULL, -1, samplesize, radius, NULL, gno, impno,
        num, numnodes, nodes, dists);
    return 0;
}


int get_all_model_results(
    double radius, int numvars, int * varindexes, float * varcoeffs, double distcoeff,
    double asc, double denom, double nestdenom, double mu, int graphno, int impno,
    int len, double * returnobj)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[graphno];

    std::vector<double> nodes = sa->getAllModelResults(radius, numvars,
        varindexes, varcoeffs, distcoeff, asc, denom, nestdenom, mu, impno);

    for (int i = 0 ; i < len ; i++) {
        returnobj[i] = (double) nodes[i];
    }

	return 0;
}


int compute_all_design_variables(
    double radius, char * type, int gno, int num, double * nodes)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];
    std::string str(type);

    #pragma omp parallel for
    for(int i = 0 ; i < num ; i++) {
    	nodes[i] = (double) sa->computeDesignVariable(i,radius,str);
    }

	return 0;
}


int precompute_range(double radius, int gno)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

	sa->precomputeRangeQueries((float)radius);

	return 0;
}


double route_distance(int srcnode, int destnode, int gno, int impno)
{
    std::shared_ptr<MTC::accessibility::Accessibility> sa = sas[gno];

    double dist = sa->ga[impno]->Distance(srcnode,destnode);

    return dist;
}
