class joueur:
  def __init__(self,nom):
    self._nom=nom
    self._etablissements=[]
    self._argent=3
    self._monuments=[]
  @property
  def nom(self):
    return self._nom
  @property
  def etablissements(self):
    return self._etablissements

  def recevoir(self,n):
    self._argent+=n
  def payer(self,n):
    if self._argent<n:
      raise ValueError("Pas assez d'argent")
      #la faudra voir comment mettre autre chose psq c'est bizarre de mettre une errorvalue genre si tout le jeu crash c'est chiant quoi
    else:
      self._argent-=n

  def ajouter_etablissement(self,etablissement):
    self._etablissements.append(etablissement)
  def retirer_etablissement(self,etablissement):
    self._etablissements.remove(etablissement)
  def possede_etablissement(self,etablissement):
    return etablissement in self._etablissements

  def a_gagne(self):
    if len(self._monuments)==4:
      return True
    else:
      return False
  def a_2_des(self):
    if "Gare" in self._monuments:
      return True
    else:
      return False
  def peut_relancer(self):
    if "Tour radio" in self._monuments:
      return True
    else:
      return False
  def relance_si_double(self):
    if "Parc d'atractions" in self._monuments:
      return True
    else:
      return False
  def gain_augmente(self):
    if "Centre commercial" in self._monuments:
      return True
    else:
      return False
  def ajouter_monument(self,monument):
    self._monuments.append(monument)



from abc import ABC, abstractmethod
class Carte(ABC):
  _COULEURS = {'Violet','Rouge','Bleu','Vert'}
  _CATEGORIE = {'rouage','blé','cochon','usine','cafe','tdt','pain','fruit'}
  def __init__(self,nom,cout):
    self._nom=nom
    self._cout=cout
  
  @property
  def nom(self):
    return self._nom
  @property
  def cout(self):
    return self._cout 



class etablissement(Carte):
  def __init__(self,nom,cout,categorie,couleur,numeros):
    super().__init__()
    self._categorie=categorie
    self._couleur=couleur
    self._numeros=numeros
  
  @property
  def categorie(self):
    return self._categorie
  @property
  def couleur(self):
    return self._couleur
  @property
  def numeros(self):
    return self._numeros
  
  def peut_activer(self, proprio, lanceur):
        match self._couleur:
            case "Bleu":
              return True
            case "Vert":
              return proprio==lanceur
            case "Violet":
              return proprio==lanceur
            case "Rouge":
              return proprio!=lanceur
  def achetable(self,proprio):
    if self._couleur == "Violet":
      return not self._nom in proprio.etablissements
    else:
      return True
  @abstractmethod
  def activer(self, proprio, joueur_actif=None):
    pass

#du coup la j'ai commencé a faires les sous classes dont je parlais redites moi si vous trouvez ça nul c'est ok
#et j'ai pas fini les cartes violettes psq jpense il manque une classe partie ou un truc qui réunit tout les joueurs qui jouent

class Etab_gain(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
  
  def activer(self, proprio, joueur_actif=None):
    bonus=0
    if proprio.gain_augmente():
      bonus=1
    proprio.recevoir(self._montant+bonus)

class Etab_gain_par_cat(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant,categorie_cible):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
    self._categorie_cible=categorie_cible
  
  def activer(self, proprio, joueur_actif=None):
    for etab in proprio.etablissements:
      if etab.categorie == self._categorie_cible:
        proprio.recevoir(self._montant)

class Etab_perte_lanceur(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
  
  def activer(self, proprio,joueur_actif=None):
    bonus=0
    if joueur_actif.gain_augmente():
      bonus=1
    joueur_actif.recevoir(self._montant+bonus)
    proprio.payer(self._montant+bonus)

class Stade(etablissement):
    def __init__(self):
        super().__init__("Stade",6,[6],"Violet","tdt")

    pass

class CentreAffaires(etablissement):
  pass

class ChaineTele(etablissement):
  pass