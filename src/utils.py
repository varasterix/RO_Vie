from sklearn.model_selection import ParameterGrid
import csv


def read_best_known_results(file_path):
    best_known_results = {}
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(reader):
            if index != 0:
                file_name = row[0]
                # n = row[1]
                # m = row[2]
                best_known_result = int(row[3])
                best_known_results[file_name] = best_known_result
    return best_known_results


def get_best_know_result(best_known_results, file_name):
    return best_known_results[file_name]


def read_global_memetic_results(file_path):
    global_memetic_results = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(reader):
            if index == 0:
                instance_results = {
                    'file_name': row[0],
                    'n': row[1],
                    'm': row[2],
                    'best_known_solution': row[3],
                    'inf_bound': row[4],
                    'initial_solution': row[5],
                    'best_solution_found': row[6],
                    'relative_gap': row[7],
                    'initial_solutions_mean': row[8],
                    'best_initial_solution': row[9],
                    'worst_initial_solution': row[10],
                    'best_parameters': row[11]
                    }
            else:
                instance_results = {
                    'file_name': row[0],
                    'n': int(row[1]),
                    'm': int(row[2]),
                    'best_known_solution': int(row[3]),
                    'inf_bound': None if row[4] == '' else int(row[4]),
                    'initial_solution': None,  # Always row[5]=='' here (population based heuristic)
                    'best_solution_found': None if row[6] == '' else int(row[6]),
                    'relative_gap': None if row[7] == '' else float(row[7]),
                    'initial_solutions_mean': None if row[8] == '' else float(row[8]),
                    'best_initial_solution': None if row[9] == '' else int(row[9]),
                    'worst_initial_solution': None if row[10] == '' else int(row[10]),
                    'best_parameters': row[11]
                    }
            global_memetic_results.append(instance_results)
        csv_file.close()
    return global_memetic_results


def get_best_known_and_found_solutions(global_memetic_results, file_name):
    result = list(filter(lambda res: res['file_name'] == file_name, global_memetic_results))[0]
    return result['best_known_solution'], result['best_solution_found']


def update_global_memetic_results(global_memetic_results, file_name, solution_found, relative_gap,
                                  initial_solutions_mean, best_initial_solution, worst_initial_solution,
                                  best_parameters):
    new_global_memetic_results = []
    is_updated = False
    for result in global_memetic_results:
        if result['file_name'] == file_name and (result['best_solution_found'] is None or
                                                 result['best_solution_found'] > solution_found):
            new_result = {
                'file_name': file_name,
                'n': result['n'],
                'm': result['m'],
                'best_known_solution': result['best_known_solution'],
                'inf_bound': result['inf_bound'],
                'initial_solution': result['initial_solution'],
                'best_solution_found': solution_found,
                'relative_gap': relative_gap,
                'initial_solutions_mean': initial_solutions_mean,
                'best_initial_solution': best_initial_solution,
                'worst_initial_solution': worst_initial_solution,
                'best_parameters': str(best_parameters)
                }
            new_global_memetic_results.append(new_result)
            is_updated = True
        else:
            new_global_memetic_results.append(result)
    return new_global_memetic_results, is_updated


def write_global_memetic_results(file_path, global_memetic_results):
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')
        column_keys = ['file_name', 'n', 'm', 'best_known_solution', 'inf_bound', 'initial_solution',
                       'best_solution_found', 'relative_gap', 'initial_solutions_mean', 'best_initial_solution',
                       'worst_initial_solution', 'best_parameters']
        all_rows = []
        for index, result in enumerate(global_memetic_results):
            if index == 0:
                row = [result[key] for key in column_keys]
            else:
                row = [str(result[key]) if result[key] is not None else '' for key in column_keys]
            all_rows.append(row)
        writer.writerows(all_rows)
    csv_file.close()


def read_grid_search_parameters(file_path):
    param_grid = {}
    nb_operations = 1
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(reader):
            if index != 0:
                # parameter_description = row[0]
                parameter_name = row[1]
                parameter_type = row[2]
                values = list(filter(lambda value: value != '', row[3:]))
                nb_operations = nb_operations * len(values)
                if parameter_type == 'bool':
                    param_grid[parameter_name] = [bool(int(value)) for value in values]
                elif parameter_type == 'int':
                    param_grid[parameter_name] = [int(value) for value in values]
                elif parameter_type == 'float':
                    param_grid[parameter_name] = [float(value) for value in values]
                elif parameter_type == 'str':
                    param_grid[parameter_name] = [value for value in values]
                else:
                    raise Exception('Unsupported type of parameter: ' + parameter_type)
    return ParameterGrid(param_grid), nb_operations


def write_best_parameters(file_name, parameters, file_path):
    output = open(file_path + file_name.split('.')[0] + "_parameters.txt", 'w+')
    for key in parameters:
        output.write(key + " " + type(parameters[key]).__name__ + " " + str(parameters[key]) + '\n')
    output.close()


def load_best_parameters(file_name, file_path):
    return load_parameters(file_path + file_name.split('.')[0] + "_parameters.txt")


def load_parameters(complete_file_path):
    load = open(complete_file_path, 'r')
    parameters = {}
    for line in load:
        parameter_key, parameter_type, value = line[:-1].split(" ")
        if parameter_type == 'bool':
            parameters[parameter_key] = bool(int(value))
        elif parameter_type == 'int':
            parameters[parameter_key] = int(value)
        elif parameter_type == 'float':
            parameters[parameter_key] = float(value)
        elif parameter_type == 'str':
            parameters[parameter_key] = value
        else:
            raise Exception('Unsupported type of parameter: ' + parameter_type)
    load.close()
    return parameters
