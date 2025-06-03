import streamlit as st
import os
import random

from gestione_mazzo import Deck, Card, GameBoard
from gestione_giocatori import HumanPlayer, PlayerAI, str_to_card
from gs import GameSystem, TurnManager 

# Inizializzazione dello stato della sessione Streamlit
# Questo blocco serve a preservare le variabili tra le interazioni dell'utente
if 'game_system' not in st.session_state:
    st.session_state.game_system = None
    st.session_state.game_started = False
    st.session_state.username = ""
    st.session_state.messages = [] 
    st.session_state.player_card_choice = None 
    st.session_state.current_turn_player_name = "Human" 
    st.session_state.current_player_object = None 
    st.session_state.game_over = False 
    st.session_state.final_results_message = ""

def add_message(message):
    """
    Aggiunge un messaggio alla lista dei messaggi da visualizzare nell'interfaccia Streamlit.
"""
    st.session_state.messages.append(message)

class StreamlitUI:
    """
    Classe che gestisce l'interfaccia utente tramite Streamlit.

     """
    def __init__(self, gs_instance):
        self.gs = gs_instance

    def reset_game(self):
        """
        Reimposta tutte le variabili di stato per iniziare una nuova partita.
        """
        st.session_state.game_system = None
        st.session_state.game_started = False
        st.session_state.username = ""
        st.session_state.messages = []
        st.session_state.player_card_choice = None
        st.session_state.current_turn_player_name = "Human"
        st.session_state.current_player_object = None
        st.session_state.game_over = False
        st.session_state.final_results_message = ""

    def display_game_board(self):
        """
        Mostra le carte attualmente sul tavolo.  """
        return self.gs.gameboard.GBcards if self.gs.gameboard.GBcards else []

    def _on_card_button_click(self, card_str_choice):
        """
        Gestisce il click su una carta da parte del giocatore umano.
            """
        if st.session_state.current_turn_player_name == "Human":
            if handle_player_turn(card_str_choice):
                if not check_and_redistribute_cards():
                    end_game_logic()
                    st.rerun()
                else:
                    st.session_state.game_system.TurnManager.nextTurn()
                    st.session_state.current_turn_player_name = "AI"
                    st.session_state.current_player_object = st.session_state.game_system.playerAI
                    st.rerun()
        else:
            add_message("Non è il tuo turno. Attendi la mossa dell'AI.")
            st.rerun()

    def display_player_hand(self):
        """
        Mostra le carte nella mano del giocatore.
        """
        return self.gs.Hplayer.handCard if self.gs.Hplayer.handCard else []

    def display_messages(self):
        """
        Visualizza tutti i messaggi nella UI e li svuota dopo la visualizzazione.
        """
        for msg in st.session_state.messages:
            st.info(msg)
        st.session_state.messages = []

# --- Funzioni di logica di gioco ---

def start_game_logic():
    """
    Avvia una nuova partita creando un GameSystem e impostando il turno iniziale.
    """
    st.session_state.game_system = GameSystem()
    gs = st.session_state.game_system
    gs.startGame(st.session_state.username)
    st.session_state.game_started = True
    st.session_state.current_turn_player_name = "Human"
    st.session_state.current_player_object = gs.Hplayer
    st.rerun()

def handle_player_turn(card_str_choice):
    """
    Gestisce la mossa del giocatore umano.
    Restituisce True se la mossa è valida, False altrimenti.
    """
    gs = st.session_state.game_system
    try:
        chosen_card = str_to_card(card_str_choice)
        if chosen_card not in gs.Hplayer.handCard:
            add_message(f"La carta '{card_str_choice}' non è nella tua mano. Scegli una carta valida.")
            return False

        add_message(f"{gs.Hplayer.username} gioca: {card_str_choice}")
        result = gs.Hplayer.playCard(card_str_choice)
        if result == 'Scopa':
            add_message(f"Risultato della tua mossa : {result}")
        st.session_state.game_system = gs
        return True
    except Exception as e:
        add_message(f"Errore giocando la tua carta: {e}")
        return False

def handle_ai_turn():
    """Gestisce la mossa del giocatore AI. Restituisce True se la mossa 
    AI è stata eseguita, False se non ha potuto giocare.
    """
    gs = st.session_state.game_system
    add_message("--- Turno AI ---")
    card_ai_str = gs.playerAI.chooseMove()
    if not card_ai_str:
        add_message("AI non è riuscita a scegliere una mossa valida.")
        return True

    chosen_card = str_to_card(card_ai_str)
    if chosen_card not in gs.playerAI.handCard:
        add_message(f"AI ha selezionato una carta non valida: {card_ai_str}. Tentativo di fallback.")
        if gs.playerAI.handCard:
            fallback_choice = random.choice(gs.playerAI.handCard)
            card_ai_str = f"{fallback_choice.number} di {fallback_choice.suit}"
            add_message(f"AI gioca una carta casuale: {card_ai_str}")
        else:
            add_message("AI non ha carte da giocare.")
            return True

    add_message(f"AI gioca: {card_ai_str}")
    result = gs.playerAI.playCard(card_ai_str)
    if result == 'Scopa':
        add_message(f"Risultato della mossa dell'AI: {result}")
    st.session_state.game_system = gs
    return True

def check_and_redistribute_cards():
    """Controlla se le mani sono vuote e, se ci sono carte nel mazzo, le distribuisce.
      Restituisce True se la distribuzione è avvenuta o non necessaria, False se il mazzo è finito.
    """
    gs = st.session_state.game_system
    if not gs.Hplayer.handCard and not gs.playerAI.handCard:
        if gs.deck.cards:
            add_message("=== Nuova distribuzione di carte ===")
            gs.deck.distribute(gs.Hplayer)
            gs.deck.distribute(gs.playerAI)
            st.session_state.game_system = gs
        else:
            return False
    return True

def end_game_logic():
    """Conclude la partita, calcola i punteggi e aggiorna lo stato finale."""
    gs = st.session_state.game_system
    add_message("Partita terminata!")
    gs.calcul
