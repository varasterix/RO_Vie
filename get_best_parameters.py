import os
import subprocess
import src.constants as constants

grid_search_parameters_path = constants.PARAMETER_GRID_SEARCH_PARAMETERS_PATH
store_best_parameters_path = constants.PARAMETER_STORE_BEST_PARAMETERS_PATH
data_path = constants.PARAMETER_DATA_PATH


if __name__ == "__main__":
    python_script = "grid_search_analysis.py"
    for dataSet in os.listdir(data_path):
        for instance in os.listdir(data_path + dataSet):
            file_name = instance.split('.txt')[0]
            if file_name == 'tai52':
                print("Grid search for instance " + data_path + dataSet + '/' + file_name + '...')
                flow_shop_file_path = data_path + dataSet + "/" + instance
                grid_search_analysis_args = ["python", python_script, grid_search_parameters_path, flow_shop_file_path,
                                             store_best_parameters_path]
                subprocess.call(args=grid_search_analysis_args)
    print("Finished!")
