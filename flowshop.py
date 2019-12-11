#!/usr/bin/env python
# coding: utf-8

"""Résolution du flowshop de permutation :
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import ordonnancement


class Flowshop:
    def __init__(self, nb_jobs=0, nb_machines=0, l_job=None):
        # nombre de jobs pour le problème
        self.nb_jobs = nb_jobs
        # nombre de machine pour le problème
        self.nb_machines = nb_machines
        # liste des jobs pour le problème
        self.l_job = l_job

    def nombre_jobs(self):
        return self.nombre_jobs

    def nombre_machines(self):
        return self.nombre_machines

    def liste_jobs(self, num):
        return self.l_job[num]

    def definir_par(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom,"r")
        # lecture de la première ligne
        ligne = fdonnees.readline() 
        l = ligne.split() # on récupère les valeurs dans une liste
        self.nb_jobs = int(l[0])
        self.nb_machines = int(l[1])
       
        self.l_job = []
        for i in range(self.nb_jobs):
            ligne = fdonnees.readline() 
            l = ligne.split()
            # on transforme les chaînes de caractères en entiers
            l = [int(i) for i in l]
            j = job.Job(i, l)
            self.l_job += [j]
        # fermeture du fichier
        fdonnees.close()


if __name__ == "__main__":
    prob = Flowshop()
    prob.definir_par("jeu1.txt")
    for i in range(prob.nb_jobs):
        j = prob.liste_jobs(i)
        j.afficher()
