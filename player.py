from tkinter import *
from tkinter import filedialog
import pygame
import random

fenetre = Tk()
fenetre.title("Music Player")
fenetre.geometry("650x300")

duree_piste = 0
debut = 0
temps = IntVar()
boucle = False

pygame.init()
pygame.mixer.init()

#Ajoute une piste a la liste
def ajouter():
    piste = filedialog.askopenfilename(title="Ajouter une piste", filetypes=[("Audio","*.mp3")])
    pistes_audio.insert(END, piste)

#Supprime la piste de la liste
def supprimer():
    arreter()
    pistes_audio.delete(ACTIVE)

#Joue la piste selectionnée dans la liste
def jouer():

    global duree_piste
    global debut

    piste = pistes_audio.get(ACTIVE)

    duree_piste = pygame.mixer.Sound(piste).get_length()
    debut = 0

    barre_lecture.config(to=duree_piste*1000)
    
    fin_de_piste = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(fin_de_piste)

    pygame.mixer.music.load(piste)
    pygame.mixer.music.play()

    test_fin(fin_de_piste) 
    afficher_position()

#Arrete la piste
def arreter():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pistes_audio.selection_clear(ACTIVE)

#Pause/Reprend la piste
def pause():

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        afficher_position()

#Active/desactive la repetition de piste
def boucler():
    global boucle

    if boucle:
        boucle = False
        btn_boucle.config(image= btn_boucle_off_img)
    else:
        boucle = True
        btn_boucle.config(image= btn_boucle_img)
    pass

#Change le volume
def volume(vol):
    pygame.mixer.music.set_volume(int(vol)/100)

#Affiche la position dans la piste et maj la barre de lecture
def afficher_position():

    t = debut + pygame.mixer.music.get_pos()

    timer.config(text = f"{sec_en_min(t//1000)} / {sec_en_min(int(duree_piste))}")
    temps.set(t)

    if pygame.mixer.music.get_busy():
        timer.after(1000, afficher_position)
    else:
        timer.config(text="00:00 / 00:00")
        temps.set(0)

#Change la position dans la piste
def maj_position(pos):
    
    global debut
    pygame.mixer.music.play(0, float(pos)/1000)

    debut = int(pos)

#test si la fin de la piste a été atteinte
def test_fin(fin):

    global debut

    for event in pygame.event.get():
        if event.type == fin and boucle:
            debut = 0
            pygame.mixer.music.play()

    fenetre.after(100, lambda: test_fin(fin))

#Lance une piste au hasard
def aleatoire():

    pistes_audio.selection_clear(0, pistes_audio.size())
    piste_aleatoire = random.randint(0,pistes_audio.size()-1)

    pistes_audio.selection_set(piste_aleatoire)
    pistes_audio.activate(piste_aleatoire)
    
    jouer()

#Convertis seconde en minute
def sec_en_min(num):
    sec = num%60
    min = num//60
    return f"{min:0>2}:{sec:0>2}"



#Elements de l'interface
pistes_audio = Listbox(fenetre, font=('System',12), bg='grey20', fg='white')
barre_lecture = Scale(fenetre, from_=0 , to=duree_piste, variable= temps, orient=HORIZONTAL, command= maj_position, width=10, sliderlength=15, showvalue=0)
boutons = Frame(fenetre)
timer = Label(fenetre, text= "00:00 / 00:00")

btn_jouer_img = PhotoImage(file='images\play.png').subsample(2,2)
btn_pause_img = PhotoImage(file='images\pause.png').subsample(2,2)
btn_stop_img = PhotoImage(file='images\stop.png').subsample(2,2)
btn_boucle_img = PhotoImage(file='images\loop.png').subsample(2,2)
btn_boucle_off_img = PhotoImage(file='images\loop_off.png').subsample(2,2)
btn_ajout_img = PhotoImage(file='images\_add.png').subsample(2,2)
btn_suppr_img = PhotoImage(file='images\delete.png').subsample(2,2)
btn_aleatoire_img = PhotoImage(file='images\_random.png').subsample(2,2)


btn_jouer = Button(boutons, image=btn_jouer_img, width=70, command= jouer, height=60, font=('Arial',12), relief=FLAT)
btn_pause = Button(boutons, image=btn_pause_img, width=70, command= pause, height=60, font=('Arial',12), relief=FLAT)
btn_stop = Button(boutons, image=btn_stop_img, width=70, command= arreter, height=60, font=('Arial',12), relief=FLAT)
btn_boucle = Button(boutons, image=btn_boucle_off_img, width=70, command= boucler, height=60, font=('Arial',12), relief=FLAT)
btn_aleatoire = Button(boutons, image=btn_aleatoire_img, width=70, command= aleatoire, height=60, font=('Arial',12), relief=FLAT)

btn_ajouter = Button(boutons, image=btn_ajout_img, command= ajouter, width=70, height=60, text="+", font=('Arial',12), relief=FLAT)
btn_supprimer = Button(boutons, image=btn_suppr_img, command= supprimer, width=70, height=60, text="-", font=('Arial',12), relief=FLAT)

barre_volume = Scale(boutons, from_=0 , to=100, command= volume, width=10, sliderlength=15, orient=HORIZONTAL)


#Position dans l'interface
pistes_audio.pack(fill="both", expand="yes")
barre_lecture.pack(fill=X)
boutons.pack(anchor='center')
timer.pack()

btn_jouer.grid(row=0, column=2)
btn_pause.grid(row=0, column=3)
btn_stop.grid(row=0, column=4)
btn_boucle.grid(row=0, column=0)
btn_aleatoire.grid(row=0, column=1)

btn_ajouter.grid(row=0, column=6)
btn_supprimer.grid(row=0, column=7)

barre_volume.grid(row=0, column=8)


fenetre.mainloop()