#!/usr/bin/env python

"""Résolution du flowshop de permutation : 

 - par algorithme NEH
 - par une méthode évaluation-séparation
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import ordonnancement
import sommet

import copy
import heapq

MAXINT = 10000

class Flowshop():
	def __init__(self, nb_jobs=0, nb_machines=0, l_job=[]):
		self.nb_jobs = nb_jobs
		self.nb_machines = nb_machines
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
	   
		for i in range(self.nb_jobs):
			ligne = fdonnees.readline() 
			l = ligne.split()
			# on transforme les chaînes de caractères en entiers
			l = [int(i) for i in l]
			j = job.Job(i, l)
			self.l_job += [j]
		# fermeture du fichier
		fdonnees.close()
		
	
	# exo 4 A REMPLIR
	def creer_liste_NEH(self):
		"""renvoie une liste selon l'ordre NEH"""
		sorted_jobs = sorted(self.l_job, key=lambda job : job.duree(), reverse=True)

		best_order = []
		for job in sorted_jobs :
			minD = MAXINT
			best_pos = 0
			for i in range(0,len(best_order) +1) :
				ordo = ordonnancement.Ordonnancement(self.nb_machines)
				new_list = [j for j in best_order]
				new_list.insert(i,job)
				ordo.ordonnancer_liste_job(new_list)
				if ordo.duree() < minD :
					minD = ordo.duree()
					best_pos=i
			best_order.insert(best_pos,job)
		return best_order

	# exo 5 A REMPLIR

	# calcul de r_kj tenant compte d'un ordo en cours
	def calculer_date_dispo(self, ordo, machine, job):
		if machine == 0 : 
			return 0
		else :
			ordoTemp = ordonnancement.Ordonnancement(ordo.nb_machines)
			ordoTemp.ordonnancer_liste_job(ordo.sequence())
			ordoTemp.ordonnancer_job(job)
			time = ordoTemp.date_debut_operation(job, machine)
			return time
	
	# calcul de q_kj tenant compte d'un ordo en cours
	def calculer_duree_latence(self, ordo, machine, job):
		ordoTemp = ordonnancement.Ordonnancement(ordo.nb_machines)
		ordoTemp.ordonnancer_liste_job(ordo.sequence())
		ordoTemp.ordonnancer_job(job)
		return ordoTemp.date_disponibilite(ordoTemp.nb_machines-1) - ordoTemp.date_disponibilite(machine)

	# calcul de la somme des durées des opérations d'une liste
	# exécutées sur une machine donnée
	def calculer_duree_jobs(self, machine, liste_jobs):
		return sum([job.duree_operation(machine) for job in liste_jobs])

	# calcul de la borne inférieure en tenant compte d'un ordonnancement en cours
	def calculer_borne_inf(self, ordo, liste_jobs):
		if len(liste_jobs) == 0 :
			return ordo.duree()
		LB = []
		for machine in range(0,self.nb_machines) :
			minR = MAXINT
			sumP = self.calculer_duree_jobs(machine, liste_jobs)
			minQ = MAXINT
			for job in liste_jobs :
				t = self.calculer_date_dispo(ordo, machine, job)
				if t<minR :
					minR = t
				u = self.calculer_duree_latence(ordo, machine, job)
				if u <minQ :
					minQ=u
			LB.append(minR + sumP + minQ)
		return max(LB)

	# exo 6 A REMPLIR
	
	# procédure par évaluation et séparation
	def evaluation_separation(self):
		nbSom = 0
		heap = []
		som = sommet.Sommet([], self.l_job, 0, nbSom)
		heapq.heappush(heap,som)
		minLB = MAXINT
		bestSolu = None
		while len(heap) != 0 : 
			s = heapq.heappop(heap)
			if len(s.jobs_non_places())==0 and s.evaluation() < minLB :
				minLB = s.evaluation()
				bestSolu = s
			for j in s.jobs_non_places() :
				tempO = ordonnancement.Ordonnancement(self.nb_machines)
				newSeq = s.sequence() + [j]
				nonPlace = [np for np in s.jobs_non_places()]
				nonPlace.remove(j)
				tempO.ordonnancer_liste_job(newSeq)
				tempLB = self.calculer_borne_inf(tempO, nonPlace)
				if tempLB < minLB :
					nbSom= nbSom +1
					tempS = sommet.Sommet(newSeq, nonPlace, tempLB ,nbSom)
					heapq.heappush(heap, tempS) 
		return bestSolu.sequence()

if __name__ == "__main__":
	# Initialisation des jeux de données
	jeu1 = Flowshop(0,0,[])
	jeu1.definir_par("jeu1.txt")
	
	jeu2 = Flowshop(0,0,[])
	jeu2.definir_par("jeu2.txt")
	
	# Test NEH
	l1 = jeu1.creer_liste_NEH()
	ordoNEH1 = ordonnancement.Ordonnancement(jeu1.nb_machines)
	ordoNEH1.ordonnancer_liste_job(l1)
	
	l2 = jeu2.creer_liste_NEH()
	ordoNEH2 = ordonnancement.Ordonnancement(jeu2.nb_machines)
	ordoNEH2.ordonnancer_liste_job(l2)
	
	# Test LB
	ordoLB1 = ordonnancement.Ordonnancement(jeu1.nb_machines)
	LB1 = jeu1.calculer_borne_inf(ordoLB1, jeu1.l_job)
	
	ordoLB2 = ordonnancement.Ordonnancement(jeu2.nb_machines)
	LB2 = jeu2.calculer_borne_inf(ordoLB2, jeu2.l_job)
	
	# Test separation et evaluation
	ordoES1 = ordonnancement.Ordonnancement(jeu1.nb_machines)
	seq1 = jeu1.evaluation_separation()
	ordoES1.ordonnancer_liste_job(seq1)
	
	ordoES2 = ordonnancement.Ordonnancement(jeu2.nb_machines)
	seq2 = jeu2.evaluation_separation()
	ordoES2.ordonnancer_liste_job(seq2)
	
	# Affichage NEH
	print("_____________ Ordonnancement NEH _____________")
	print("Resultat du jeu de test n°1 : ")
	ordoNEH1.afficher()
	print("Resultat du jeu de test n°2 : ")
	ordoNEH2.afficher()
	
	# Affichage LB
	print("_____________ Borne inferieur _____________")
	print("Jeu 1, borne inf = ",str(LB1))
	print("Jeu 2, borne inf = ",str(LB2))
	print("")
	
	# Affichage optimum
	print("_____________ Separation et evaluation _____________")
	print("Resultat optimal du jeu de test n°1 : ")
	ordoES1.afficher()
	print("Resultat optimal du jeu de test n°2 : ")
	ordoES2.afficher()