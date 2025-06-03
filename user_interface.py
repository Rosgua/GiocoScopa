from pattern_observer import Observer

class UserInterface(Observer):
    """Gestisce l'interazione con l'utente tramite console."""
    def __init__ (self, gamesystem):
        self.gs = gamesystem

    def displayGameBoard(self):
        "Mostra le carte presenti sul tavolo da gioco."
        print("Carte sul tavolo: ")
        if self.gs.gameboard.GBcards:
            for c in self.gs.gameboard.GBcards:
                print(f" {c.number} di {c.suit}")
        else:
            print('[Tavolo vuoto]')

    def notify(self):
        """Esplicita l'inizio di un nuovo turno e permette l'aggiornamento"
        delle carte sul tavolo e in mano al giocatore. """
        print("Nuovo Turno")
        self.displayCardsP()
        self.displayGameBoard()

    def displayCardsP(self):
        """Mostra le carte in mano al giocatore"""
        print('Le tue carte : ')
        for c in self.gs.Hplayer.handCard:
            print(f"{c.number} di {c.suit}")
        
    def getUsername(self)-> str:
        """Chiede all'utente di inserire il proprio username e lo restiruisce"""
        username = input("Inserisci il tuo username: ")
        return username

    def promptStart(self)-> str:
        """Chiede all'utene se vuole iniziare una nuova partita.
        Puoi scegliere se scrivere si o no."""
        risposta = input("Vuoi iniziare una partita?(si/no)")
        return risposta =='si'
    
    def PromptScelta(self):
        scelta = input("Scegli una carta da giocare: ")
        return scelta
    
 