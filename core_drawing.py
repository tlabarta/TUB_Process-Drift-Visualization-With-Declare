import seaborn as sns; sns.set()
import matplotlib.pylab as plt
import copy
#https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib
import pandas as pd

def heatmaplike_graph_with_subplots(data,PATHoUT, ts = None, y_lines = None, x_lines_all = None, cluster_order = None):
    PATHoUT = "graphs_produced/" + PATHoUT

    data_c = copy.deepcopy(data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            data_c[i][j] = data[i][j]/100

    #https://matplotlib.org/examples/color/colormaps_reference.html
    # copper
    # viridis

    ax = sns.heatmap(data_c, linewidth=0, cmap="plasma", xticklabels=ts) #cmap="PiYG"
    # ax = sns.heatmap(data_c, linewidth=0, cmap="binary", xticklabels=ts) #cmap="PiYG"

    #plt.show()




    # draw horizontal lines
    lines = [y_lines] * (len(data_c[0])+1)
    dataT = pd.DataFrame(lines)
    asx = sns.lineplot(data=dataT,legend=False, palette=['white'] * len(y_lines), dashes = [(2, 2)] * len(y_lines)) #, dashes=[(2, 2), (2, 2)]

    # here is the same but faster
    # if y_lines:
    #     ax.hlines(y_lines, *ax.get_xlim(),colors='white',linestyles='dashed')


    if x_lines_all:
        if len(x_lines_all) == 1:
            ax.vlines(next(iter(x_lines_all.values())), *ax.get_ylim(), colors='white', linestyles='dotted')

        # here draw per cluster
        else:
            # lines = [[44,55],[88,66]]
            # dataT = pd.DataFrame(lines)
            # asy = sns.lineplot(data=dataT, legend=False, palette=['white'] * 2,
            #                    dashes=[(4, 2)] * len(y_lines))

            to_ind = 0

            for i,j in zip(cluster_order, y_lines):
                from_ind = to_ind
                to_ind =  j
                for k in x_lines_all[i]:
                    plt.plot([k,k],[from_ind, to_ind], linestyle='dotted', color='white')

   # ax.tight_layout()
    ax.get_figure().savefig(PATHoUT, bbox_inches='tight')
