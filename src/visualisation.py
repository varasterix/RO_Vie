import plotly.figure_factory as ff
from src.ordonnancement import Ordonnancement
from src.job import Job
from datetime import datetime
import numpy as np

"""
This python file gives tools to visualise a solution (given by an object "Ordonnancement") to an instance of the 
flow-shop permutation problem

Note: In the "create_solution_figure" function, to have the desired value on the x-axis, a dirty method is used (by
converting integers into date-times): no other solutions are found on the forums about the package "plotly"
"""


def convert_to_datetime(x):
    """
    Converts the given integer to a corresponding datatime
    :param x: integer
    :return: a datetime corresponding to the given integer
    """
    return datetime.fromtimestamp(31536000+x*3600.0).strftime("%Y-%m-%d %H:%M:%S")


def create_solution_figure(ordonnancement, show_durations=True):
    if not isinstance(ordonnancement, Ordonnancement):
        raise Exception("The input object as to be an object from the class Ordonnancement")
    else:
        c_max = ordonnancement.duree()
        tasks = []
        annotations = []
        nb_machines = ordonnancement.nb_machines
        nb_jobs = len(ordonnancement.seq)
        for job in ordonnancement.seq:
            job_name = "Job " + str(job.numero())
            for machine in range(nb_machines):
                machine_name = "Machine " + str(machine)
                start = ordonnancement.date_debut_operation(job, machine)
                duration = job.duree_operation(machine)
                end = duration + start
                middle = (start + end)/2
                tasks.append(dict(Task=machine_name, Start=convert_to_datetime(start),
                                  Finish=convert_to_datetime(end), Resource=job_name))
                annotations.append(dict(x=convert_to_datetime(middle), y=(nb_machines - 1 - machine),
                                        text=str(duration), showarrow=True, font=dict(color='black')))

        span = 256 / nb_jobs
        colors = {"Job " + str(job.numero()): 'rgb(' + str((job.numero() * span) % 256) + ', '
                                              + str((84 + job.numero() * span) % 256) + ', '
                                              + str((169 + job.numero() * span) % 256) + ')'
                  for job in ordonnancement.seq}

        figure_name = 'Scheduling_' + str(nb_jobs) + '_jobs_on_' + str(nb_machines) + "_machines"
        figure = ff.create_gantt(tasks, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True,
                                 showgrid_y=True, title=figure_name)

        if show_durations:
            figure.layout['annotations'] = annotations
        num_tick_labels = np.arange(start=0, stop=(c_max+1), step=1, dtype=int)
        date_ticks = [convert_to_datetime(x) for x in num_tick_labels]
        figure.layout.xaxis.update({'tickvals': date_ticks, 'ticktext': num_tick_labels})

        return figure, figure_name


def show_solution_figure(ordonnancement, show_durations=True):
    """
    Shows the representation of the solution (given by the Ordonnancement object) to an instance of the flow-shop
    permutation problem
    :param ordonnancement: an Ordonnancement object where the scheduling of all jobs is done (in other words which
    represents a solution to an instance of the flow-shop permutation problem)
    :param show_durations: boolean which indicates if the duration of the tasks have to be represented (True by default)
    """
    figure, figure_name = create_solution_figure(ordonnancement, show_durations)
    figure.show()
    return None


def save_solution_as_html(ordonnancement, file_path="images/", file_name="", show_durations=True):
    """
    Generates the representation of the solution (given by the Ordonnancement object) to an instance of the flow-shop
    permutation problem as an html file with the given file name and stores it in the given file path
    :param ordonnancement: an Ordonnancement object where the scheduling of all jobs is done (in other words which
    represents a solution to an instance of the flow-shop permutation problem)
    :param file_path: path where the html file corresponding to the representation of the solution is stored (it needs
    to have the character "/" at the end or be the empty string)
    :param file_name: name of the html file corresponding to the representation of the solution
    :param show_durations: boolean which indicates if the duration of the tasks have to be represented (True by default)
    """
    figure, figure_name = create_solution_figure(ordonnancement, show_durations)
    if not file_name == "":
        figure_name = file_name
    figure.write_html(file_path + figure_name + '.html')
    return None


# "main" to give an example of how to use the "visualisation.py" methods
if __name__ == "__main__":
    a = Job(1, [1, 1, 1, 1, 10])
    b = Job(2, [1, 1, 1, 4, 8])
    c = Job(3, [2, 1, 3, 5, 1])
    d = Job(4, [2, 5, 5, 3, 3])
    e = Job(5, [1, 1, 3, 7, 1])
    scheduling = Ordonnancement(5)
    scheduling.ordonnancer_job(a)
    scheduling.ordonnancer_job(b)
    scheduling.ordonnancer_job(c)
    scheduling.ordonnancer_job(d)
    scheduling.ordonnancer_job(e)
    # show_solution_figure(scheduling)
    save_solution_as_html(scheduling)
