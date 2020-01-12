import subprocess
import src.constants as constants

time_limit = 0.1
flow_shop_file_path = 'data/dataset2/tai42.txt'
parameters_file_path = constants.PARAMETER_DEFAULT_PARAMETERS_FILE_PATH
global_memetic_results_path = constants.PARAMETER_GLOBAL_MEMETIC_RESULTS_PATH
visualise_results = 0  # boolean


if __name__ == "__main__":
    python_script = "solver.py"
    solver_args = ["python", python_script, str(time_limit), flow_shop_file_path, parameters_file_path,
                   global_memetic_results_path, str(visualise_results)]
    subprocess.call(args=solver_args)
