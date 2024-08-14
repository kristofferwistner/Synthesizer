import pygame as pg
import numpy as np
import sys
import time

"""

Kilder:
Squarewave by Aurélien Dotpro from Noun Project (CCBY3.0). Hentet fra: https://thenounproject.com/icon/squarewave-538698/
sawtooth by Aurélien Dotpro from Noun Project (CCBY3.0). Hentet fra: https://thenounproject.com/icon/sawtooth-538692/
Sine Waves by Aurélien Dotpro from Noun Project (CCBY3.0). Hentet fra: https://thenounproject.com/icon/sine-waves-187988/

"""
FPS = 30

pg.init()
pg.mixer.init()
pg.font.init()


mein_font = pg.font.SysFont('Impact', 50)
mein_font2 = pg.font.SysFont('Impact', 25)

WIDTH = 1280
HEIGHT = 720

SIZE = (WIDTH, HEIGHT)
surface = pg.display.set_mode(SIZE)


clock = pg.time.Clock()

# Deklarer bool-verdier
SINE_toggle = True
SAW_toggle = False
SQUARE_toggle = False

# Definerer farger
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (52, 235, 147)
BLUE = (7, 69, 97)

# Importerer bilder og skalerer dem
bakgrunn = pg.image.load("bakgrunn2.jpg")
BK = pg.transform.scale(bakgrunn, SIZE)

saw = pg.image.load("saw.jpg")
SAW_img = pg.transform.scale(saw, (300,150))
square = pg.image.load("square.jpg")
SQUARE_img = pg.transform.scale(square, (300,150))
sine =  pg.image.load("sine2.jpg")
SINE_img = pg.transform.scale(sine, (300,150))


# Knytter tastaturknapper til noter
keyboardDick = {
    "a" : "C4",
    "w" : "C#4",
    "s" : "D4",
    "e" : "D#4",
    "d" : "E4",
    "f" : "F4",
    "t" : "F#4",
    "g" : "G4",
    "y" : "G#4",
    "h" : "A4",
    "u" : "A#4",
    "j" : "B4",
    "k" : "C5"
    }

# Noter til frekvensverdier
freqDick = {
    "C4" : 261.63,
    "C#4": 277.18,
    "D4" : 293.66,
    "D#4": 311.13,
    "E4" : 329.63,
    "F4" : 349.23,
    "F#4": 369.99,
    "G4" : 392,
    "G#4": 415.30,
    "A4" : 440,
    "A#4": 466.16,
    "B4" : 493.88,
    "C5" : 523.25
    }

balls_list = list(keyboardDick.keys())
balls2_list = list(keyboardDick.values()) # bare brukt for å sortere tastene


hvit_tang_tast_list = []
svart_tang_tast_list = []


for i in range(len(balls_list)):
    if "#" in balls2_list[i]:
        svart_tang_tast_list.append(balls_list[i])
    else:
        hvit_tang_tast_list.append(balls_list[i])


# Klasse for tangentene 
class Tangenter:
    def __init__(self, color, l, t, w, h, key):
        self.color = color
        self.l = l
        self.t = t
        self.w = w
        self.h = h
        self.key = key


    def draw(self, surface):
        pg.draw.rect(surface, self.color, (self.l, self.t, self.w, self.h))
        
        text_surface = mein_font.render(self.key.upper(), False, BLUE)
        surface.blit(text_surface, ((self.l + self.w/2)- 20, (self.t + self.h/2)))
        

hvit_tang_width = WIDTH/7 - 10
hvit_tang_height = 300

svart_tang_width = hvit_tang_width * 0.5
svart_tang_height = hvit_tang_height * 0.6

hvit_tang_liste = []
for i in range(7):
    hvit_tang_liste.append(Tangenter(WHITE, i*hvit_tang_width + 50, HEIGHT - hvit_tang_height, hvit_tang_width - 10, hvit_tang_height, hvit_tang_tast_list[i]))

l = 0 #brukes for å legge keyen til rektangelet
k = 0 #brukes i svart_tang for løkke
svart_tang_liste = [] #bare 5 svarte tangenter, som kommer med 0, 1, 3, 4, 5 hvite tangent
for i in range(6): #range er 6 siden vi skipper svart tangent et sted
    if k != 2:
        svart_tang_liste.append(Tangenter(BLACK, i*hvit_tang_width + 35 + hvit_tang_width/2 + 50, HEIGHT - hvit_tang_height, svart_tang_width, svart_tang_height, svart_tang_tast_list[l]))
        l += 1
    k += 1
    
