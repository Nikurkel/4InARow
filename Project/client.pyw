import pygame
import pygame_gui
import json
import time
import threading
from data.network import Network
from data.button import Button
from data.load import Data

pygame.init()
pygame.font.init()

# converts received game state (json to object) (only variables)
class Game:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Client:
    # base layout: 1600 x 900 pixels
    # ref makes layout scalable
    def ref(self, x):
        return round(x*self.width/1600)

    def __init__(self):
        self.infos = pygame.display.Info()
        self.maxWidth = self.infos.current_w # get Monitor size
        self.specifiedWidth = 1000
        self.fullscreen = False
        self.data = Data("data/properties.txt")
        try:
            self.specifiedWidth = int(self.data.find("width"))
            if self.data.find("fullscreen").lower() == "true":
                self.fullscreen = True
            else:
                self.fullscreen = False
        except:
            pass

        if self.fullscreen:
            self.width = self.maxWidth
        else:
            self.width = self.specifiedWidth

        self.height = self.ref(900)
        if self.width == self.maxWidth:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.width, self.height))

        self.gui_manager = pygame_gui.UIManager((self.width, self.height))
        self.messageInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(self.ref(1075),self.ref(900)-35, self.ref(500), self.ref(25)),manager=self.gui_manager)
        self.messageInput.set_text_length_limit(30)

        self.buttonPos_x = [self.ref(4), self.ref(154), self.ref(304), self.ref(454), self.ref(604), self.ref(754), self.ref(904)]
        self.buttonPos_y = [self.ref(4), self.ref(154), self.ref(304), self.ref(454), self.ref(604), self.ref(754)]
        self.messagePos_x = self.ref(1075)
        self.messagePos_y = [self.ref(175), self.ref(225), self.ref(275), self.ref(325), self.ref(375), self.ref(425), self.ref(475), self.ref(525), self.ref(575), self.ref(625), self.ref(675), self.ref(725), self.ref(775)]
        self.messageIndex = [0, 13]

        self.colors =   {   "background":   (50,50,50),
                            "player1_1":    (50,50,150),
                            "player2_1":    (150,50,50),
                            "player1_2":    (150,150,150),
                            "player2_2":    (150,150,150),
                            "normal_text":  (10,10,10),
                            "buttons":      (100,100,100),
                            "chat":         (100,100,100)
                        }
        try:
            self.colors = self.data.findColorList("classic")
        except:
            print("classic theme not found")

        self.winAnimation = 0
        self.animationSpeed = 0.2
        
        self.btns = []
        for i, x in enumerate(self.buttonPos_x):
            self.btns.append(Button(f"{i+1}", x, self.buttonPos_y[0], self.colors["buttons"], self.colors["normal_text"], self.ref(142)))

        self.run = True
        print(self.data.find("server"),self.data.find("port"))
        self.n = Network(self.data.find("server"), int(self.data.find("port"))) # connection to server
        self.player = int(self.n.getPlayer())
        self.userNameThis = ""
        self.userNameOther = ""
        self.clock = pygame.time.Clock()
        self.messages = []
        self.ownMessages = []
        self.ownMessagesIndex = -1

        # update my color on running game instance
        if self.player == 0:
            c1 = self.colors["player1_1"]
            c2 = self.colors["player1_2"]
        else:
            c1 = self.colors["player2_1"]
            c2 = self.colors["player2_2"]

        self.n.send(f"command,/color this {'%02x%02x%02x' % c1} {'%02x%02x%02x' % c2}") # converts color tuple to hex String

    # frontend
    def drawBackground(self, window, colors, p, width, height, buttonPos_x, buttonPos_y, btns):
        pygame.draw.rect(window, colors["background"],(0, 0, width, height))
        fromButton = btns[0].width + self.ref(4) # column width
        gameWidth = buttonPos_x[-1] + fromButton # game width
        if p == 0:
            pygame.draw.rect(window, colors["player1_2"], (gameWidth, 0, width-gameWidth, buttonPos_x[0] + fromButton))
        else:
            pygame.draw.rect(window, colors["player2_2"], (gameWidth, 0, width-gameWidth, buttonPos_x[0] + fromButton))
        for x in buttonPos_x:
            pygame.draw.line(window, colors["normal_text"], (x + fromButton, 0), (x + fromButton, height))
        for y in buttonPos_y:
            pygame.draw.line(window, colors["normal_text"], (0, y + fromButton), (gameWidth, y+fromButton))
        
        pygame.draw.line(window, colors["normal_text"], (gameWidth, buttonPos_y[0] + fromButton), (width, buttonPos_y[0] + fromButton))

    def drawChat(self, window, colors, font, msgs, messagePos_x, messagePos_y, messageIndex):
        # only draw chat Background when message is drawn
        for y, i in zip(messagePos_y, msgs[messageIndex[0]:messageIndex[1]]):
            pygame.draw.rect(window,colors["chat"],(messagePos_x,y,self.ref(500),self.ref(40))) # background
            if i[0] == "0":
                color = colors["player1_1"]
            elif i[0] == "1":
                color = colors["player2_1"]
            else:
                color = colors["normal_text"]
            text = font.render(i[2:], 1, color)
            window.blit(text, (messagePos_x+self.ref(10), y+self.ref(8))) # message

    def drawElements(self, window, colors, game, font, p, btns, userNameThis, userNameOther):
        for button in btns:
            button.color = colors["buttons"]
            button.textColor = self.colors["normal_text"]
            button.draw(window, font)

        if p == 0:
            text = font.render(userNameThis, 1, colors["player1_1"])
        elif p == 1:
            text = font.render(userNameThis, 1, colors["player2_1"])

        window.blit(text, (self.ref(1050+550/2)-round(text.get_width()/2),self.ref(10)))

        text = font.render("wins", 1, colors["normal_text"])
        window.blit(text, (self.ref(1050+(550/4*3))-round(text.get_width()/2),self.ref(50)))

        text = font.render(str(game.wins[0]), 1, colors["player1_1"])
        window.blit(text, (self.ref(1050+(550/4*3 - 50))-round(text.get_width()/2),self.ref(100)))

        text = font.render(str(game.wins[1]), 1, colors["player2_1"])
        window.blit(text, (self.ref(1050+(550/4*3 + 50))-round(text.get_width()/2),self.ref(100)))

        text = font.render(":", 1, colors["normal_text"])
        window.blit(text, (self.ref(1050+(550/4*3))-round(text.get_width()/2),self.ref(100)))

        if game.nextPlayer == 1:
            if p == 0:
                text = font.render(f"{userNameThis}'s turn", 1, colors[f"player1_1"])
            else:
                text = font.render(f"{userNameOther}'s turn", 1, colors[f"player1_1"])
        else:
            if p == 1:
                text = font.render(f"{userNameThis}'s turn", 1, colors[f"player2_1"])
            else:
                text = font.render(f"{userNameOther}'s turn", 1, colors[f"player2_1"])
        window.blit(text, (self.ref(1050+550/4)-round(text.get_width()/2),self.ref(100)))

    def drawGame(self, window, colors, game, buttonPos_x, buttonPos_y, winAnimation):
        offset = (buttonPos_x[4]-buttonPos_x[3])/2 - buttonPos_x[0] # offset for centre of field / circle radius
        ring = self.ref(15) # outer ring

        for i, row in enumerate(game.state):
            for j , field in enumerate(row):
                if field == 1:
                    pygame.draw.circle(window, colors["player1_1"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, 0)
                    pygame.draw.circle(window, colors["player1_2"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, ring)
                if field == 2:
                    pygame.draw.circle(window, colors["player2_1"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, 0)
                    pygame.draw.circle(window, colors["player2_2"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, ring)
                if field == 3:
                    if winAnimation%2 == 0:
                        pygame.draw.circle(window, colors["player1_2"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, 0)
                        pygame.draw.circle(window, colors["player1_1"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, ring)
                    else:
                        pygame.draw.circle(window, colors["player1_1"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, 0)
                        pygame.draw.circle(window, colors["player1_2"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, ring)
                if field == 4:
                    if winAnimation%2 == 0:
                        pygame.draw.circle(window, colors["player2_2"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, 0)
                        pygame.draw.circle(window, colors["player2_1"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, ring)
                    else:
                        pygame.draw.circle(window, colors["player2_1"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, 0)
                        pygame.draw.circle(window, colors["player2_2"], (buttonPos_x[j]+offset, buttonPos_y[i+1]+offset), offset, ring)

    def redrawWindow(self, game):
        font = pygame.font.SysFont("", self.ref(40))
        self.drawBackground(self.window, self.colors, self.player, self.width, self.height, self.buttonPos_x, self.buttonPos_y, self.btns)
        self.drawChat(      self.window, self.colors, font, self.messages, self.messagePos_x, self.messagePos_y, self.messageIndex)
        self.drawElements(  self.window, self.colors, game, font, self.player, self.btns, self.userNameThis, self.userNameOther)
        self.drawGame(      self.window, self.colors, game, self.buttonPos_x, self.buttonPos_y, self.winAnimation)
        self.gui_manager.draw_ui(self.window)
        pygame.display.update()

    # backend
    def clientCommand(self, command):
        try:
            if command[0:5] == "color":

                if command[6:9] == "me1":
                    c = command[10:16]
                    if self.player == 0:
                        self.colors["player1_1"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                        c1 = self.colors["player1_1"]
                        c2 = self.colors["player1_2"]
                    else:
                        self.colors["player2_1"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                        c1 = self.colors["player2_1"]
                        c2 = self.colors["player2_2"]

                    self.n.send(f"command,/color this {'%02x%02x%02x' % c1} {'%02x%02x%02x' % c2}")

                elif command[6:9] == "me2":
                    c = command[10:16]
                    if self.player == 0:
                        self.colors["player1_2"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                        c1 = self.colors["player1_1"]
                        c2 = self.colors["player1_2"]
                    else:
                        self.colors["player2_2"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                        c1 = self.colors["player2_1"]
                        c2 = self.colors["player2_2"]
                        
                    self.n.send(f"command,/color this {'%02x%02x%02x' % c1} {'%02x%02x%02x' % c2}")

                elif command[6:16] == "background":
                    c = command[17:23]
                    self.colors["background"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

                elif command[6:13] == "buttons":
                    c = command[14:20]
                    self.colors["buttons"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                    for button in self.btns:
                        button.color = self.colors["buttons"]
                        button.textColor = self.colors["normal_text"]

                elif command[6:10] == "text":
                    c = command[11:17]
                    self.colors["normal_text"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

                elif command[6:10] == "chat":
                    c = command[11:17]
                    self.colors["chat"] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

            elif command[0:5] == "scale":
                self.width = int(command[6:])
                self.specifiedWidth = self.width
                self.height = self.ref(900)
                pygame.display.quit()
                pygame.display.init()
                self.window = pygame.display.set_mode((self.width, self.height))
                self.gui_manager = pygame_gui.UIManager((self.width,self.height))
                self.rescale()

            elif command[0:5] == "save ":
                try:
                    self.data.save(command[5:], self.colors)
                except:
                    print("failed saving")

            elif command[0:5] == "load ":
                try:
                    self.colors = self.data.findColorList(command[5:])

                    if self.player == 0:
                        self.n.send(f"command,/color this {'%02x%02x%02x' % (self.colors['player1_1'])} {'%02x%02x%02x' % (self.colors['player1_2'])}")
                    else:
                        self.colors["player1_1"], self.colors["player2_1"] = self.colors["player2_1"], self.colors["player1_1"]
                        self.colors["player1_2"], self.colors["player2_2"] = self.colors["player2_2"], self.colors["player1_2"]
                        self.n.send(f"command,/color this {'%02x%02x%02x' % (self.colors['player2_1'])} {'%02x%02x%02x' % (self.colors['player2_2'])}")
                except:
                    print("failed loading")

            elif command[0:] == "themes":
                self.n.send("message,my themes:")
                for i in self.data.listThemes():
                    self.n.send(f"message,{i}")

            elif command[0:4] == "ping":
                start = time.time()
                args = json.loads(self.n.send("get"))
                end = time.time()
                latency = round((end - start)*1000, 4)
                self.n.send(f"message,ping took {latency} ms")
            else:
                self.n.send(f"message,not a command {command}")

        except:
            pass

    def toggleFrame(self):
        while self.run:
            self.winAnimation += 1
            time.sleep(self.animationSpeed)

    def rescale(self):
        txt = self.messageInput.get_text()
        self.messageInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(self.ref(1075),self.ref(900)-35, self.ref(500), self.ref(25)),manager=self.gui_manager)
        self.messageInput.set_text_length_limit(30)
        self.messageInput.set_text(txt)

        self.buttonPos_x = [self.ref(4), self.ref(154), self.ref(304), self.ref(454), self.ref(604), self.ref(754), self.ref(904)]
        self.buttonPos_y = [self.ref(4), self.ref(154), self.ref(304), self.ref(454), self.ref(604), self.ref(754)]
        self.messagePos_x = self.ref(1075)
        self.messagePos_y = [self.ref(175), self.ref(225), self.ref(275), self.ref(325), self.ref(375), self.ref(425), self.ref(475), self.ref(525), self.ref(575), self.ref(625), self.ref(675), self.ref(725), self.ref(775)]

        self.btns = []
        for i, x in enumerate(self.buttonPos_x):
            self.btns.append(Button(f"{i+1}", x, self.buttonPos_y[0], self.colors["buttons"], self.colors["normal_text"], self.ref(142)))

    def input(self, game):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

                if event.key == pygame.K_RETURN:
                    self.sendMessage()

                if event.key == pygame.K_UP:
                    self.scrollUP()

                if event.key == pygame.K_DOWN:
                    self.scrollDown()

                if event.key == pygame.K_TAB:
                    self.toggleFullscreen()

            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickButton(event, game)
            
            if event.type == pygame.MOUSEWHEEL:
                self.adjustChat(event)
            
            self.gui_manager.process_events(event)
        if self.run:
            self.gui_manager.update(self.clock.tick(30))

    def quit(self):
        self.n.send("command,/close")
        pygame.quit()
        self.run = False

    def sendMessage(self):
        try:
            if self.messageInput.get_text()[0:2] == "//":
                self.clientCommand(self.messageInput.get_text()[2:])
            elif self.messageInput.get_text()[0] == '/':
                self.n.send(f"command,{self.messageInput.get_text()}")
            else:
                self.n.send(f"message,{self.messageInput.get_text()}")
            self.ownMessages.insert(0,self.messageInput.get_text())
            self.messageInput.set_text("")
            self.ownMessagesIndex = -1
        except:
            pass

    def scrollUP(self):
        self.ownMessagesIndex += 1
        if self.ownMessagesIndex >= len(self.ownMessages):
            self.ownMessagesIndex = len(self.ownMessages)-1
        else:
            self.messageInput.set_text(self.ownMessages[self.ownMessagesIndex])

    def scrollDown(self):
        self.ownMessagesIndex -= 1
        if self.ownMessagesIndex <= -1:
            self.ownMessagesIndex = -1
            self.messageInput.set_text("")
        elif self.ownMessagesIndex < len(self.ownMessages):
            self.messageInput.set_text(self.ownMessages[self.ownMessagesIndex])

    def toggleFullscreen(self):
        pygame.display.quit()
        pygame.display.init()
        if self.fullscreen:
            self.width = self.specifiedWidth
            self.height = self.ref(900)
            self.window = pygame.display.set_mode((self.width, self.height))
        else:
            self.width = self.maxWidth
            self.height = self.ref(900)
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.fullscreen = not self.fullscreen
        self.gui_manager = pygame_gui.UIManager((self.width,self.height))
        self.rescale()

    def clickButton(self, event, game):
        for button in self.btns:
            if button.click(event.pos) and game.ready:
                try:
                    self.n.send(button.text)
                except:
                    pass

    def adjustChat(self, event):
        if len(self.messages) > 13:
            self.messageIndex[0] -= event.y
            if self.messageIndex[0] < 0:
                self.messageIndex[0] = 0
            self.messageIndex[1] = self.messageIndex[0] + 13
            if self.messageIndex[1] > len(self.messages):
                self.messageIndex[1] = len(self.messages)
                self.messageIndex[0] = self.messageIndex[1] - 13

    def updateUser(self, game):
        if self.player == 0:
            self.userNameThis = game.userNames[0]
            self.userNameOther = game.userNames[1]

            self.colors["player2_1"] = tuple(game.colors["player2_1"])
            self.colors["player2_2"] = tuple(game.colors["player2_2"])

        elif self.player == 1:
            self.userNameThis = game.userNames[1]
            self.userNameOther = game.userNames[0]

            self.colors["player1_1"] = tuple(game.colors["player1_1"])
            self.colors["player1_2"] = tuple(game.colors["player1_2"])

    def updateChat(self, game):
        if self.messages != game.chat:
            self.messages = game.chat
            if len(self.messages) < 13:
                self.messageIndex[1] = len(self.messages)
                self.messageIndex[0] = 0
            else:
                # jump to new message
                self.messageIndex[0] = len(self.messages)-13 
                self.messageIndex[1] = len(self.messages)

    def main(self):
        self.timer = threading.Timer(self.animationSpeed, self.toggleFrame)
        self.timer.start()

        while self.run:
            try:
                args = json.loads(self.n.send("get"))
                game = Game(**args)
                pygame.display.set_caption(f"Game {game.id}")

                self.updateUser(game)
                self.updateChat(game)

                self.redrawWindow(game)
                self.input(game)
                self.clock.tick(60)
            except:
                self.run = False
                
            
c = Client()
c.main()