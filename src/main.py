import calculate_run_parameters


def main():
    filename = ["bottom_200k.xes", "center_bottom_200k.xes", "center_top_200k.xes", "top_200k.xes",
                "top_general_200k.xes"]

    calculate_run_parameters.GetRunParameter(filename)