alle_tang_liste = hvit_tang_liste + svart_tang_liste 


# Bytte farge på tangenten for å vise at du spiller på den
def changeColor(tast):
    for rek in alle_tang_liste:
        if rek.key == tast:
            rek.color = BLUE

def changeColorBack(tast):
    for rek in hvit_tang_liste:
        if rek.key == tast:
            rek.color = WHITE
    for rek in svart_tang_liste:
        if rek.key == tast:
            rek.color = BLACK

def updr_tangenter():
    
    for tang in hvit_tang_liste:
        tang.draw(surface)
    
    for tang in svart_tang_liste:
        tang.draw(surface)

# Tegner inn tekst i form av overskrift osv. 
def text():
    font1 = pg.font.SysFont("IMPACT", 70)
    font2 = pg.font.SysFont("IMPACT", 30)
    text = font1.render("SYNTHESIZER", True, WHITE)
    text_rect = text.get_rect()
    surface.blit(text, (1280//2 - text_rect.width//2,55))
    
    pitchU = font2.render("PITCH UP: P", True, GREEN)
    pitchD = font2.render("PITCH DOWN: O", True, GREEN)
    surface.blit(pitchU, (75, 55))
    surface.blit(pitchD, (75, 90))
    
    better = font2.render("BETTER THAN SERUM", True, GREEN)
    better_rect = better.get_rect()
    surface.blit(better, ((1280//2 - better_rect.width//2 ,30)))
    
# Denne funksjonen lager selve lyden ved hjelp av matte og ulike funksjoner. Returnerer en sound/lyd, men trenger en frekvens som input
def synth(frequency, duration=1.5, sampling_rate=44100):
    # Lager funksjonen
    frames = int(duration*sampling_rate)
    key = pg.key.get_pressed()

    if SAW_toggle:
        arr = np.sin(2*np.pi*frequency*np.linspace(0,duration, frames))
        arr = np.clip(arr*50, -10, 10)
        arr = np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) + np.exp(np.pi)
        SAW_img_toggle = True
        
        SQUARE_img_toggle = False
        SINE_img_toggle = False
        
    elif SQUARE_toggle:
        arr = np.sin(2*np.pi*frequency*np.linspace(0,duration, frames))
        arr = np.clip(arr*50, -1, 1)
        SQUARE_img_toggle = True
        
        SINE_img_toggle = False
        SAW_img_toggle = False
        
    elif SINE_toggle:
        arr = np.sin(2*np.pi*frequency*np.linspace(0,duration, frames))
        SINE_img_toggle = True
        
        SQUARE_img_toggle = False
        SAW_img_toggle = False
    
    """
    #Hardstyle kick
    arr = np.clip(arr*10, -1, 1)
    arr = np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) + np.exp(np.pi)
    """
    
    # Lager lyden
    sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())
    
    return sound

# Denne funksjonen tar inn en frekvens, sender den videre inn i synth-funksjonen og så spiller den lyden på høyttalerne 
def play(frequency):
    
    freq = synth(frequency)
    freq.set_volume(0.33)

    freq.play()
    freq.fadeout(1000)


# Klasse for alle de interaktive knappene på skjermen. 
class Button:
    def __init__(self, h, w, x, y, color, name = "", tcolor = BLACK):
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.color = color
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.click = False
        self.name = name
        self.tcolor = tcolor
        
    def draw(self):
        
        action = False
        # Får tak i museposisjonen på skjermen
        pos = pg.mouse.get_pos()
        self.click = False
        # Sjekker om museposisjonen ligger over knappen, og deretter sjekker om man trykker ned med venstre museklikk
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                action = True
            

        if pg.mouse.get_pressed()[0] == 0:
            self.click = False
            
        
        
        pg.draw.rect(surface, self.color, self.rect)
        
        text_surface = mein_font2.render(self.name, False, self.tcolor)
        if self.name == "SQUARE":
            surface.blit(text_surface, (self.x + self.w/6, self.y + self.h/3))
        else:
            surface.blit(text_surface, (self.x + self.w/4 , self.y + self.h/3))
        
        # Returnerer en verdi som tilsier at det skjer en handling, dvs om det blir trykket ned. Brukes senere i programmet
        return action

# Lager rammen rundt bildet av waveformen
Ramme_kort1 = Button(150,8,795,175, GREEN)
Ramme_kort2 = Button(150,8,1095,175, GREEN)
Ramme_lang1 = Button(8,300,800,175, GREEN)
Ramme_lang2 = Button(8,308,795,325, GREEN)
RAMME = [Ramme_kort1, Ramme_kort2, Ramme_lang1, Ramme_lang2]

# Lager de ulike knappene
SAW_button = Button(75,125, 400, 175, WHITE, "SAW")
SQUARE_button = Button(75,125,250,175, WHITE, "SQUARE")
SINE_button = Button(75,125,100,175, BLUE, "SINE", WHITE)
buttons = [SAW_button, SQUARE_button, SINE_button]


# Definerer hvilke taster du kan bruke til å spille på pianoet
taster = ["a","w","s","e","d","f","t","g","y","h","u","j","k"]

# Gjør at du kan "transpose"/pitche opp og ned lyden
def changeFreq(direction):
    global freqDick
    for ball in freqDick.keys():
        if direction == "up":
            freqDick[ball] *= 2
        if direction == "down":
            freqDick[ball] /= 2
            

        
running = True
mod = 1

while running:
    
    clock.tick(FPS)
    
    surface.blit(BK, (0,0))                    # tegner bakgrunn
    
    updr_tangenter()                           # tegner tangenter
    text()
    
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False
            
            
        if event.type == pg.KEYDOWN:
            key = str(event.unicode)
            if key in taster:
                play(freqDick[keyboardDick[key]])
                changeColor(key)
        # Det som skjer over er at om den keyen du trykker ned ligger i taster-listen, så kjøres keyen inn i keyboard-dictionarien og gir en note, og deretter sendes det inn i frekvens-dictionarien. Dette sendes tilslutt inn i play-funksjonen
                
        if event.type == pg.KEYUP:
            key = str(event.unicode)
            if key in taster:
               changeColorBack(key)
               
        
        if event.type == pg.KEYUP and str(event.unicode) != '' and str(event.unicode) in taster:
            key = str(event.unicode)+str(mod)
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_o:
                changeFreq("down")
            if event.key == pg.K_p:
                changeFreq("up")
            # Det over er for å pitche opp og ned ved bruk av "O" og "P"
            
            
            # Tegner inn knappene
    for i in buttons:
        i.draw()
        
        
        # Dersom return action == True, vil dette skje. Altså, om man trykker på SAW-knappen, vil dette skje. Saw blir togglet, og dersom man trykker på en annen, vil denne "slås" av. 
    if SAW_button.draw():
        SAW_toggle = True
        
        SQUARE_toggle = False
        SINE_toggle = False
        
        SAW_button.color = BLUE
        SQUARE_button.color = WHITE
        SINE_button.color = WHITE
        
        SAW_button.tcolor = WHITE
        SQUARE_button.tcolor = BLACK
        SINE_button.tcolor = BLACK
        
    
    elif SQUARE_button.draw():
        SQUARE_toggle = True
        
        SAW_toggle = False
        SINE_toggle = False
        
        SAW_button.color = WHITE
        SQUARE_button.color = BLUE
        SINE_button.color = WHITE
        
        SAW_button.tcolor = BLACK
        SQUARE_button.tcolor = WHITE
        SINE_button.tcolor = BLACK
        
        
    elif SINE_button.draw():
        SINE_toggle = True
        
        SQUARE_toggle = False
        SAW_toggle = False
        
        SAW_button.color = WHITE
        SQUARE_button.color = WHITE
        SINE_button.color = BLUE
        
        SAW_button.tcolor = BLACK
        SQUARE_button.tcolor = BLACK
        SINE_button.tcolor = WHITE
        

    # Dersom det er sant, vil den tegne en graf tilsvarende den knappen du trykket på. 
    if SINE_toggle:
        surface.blit(SINE_img,(800,175))
                
    elif SAW_toggle:
        surface.blit(SAW_img,(800,175))
        
    elif SQUARE_toggle:
        surface.blit(SQUARE_img,(800,175))
    
    # Tegner ramme rundt bildet
    for i in RAMME:
        i.draw()
    
    pg.display.update()


pg.mixer.quit()
pg.quit()
sys.exit()









