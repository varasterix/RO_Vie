import os
import subprocess
from src.utils import load_best_parameters
import src.constants as constants

time_limit = 1
grid_search_parameters_path = constants.PARAMETER_GRID_SEARCH_PARAMETERS_PATH
global_memetic_results_path = constants.PARAMETER_GLOBAL_MEMETIC_RESULTS_PATH
store_best_parameters_path = constants.PARAMETER_STORE_BEST_PARAMETERS_PATH
use_best_parameters = 0  # boolean
default_parameters_file_path = constants.PARAMETER_DEFAULT_PARAMETERS_FILE_PATH
data_path = constants.PARAMETER_DATA_PATH
visualise_results = 0  # boolean


if __name__ == "__main__":
    python_script = "memetic_solver.py"
    for dataSet in os.listdir(data_path):
        for instance in os.listdir(data_path + dataSet):
            flow_shop_file_path = data_path + dataSet + "/" + instance
            file_name = instance.split('.txt')[0]
            print("Solving instance " + data_path + dataSet + '/' + file_name + '...')
            parameters_file_path = default_parameters_file_path if not use_best_parameters else \
                load_best_parameters(file_name=file_name, file_path=store_best_parameters_path)
            solver_args = ["python", python_script, str(time_limit), flow_shop_file_path, parameters_file_path,
                           global_memetic_results_path, str(visualise_results)]
            subprocess.call(args=solver_args)
    print("Finished!")
