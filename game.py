import pygame
from client import Client
import time
import random


class Player:
    width = height = 50

    def __init__(
        self,
        ID,
        in_game,
        already_played,
        my_turn,
        my_hand,
        round_over,
        my_cards,
        color=(200, 0, 0),
    ):
        self.ID = ID
        self.IN_GAME = in_game
        self.ALREADY_PLAYED = already_played
        self.MY_TURN = my_turn
        self.MY_HAND = my_hand
        self.ROUND_OVER = round_over
        self.MY_CARDS = my_cards
        self.color = color

status = ""
drawBeginner = 0

class Game:
    def __init__(self, w, h):
        self.net = Client()
        self.width = w
        self.height = h
        self.player = Player(self.net.id, already_played=0, in_game=1, my_turn=0, my_hand=0, round_over=0, my_cards="x")
        self.player2 = Player(self.net.id, already_played=0, in_game=0, my_turn=0, my_hand=0, round_over=0, my_cards="x")
        self.canvas = Canvas(self.width, self.height, "BLACK JACK")
        self.cards = [
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        ]
        random.shuffle(self.cards)
        
    def calcCard(self,card):
            if(card == 'A'): return '1'
            if(card == 'J'): return '10'
            if(card == 'Q'): return '10'
            if(card == 'K'): return '10'
            return card
    def updatePlayer(self):
        # "ID:IN_GAME,ALREADY_PLAYED,MY_TURN,MY_HAND,ROUND_OVER,MY_CARDS"
        (
            self.player2.IN_GAME,
            self.player2.ALREADY_PLAYED,
            self.player2.MY_TURN,
            self.player2.MY_HAND,
            self.player2.ROUND_OVER,
            self.player2.MY_CARDS
        ) = self.parse_data(self.send_data())
        

    def run(self):
        clock = pygame.time.Clock()
        run = True
        global status
        initialPurchase = True
        showPlayer2 = False
        # Send Network Stuff ---- # "ID:IN_GAME,ALREADY_PLAYED,MY_TURN,MY_HAND,ROUND_OVER,MY_CARDS"
        
        while run:
            # time.sleep(0.3)
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False
            keys = pygame.key.get_pressed()

            # Update Canvas
            self.canvas.draw_background()

            if self.player2.IN_GAME == 0 and self.player.IN_GAME == 1:
                status = "Aguardando outro jogador"
                self.updatePlayer()
            elif (self.player2.IN_GAME == 1 and self.player2.ALREADY_PLAYED == 0) and self.player.IN_GAME == 0: 
                self.player.IN_GAME = 0
                self.player.ALREADY_PLAYED = 0 # esse cara vai dizer se ele já jogou um vez
                self.player.MY_TURN = 0
                status = "O outro jogador quer jogar!"
                self.updatePlayer()
            else:
                showPlayer2 = True
                            
            if(self.player.ROUND_OVER == 1 or self.player2.ROUND_OVER == 1 or self.player.MY_TURN == 1):
                self.updatePlayer()
                
            if (self.player.IN_GAME == 1 and self.player2.IN_GAME == 1) and self.player.ALREADY_PLAYED == 0:
                if(initialPurchase):
                    card1 = self.cards.pop(0)
                    card2 = self.cards.pop(0)
                    print("pop",card1, card2)
                    self.player.MY_CARDS = "["+(card1)+"]"+ "["+(card2)+"]"
                    self.player.MY_HAND = int(self.calcCard(str(card1))) + int(self.calcCard(str(card2)))
                    initialPurchase = False
                    self.updatePlayer() 
                    
                #verificar se o adversário comprou mais do que 21
                if(self.player2.MY_HAND > 21):
                    # self.player.MY_TURN = 1
                    self.player.ALREADY_PLAYED = 1
                    self.updatePlayer()
                     
                if self.player.MY_TURN == 0 and self.player2.MY_TURN == 0:
                        status = "Use S para sortear quem começa!"
                        
                        if keys[pygame.K_s]:
                            self.player.MY_TURN = 1
                            print("turn = ", str(self.player2.MY_TURN))
                            time.sleep(0.5)
                        self.updatePlayer()
                #Quer dizer que posso comprar ou passar
                if self.player2.MY_TURN == 1 and self.player.ALREADY_PLAYED != 1:
                    status = "Sua vez de jogar!"
                    self.player.MY_TURN = 0
                    #Comprar Carta
                    if keys[pygame.K_c]:
                            card1 = self.cards.pop(0)
                            self.player.MY_CARDS += "["+(card1)+"]"  
                            self.player.MY_HAND += int(self.calcCard(card1)) 
                            if(self.player.MY_HAND > 21):
                                self.player.MY_TURN = 1
                                self.player.ALREADY_PLAYED = 1
                                self.player.ROUND_OVER = 1  
                            self.updatePlayer()
                            time.sleep(0.5)
                    #Passar a vez
                    if keys[pygame.K_p]:
                        self.player.MY_TURN = 1
                        self.player.ALREADY_PLAYED = 1
                        if(self.player.MY_HAND < self.player2.MY_HAND) and self.player2.ALREADY_PLAYED ==1:   
                            self.player.ROUND_OVER = 1 
                        self.updatePlayer()
                        status = "Aguarde o Adversário jogar!!"
                        time.sleep(0.5)
                else:
                    if(self.player.MY_TURN == 1 and self.player2.ALREADY_PLAYED != 1 and self.player.ROUND_OVER != 1):
                        status = "Aguarde o Adversário jogar!"
                        if(self.player2.IN_GAME != 1):
                            status = "Aguarde o Adversário aceitar jogar!"
                        self.updatePlayer()
             
            #Fim do Round, Verificar o resultado               
            if self.player.ALREADY_PLAYED == 1 and self.player2.ALREADY_PLAYED == 1:
                if (self.player2.ROUND_OVER == 1 and self.player.MY_HAND <= 21) or self.player.MY_HAND < self.player2.MY_HAND:
                    status = "Você Ganhou"

                if self.player.MY_HAND > 21:
                    status = "Você perdeu"
                    self.player.ROUND_OVER = 1
                    
                if self.player.MY_HAND < 21 and self.player2.MY_HAND < 21:
                    if (self.player.MY_HAND < self.player2.MY_HAND):
                        status = "Você perdeu"
                        self.player.ROUND_OVER = 1
                     
                if (self.player.MY_HAND == self.player2.MY_HAND): 
                    
                    if(self.player.ALREADY_PLAYED == 1 and self.player2.ALREADY_PLAYED == 1):
                        status = "Empate"
                
                self.player.IN_GAME = 0
                self.player.MY_TURN = 0
                self.updatePlayer()

                 
            #Começar novo Jogo
            if keys[pygame.K_j]:
                self.player.IN_GAME = 1
                self.player.ALREADY_PLAYED = 0 # esse cara vai dizer se ele já jogou um vez
                self.player.MY_TURN = 0
                self.player.MY_HAND = 0
                self.player.ROUND_OVER = 0
                self.cards = [
                    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
                    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
                    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
                    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
                ]
                random.shuffle(self.cards)
                initialPurchase = True
                showPlayer2 = False
                self.player.MY_CARDS = 'x'
                self.updatePlayer()
                time.sleep(0.5)
            
            #Meus Dados
            self.canvas.draw_text("Você", 36, 20, 20)
            self.canvas.draw_text("Mão "+str(self.player.MY_CARDS), 36, 20, 80)
            self.canvas.draw_text("Soma "+ str(self.player.MY_HAND), 36, 20, 140)
            
            #Dados do Adversário
            if(showPlayer2):
                self.canvas.draw_text("Adversário ", 36, self.width/2 +20, 20)
                self.canvas.draw_text("Mão "+ str(self.player2.MY_CARDS) , 36, self.width/2 +20, 80)
                self.canvas.draw_text("Soma "+ str(self.player2.MY_HAND), 36, self.width/2 +20, 140)
            
            #Instruções 
            self.canvas.draw_text("C - Comprar", 12,20, 200)
            self.canvas.draw_text("P - Passar", 12,20, 220)
            self.canvas.draw_text("J - Jogar de Novo", 12,20, 240)
            
            # status
            self.canvas.draw_text("Status = " + str(status), 15, 20, self.width - 20)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send status to server
        :return: None
        """
        # Protocol
        # "ID:IN_GAME,ALREADY_PLAYED,MY_TURN,MY_HAND,ROUND_OVER,MY_CARDS"
        data = (
            str(self.net.id)
            + ":"
            + str(self.player.IN_GAME)
            + ","
            + str(self.player.ALREADY_PLAYED)
            + ","
            + str(self.player.MY_TURN)
            + ","
            + str(self.player.MY_HAND)
            + ","
            + str(self.player.ROUND_OVER) 
            + ","
            +  str(self.player.MY_CARDS)        
        )
        reply = self.net.send(data)
        print(reply)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), str(d[5])
        except:
            return 0, 0, 0, 0, 0, 'x'


class Canvas:
    def __init__(self, w, h, name="None"):
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font("freesansbold.ttf", size)

        # create a text surface object,
        # on which text is drawn on it.
        text = font.render(text, True, (0, 0, 128))

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.midleft = (x, y)

        self.screen.blit(text, textRect)

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255, 255, 255))