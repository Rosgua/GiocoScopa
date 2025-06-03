from gestione_mazzo import Deck, GameBoard
from gestione_giocatori import HumanPlayer, PlayerAI
from pattern_observer import Subject,Observer
from typing import List
from user_interface import UserInterface
import abc

class GameSystem:
    """Gestisce la logica complessiva del gioco di Scopa."""
    def __init__(self):
        self.Hplayer= None
        self.ui = None
        self.deck = None
        self.playerAI= None
        self.gameboard = None 
        self.TurnManager = TurnManager() 
        self.ui = UserInterface(self)

    def startGame(self, username:str): 
        """Inizializza una nuova Partia di Scopa. 
        Aggiunge il riferimento agli altri oggetti, assicura
        che i gocatori abbiano il riferimento al gameboard,
        distribuisce le carte al gameboard e ai players. Infine,
        registra l'ui, i giocatori come observers e inizializza 
        primo turno."""
        #ui da usare solo per uso da terminale
        self.deck = Deck()
        self.Hplayer= HumanPlayer(username)
        self.playerAI= PlayerAI()
        self.gameboard = GameBoard()

        self.Hplayer.setGameBoard(self.gameboard)
        self.playerAI.setGameBoard(self.gameboard)

        self.deck.distribute(self.gameboard )
        self.deck.distribute(self.Hplayer)
        self.deck.distribute(self.playerAI )

        self.TurnManager.register(self.ui)
        self.TurnManager.register(self.Hplayer)
        self.TurnManager.register(self.playerAI)

        self.TurnManager.currentPlayerIndex = 2
        self.TurnManager.nextTurn()
    
    def gestionePartita(self):
        """Gestisce l'interfaccia quando viene avviata una nuova partita."""
        if not self.ui.promptStart() :
            print('Arrivederci')

        self.startGame(self.ui.getUsername())

        while True:

            if not self.deck.cards and  not self.playerAI.handCard and not self.Hplayer.handCard:
                break

            if not self.playerAI.handCard and not self.Hplayer.handCard:
                if not self.deck.cards:
                    pass
                else:
                    print("\n=== Nuova distribuzione di carte ===")
                    self.deck.distribute(self.Hplayer)
                    self.deck.distribute(self.playerAI)
                    self.ui.displayCardsP()
                self.ui.displayGameBoard()
                              
            if self.TurnManager.currentPlayerIndex ==1:
                scelta = self.ui.PromptScelta()
                try:
                    ris= self.Hplayer.playCard(scelta)
                    if ris == 'scopa':
                          print('Scopa!')
                except Exception:
                    print(f"Carta inserita in formato non valido")
            else:
                card_ai = self.playerAI.chooseMove()
                print(f"l'Ai ha giocato: {card_ai}")
                ris =self.playerAI.playCard(card_ai)
                if ris == 'Scopa':
                        print('Scopa!')
            self.TurnManager.nextTurn()
        
        print("Partita terminata")
        risultati = self.endGame()
        print(f'Risultati della partita: {risultati}')
        
        self.gestionePartita()

    def calculateScores(self): 
        "Permette di calcolare i punteggi finali."
        #Numero totale di carte raccolte.
        if len(self.Hplayer.collectedCard) > len(self.playerAI.collectedCard):
           self.Hplayer.score +=1
        elif len(self.Hplayer.collectedCard) < len(self.playerAI.collectedCard):
            self.playerAI.score +=1 
        #numero carte d'oro
        num_oro_p1 = sum(1 for c in self.Hplayer.collectedCard if c.suit == 'Oro')
        num_oro_p2 = sum(1 for c in self.playerAI.collectedCard if c.suit == 'Oro')

        if num_oro_p1 > num_oro_p2:
           self.Hplayer.score +=1
        elif num_oro_p1 < num_oro_p2:
            self.playerAI.score +=1

        #settebello
        settebello_p1 = any(c.number == 7 and c.suit == 'Oro' for c in self.Hplayer.collectedCard)
        settebello_p2 = any(c.number == 7 and c.suit == 'Oro' for c in self.playerAI.collectedCard)

        if settebello_p1:
            self.Hplayer.score += 1  # Aggiungi 1 punto al giocatore se ha il settebello
        if settebello_p2:
            self.playerAI.score += 1

        #primiera
        primiera_p1 = self.calculatePrimiera(self.Hplayer)
        primiera_p2 = self.calculatePrimiera(self.playerAI)
        if primiera_p1> primiera_p2:
           self.Hplayer.score +=1
        elif primiera_p2 > primiera_p1:
            self.playerAI.score +=1

        
    def calculatePrimiera(self,player):
        "Permette di calcolare la primiera per un dato giocatore."
        primiera_val = {7: 21, 6: 18, 1: 16, 5: 15, 4: 14, 3: 13, 2: 12, 10: 10, 9: 9, 8: 8}
        best_by_suit = {'Oro':None, 'Bastoni':None, 'Spade':None, 'Coppe':None}
    
        for card in player.collectedCard:
            current_best = best_by_suit[card.suit]
            if current_best is None or primiera_val[card.number]> primiera_val[current_best.number]:
                best_by_suit[card.suit] = card
            
        punteggio_tot= sum(primiera_val[v.number] for v in best_by_suit.values() if v is not None)
        return punteggio_tot
        
    def getWinner(self): 
        """Consente di dichiarare il vincitore, ossia
        il player che ha accumulato più punti."""
        if self.Hplayer.score > self.playerAI.score :
            return f"{self.Hplayer.username} Win"
        elif self.Hplayer.score == self.playerAI.score :
            return f"It's a Tie"
        else:
            return f"Ai Wins"

    def endGame(self):
        "Gestisce il termine della partita."
        self.calculateScores()
        winner = self.getWinner()
        return f"""
        Il tuo punteggio: {self.Hplayer.score}<br>
        Punteggio AI: {self.playerAI.score}<br>
        Vincitore: {winner}!
    """

class TurnManager(Subject):
    """Gestisce l'alternarsi dei turni tra i giocatori e 
    notifica gli observer."""
    def __init__(self):
        self.observers: List = []
        self.currentPlayerIndex:int = 2 #1 se fai uso web
    
    def register(self, ob:Observer):
        """Aggiunge un giocatore alla gestione dei turni."""
        self.observers.append(ob)

    def notifyAll(self):
        """Notifica i suoi observers, in particolare l'user 
        interface viene sempre notificato, i giocatori vengono
        notificati solo se è il proprio turno."""
        if len(self.observers) > 0:
            self.observers[0].notify()  # UI 
        if self.currentPlayerIndex == 1 and len(self.observers) > 1:
            self.observers[1].notify()  # HumanPlayer
        elif len(self.observers) > 2:
            self.observers[2].notify()  # PlayerAI
             
    def nextTurn(self):
        """Avanza al prossimo Turno che modifica il giocatore corrente"""
        self.currentPlayerIndex = 2 if self.currentPlayerIndex == 1 else 1
        self.notifyAll()

if __name__ == '__main__' :
    gs = GameSystem()  
    gs.gestionePartita()
    

