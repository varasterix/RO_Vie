#!/usr/bin/env python

""" Classe Sommet :

A utiliser avec une file de priorité (heapq)
pour la recherche arborescente de la méthode
par évaluation-séparation
"""

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

class Sommet():

    def __init__(self, seq, non_places, val, num):
        self.seq = seq
        self.non_places = non_places
        self.val = val
        self.num = num

    def sequence(self):
        return self.seq

    def jobs_non_places(self):
        return self.non_places

    def evaluation(self):
        return self.val

    def numero(self):
        return self.num

    def __lt__(self, autre):
        """ Etablit la comparaison selon l'évaluation associée au sommet """
        return self.val < autre.val
