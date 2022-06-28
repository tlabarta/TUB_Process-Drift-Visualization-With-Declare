import pm4py
import os


def main():
    filename = ["bottom_200k.xes", "center_bottom_200k.xes", "center_top_200k.xes", "top_200k.xes",
                "top_general_200k.xes"]

    files, winsize, winstep = GetRunParameter(filename)

    for i, j, k in files:
        os.system('python3 src/scenario_1.py -logName ' + i + " -subL " + str(j) + " -sliBy " + str(k))


def GetRunParameter(filename: str or list):
    """
    Parameters
    ----------
    filename : str or list with filename. NOTE: Only the name, not the path.

    Returns
    -------
    files: list
    """
    log_size = []
    winsize = []
    winstep = []
    files = [filename, winsize, winstep]

    for i in filename:
        log = pm4py.read_xes('../TUB_Process-Drift-Visualization-With-Declare/data/data_input/' + i)

        lsize = len(log)
        step = round(lsize / (60 + 1))
        size = 2 * step

        log_size.append(lsize)
        winstep.append(step)
        winsize.append(size)
    return files, winsize, winstep
    print(files)


python3 src/scenario_1.py -logName top_general_200k -subL 32 -sliBy 16