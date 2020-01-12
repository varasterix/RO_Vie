#!/usr/bin/env python
# coding: utf-8

""" Classe Ordonnancement """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job


class Ordonnancement:

    # constructeur pour un ordonnancement vide
    def __init__(self, nb_machines):
        # séquence des jobs
        self.seq = []
        # nombre de machiners
        self.nb_machines = nb_machines
        # durée totale de l'ordonnancement
        self.dur = 0
        # date à partir de laquelle chaque machine est libre
        self.date_dispo = [0 for i in range(self.nb_machines)]

    def duree(self):
        return self.dur

    def sequence(self):
        return self.seq

    def date_disponibilite(self, num_machine):
        return self.date_dispo[num_machine]

    def date_debut_operation(self, job, operation):
        return job.date_deb[operation]

    def fixer_date_debut_operation(self, job, operation, date):
        job.date_deb[operation] = date

    def afficher(self):
        print("Ordre des jobs :", end='')
        for job in self.seq:
            print(" ", job.numero(), " ", end='')
        print()
        for job in self.seq:
            print("Job", job.numero(), ":", end='')
            for mach in range(self.nb_machines):
                print(" op", mach, "à t =", self.date_debut_operation(job, mach), "|", end='')
            print()
        print("Cmax =", self.dur)

    # ajoute un job dans l'ordonnancement
    # à la suite de ceux déjà ordonnancés
    def ordonnancer_job(self, job):
        self.seq += [job]
        for mach in range(self.nb_machines):
            if mach == 0:  # première machine
                self.fixer_date_debut_operation(job, 0, self.date_dispo[0])
            else:  # machines suivantes
                date = max(self.date_dispo[mach - 1], self.date_dispo[mach])
                self.fixer_date_debut_operation(job, mach, date)
            self.date_dispo[mach] = self.date_debut_operation(job, mach) + \
                                    job.duree_operation(mach)
        self.dur = max(self.dur, self.date_dispo[self.nb_machines - 1])

    # ajoute les jobs d'une liste dans l'ordonnancement
    # à la suite de ceux déjà ordonnancés
    def ordonnancer_liste_job(self, liste_jobs):
        for job in liste_jobs:
            self.ordonnancer_job(job)

    def has_duplicate(self):
        seq = self.sequence()
        for i in range(len(seq) - 1):
            for j in range(i + 1, len(seq)):
                if seq[i] == (seq[j]):
                    return True
        return False

    def __str__(self):
        return str([str(job) for job in self.sequence()])

    def __eq__(self, other):
        if not isinstance(other, Ordonnancement):  # don't attempt to compare against unrelated types
            return NotImplemented
        else:
            return (self.seq == other.seq and self.nb_machines == other.nb_machines and self.dur == other.dur
                    and self.date_dispo == other.date_dispo)


# "main" pour tester la classe   
if __name__ == "__main__":
    a = job.Job(1, [1, 1, 1, 1, 10])
    b = job.Job(2, [1, 1, 1, 4, 8])
    a.afficher()
    b.afficher()
    l = [a, b]
    ordo = Ordonnancement(5)
    ordo.ordonnancer_job(a)
    ordo.ordonnancer_job(b)
    ordo.sequence()
    ordo.afficher()
    a.afficher()
    b.afficher()
