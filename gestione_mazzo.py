import random
from typing import List,Union

class Deck:
    """Rappresenta un mazzo di carte da scopa."""
    def __init__(self) -> List:
        """Inizializza un mazzo di 40 carte e le mescola."""
        suit = ['Oro','Bastoni','Spade','Coppe']
        number = [x for x in range(1,11)]
        self.cards = [Card(n,s)  for n in number for s in suit]
        random.shuffle(self.cards)
    
    def __repr__(self) ->str:
        return f"{self.cards}"
            
    def drawCards(self, n:int):
        """Rimuove un numero specificato dal mazzo e 
        restituisce le carte rimosse."""
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn
        
    def distribute(self, object ):
        """Distribuisce le carte rimosse dal mazzo con il
        metodo drawCards() e le distribuisce al Gameboard o 
        al player in base al tipo di input specificato."""
        if isinstance(object, GameBoard):
            cards = self.drawCards(4)
            object.addCard(cards)
        else:
            cards = self.drawCards(3)
            object.addCard(cards)
        
class Card:
    """Classe Card le cui istanza rappresentano le carte 
    del mazzo. Esse sono definite da un numero e un seme.
    """
    def __init__(self,number:int, suit:str):
        self.number = number
        self.suit = suit
    
    def __repr__(self)-> str:
        return f"({self.number}, {self.suit})"
    
    def __eq__(self,other)-> bool:
        if not isinstance(other, Card):
            return False
        return self.number == other.number and self.suit == other.suit
      
class GameBoard:
    """Rappresenta il tavolo da gioco. Esso è costituito da un
    set di carte proveniente dal mazzo. """
    def __init__(self):
        self.GBcards : List = []
    
    def addCard(self,new_cards:Union[List,Card] ):
        """Permette di aggiungere nuove carte opppure una
        sola alla lista Gbcards"""
        if isinstance(new_cards,list):
            self.GBcards.extend(new_cards)
        else:
             self.GBcards.append(new_cards)
    
    def removeCard(self, cards:Union[List,Card]):
        """Permette di rimuovere nuove carte opppure una
        sola alla lista Gbcards"""
        if not isinstance(cards, list):
            cards = [cards]
        for c in cards:
            if c in self.GBcards:
             self.GBcards.remove(c)
    
    def removeAll(self):
        """Rimuove tutte le carte dalla lista GBcards"""
        self.GBcards.clear() 

