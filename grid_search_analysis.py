import sys
from src.memetic import memetic_heuristic
from src.flowshop import Flowshop
from src.utils import read_grid_search_parameters, write_best_parameters

grid_search_parameters_path = sys.argv[1]
flow_shop_file_path = sys.argv[2]
store_best_parameters_path = sys.argv[3]

# Loading grid search parameters
grid_search, estimated_nb_operations = read_grid_search_parameters(grid_search_parameters_path)
print("The number of operations for this instance is estimated at most " + str(estimated_nb_operations))

# Loading an instance of the FlowShop Problem
flow_shop_instance = Flowshop()
flow_shop_instance.definir_par(flow_shop_file_path)
file_name = flow_shop_file_path.split('/')[-1].split('.txt')[0]

# Executing the memetic heuristic with each set of parameters
best_params = None
overall_best_c_max = None
overall_first_epoch_best_c_max = None
for params in grid_search:
    initial_population_condition = \
        (params['random_prop'] + params['deter_prop'] == 1.0)
    crossover_condition = \
        (params['cross_1_point_prob'] + params['cross_2_points_prob'] + params['cross_position_prob'] == 1.0)
    local_search_condition =\
        (params['ls_swap_prob'] + params['ls_insert_prob'] == 1.0)
    if initial_population_condition and crossover_condition and local_search_condition:
        print("--> " + str(params))
        list_statistics, best_scheduling, iterations_where_restart = memetic_heuristic(flow_shop_instance, params)
        c_max_list = [statistics[1] for statistics in list_statistics]
        best_c_max = best_scheduling.duree()
        first_epoch_best_c_max = c_max_list.index(best_c_max) + 1
        if best_params is None:
            best_params = params
            overall_best_c_max = best_c_max
            overall_first_epoch_best_c_max = first_epoch_best_c_max
        else:
            if best_c_max < overall_best_c_max \
                    or (best_c_max == overall_best_c_max and first_epoch_best_c_max < overall_first_epoch_best_c_max):
                best_params = params
                overall_best_c_max = best_c_max
                overall_first_epoch_best_c_max = first_epoch_best_c_max

# Save the best parameters found for the given flow shop instance
write_best_parameters(file_name, best_params, store_best_parameters_path)
