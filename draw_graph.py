'''


Example run:
python3 draw_graph.py -logName bpi_challenge_2013_open -logFolder bpic2013 -subL 100 -sliBy 50 -caseID 0 -timestampID 3 -noMinerful -driftAll

Author: Anton Yeshchenko
'''

import argparse
import csv
from pathlib import Path
import pprint

import matplotlib.pyplot as plt
import numpy
import seaborn as sns

from math import sqrt
import subprocess

# window size
from clustering_methods import cluster_hierarcical
from core_drawing import heatmaplike_graph_with_subplots
from core_stackedPlot_drawing import drawStackedAll, drawStackedOne
from extra_methods import timestamp_ticks, importData

parser = argparse.ArgumentParser()
# parser.add_argument("--tStart", type=int)

# https://pymotw.com/2/argparse/
parser.add_argument("-logName", help="the log name")
parser.add_argument("-logFolder", help="the folder with a timestamp sorted log, check https://github.com/yesanton/Event-Log-Preprocessing-Tools for timeseoring of CSVs")
parser.add_argument("-caseID", type=int)
parser.add_argument("-timestampID", type=int)
parser.add_argument("-subL", type=int)
parser.add_argument("-sliBy", type=int)
parser.add_argument('-noMinerful', action='store_true', default=False,
                    dest='noMinerful',
                    help='set this optional parameter if there are already minerful mined constraints')

parser.add_argument('-driftAll', action='store_true', default=False,
                    dest='driftAll',
                    help='set this optional parameter if you want to generale change points for the whole set at the same time (if not set, every cluster will get its own changepoint)')

parser.add_argument('-noSort', action='store_true', default=False,
                    dest='noSort',
                    help='set this optional parameter if the constrains shouldn\'t be sorted inside of clusters')

#parser.add_argument("-type", type=int, help='0 support, 1 confidence, 2 interstFactor')
# parser.add_argument("-colors", help="[bw] for black and while, [yb] for yellow to blue")

args = parser.parse_args()
tStart = 0

# THese are standard parameters
if args.subL:
    subL = args.subL
else:
    subL = 1000

if args.sliBy:
    sliBy = args.sliBy
else:
    sliBy = 500

# if args.type:
#     iii = args.type
# else:
#     iii = 0 # 0 support, 1 confidence, 2 interstFactor

# if args.colors:
#     colors = args.colors
# else:
#     colors = 'bw'

if args.logFolder:
    dataset_folder = args.logFolder
else:
    dataset_folder = "BPIC15_1"

if args.logName:
    dataset_moto = args.logName
else:
    dataset_moto = ''

if args.caseID:
    caseID = args.caseID
else:
    caseID = 0

if args.timestampID:
    timestampID = args.timestampID
else:
    timestampID = 0

if dataset_folder:
    dataset_folder += '/'




# first we run minerful with parameters!
completed = subprocess.run(['ls', '-1'])
print('returncode:', completed.returncode)

data_path = '../data_initial/'+dataset_folder + dataset_moto+'_timestamp_sorted.xes.gz'

if not args.noMinerful:
    subprocess.run(["./run-MINERfulSlider.sh",
                    "-iLF",
                    data_path,
                    "-tStart", str(tStart),"-subL",str(subL),
                    '-p', '4',
                    '-s', '0.000000001',
                    '-c', '0.0',
                    '-i', '0.0' ,
                    '-ppAT', 'none',
                    '-sliOut',
                    "../data_from_minerful/"+dataset_moto+"_"+
                    str(tStart) + "_" + str(subL) + "_"+ str(sliBy) + '.csv',
                    "-sliBy", str(sliBy),
                    " -shush"], cwd="minerful_scripts")

# prepare timestamp headers for the plot
ts = timestamp_ticks(sliding_window_step=sliBy,
                     window_size=subL,
                     dataset_folder=dataset_folder,
                     dataset_name=dataset_moto,
                     case_ind=caseID,
                     timestamp_ind=timestampID)

print (ts)
dataset_link = Path("data_from_minerful/"+dataset_moto+"_"+ str(tStart) + "_" + str(subL) + "_"+ str(sliBy) + '.csv')
sequences, hea , _= importData(dataset_link)

# For now we only concentrate on confidence as it is most representative measure
#support = []
confidence = []
# interest_factor = []

for i,j in zip(sequences, hea):
    # if j[0] == "Support":
    #     support.append(j[1:] + i)
    if j[0] == "Confidence":
        confidence.append(j[1:] + i)
    # else:
    #     interest_factor.append(j[1:] + i)


plot_with_hierarchy_clustering = True

#confidence = sort_by_closest_neigbour(confidence)
if plot_with_hierarchy_clustering:
    linkage_method = 'ward'
    linkage_metric = 'euclidean'
    fcluster_value = 2000
    fcluster_metric = 'distance'

    confidence, \
    cluster_bounds, \
    horisontal_separation_bounds_by_cluster, \
    clusters_with_declare_names, \
    clusters_dict, \
    cluster_order =\
        cluster_hierarcical(confidence, linkage_method, linkage_metric, fcluster_value, fcluster_metric, args.driftAll, args.noSort)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(clusters_with_declare_names)

    # draw_graph(confidence, plot_type, file_name_out)

    # c_d = [0] * len(clusters_dict[4][0][3:])
    # for i in clusters_dict[4]:
    #     for ind in range(len(i[3:])):
    #         c_d[ind] += i[ind+3]
    # for i in range(len(c_d)):
    #     c_d[i] /= len(c_d)
    #
    # import csv
    #
    # with open('testing_scripts/one_cluster_example.csv', mode='w') as one_cluster_example:
    #     writer = csv.writer(one_cluster_example, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     for i in clusters_dict[4]:
    #         writer.writerow(i)
    #
    # #
    # from scipy.interpolate import make_interp_spline, BSpline
    # xnew = numpy.linspace(0, len(c_d), 300)  # 300 represents number of points to make between T.min and T.max
    # spl = make_interp_spline(range(len(c_d)), c_d, k=2)  # BSpline object
    # power_smooth = spl(xnew)
    # plt.plot(xnew, power_smooth)
    # plt.show()




    append_name = linkage_method + '_' + linkage_metric + '_' + str(fcluster_value) + '_' + fcluster_metric
    if not args.driftAll:
         append_name += "_changepoints_separately"
    file_name_out = dataset_moto + "plot_confidence_" + str(tStart) + "_" + str(subL) + "_" + str(sliBy) + '_' + append_name + ".png"
    heatmaplike_graph_with_subplots(confidence, file_name_out, ts=ts, y_lines=cluster_bounds, x_lines_all=horisontal_separation_bounds_by_cluster, cluster_order = cluster_order)
    print('confidence graph drawn with a name: ' + file_name_out)

    # drawStackedAll(ts=ts, clusters_dict=clusters_dict, cluster_order = cluster_order)
    #
    # drawStackedOne(ts=ts, clusters_dict=clusters_dict,key=cluster_order[5])
    # drawStackedOne(ts=ts, clusters_dict=clusters_dict,key=cluster_order[6])
    drawStackedOne(ts=ts, clusters_dict=clusters_dict,key=cluster_order[7])





