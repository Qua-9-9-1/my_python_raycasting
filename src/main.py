import tkinter
from tkinter import *
import sys
import math

def callback():
    print("called the callback!")

argv = sys.argv

#screen
window = tkinter.Tk()
window.title("RAY PODCASTING")
window.geometry("1920x1080")
window.minsize(width=500, height=300)

# #label
# l1 = Label(text="Les profs.")
# l1.pack(side=LEFT)

# #button

# bouton = Button(text="Quitter", command=window.quit)
# bouton.pack()

# #menu deroulant

# mainmenu = tkinter.Menu(window)
# menu = tkinter.Menu(mainmenu)
# menu.add_radiobutton(label="Colors", command=(callback))
# mainmenu.add_cascade(label="Preferences", menu=menu)

rays_nb = 100 + 1
minimap_dim = 40
rays_length = minimap_dim * 10

class Player:
    def __init__(self, pos, point):
        self.pos = [0, 0]
        self.point = 0
        self.angle = 0
        self.rays = [rays_nb]

window.config(background='#000000', cursor="cross", relief="flat")#, menu=mainmenu)


def load_map_from_file(argv, player, map_screen):
    with open(argv[1], 'r') as file_map:
        char_map = file_map.read()
    y = 0
    x = 0
    for i in range(len(char_map)):
        if char_map[i] == 'X':
            map_screen.create_rectangle(x, y, x + minimap_dim, y + minimap_dim, fill='#FFFFFF')
        if char_map[i] == 'P':
            player.point = map_screen.create_oval(x, y, x + minimap_dim / 2, y + minimap_dim / 2, fill='#FF0000')
            player.pos = [x, y]
        x += minimap_dim
        if char_map[i] == '\n':
            y += minimap_dim
            x = 0
    player.angle = 0

def display_rays(player, map_screen):
    for i in range(int(rays_nb / 2)):
        end_x = player.pos[0] + rays_length * math.cos(player.angle + math.radians(-i))
        end_y = player.pos[1] + rays_length * math.sin(player.angle + math.radians(-i))
        map_screen.coords(player.rays[i],
            player.pos[0] + minimap_dim / 4,
            player.pos[1] + minimap_dim / 4,
            end_x,
            end_y)

    for i in range(int(rays_nb / 2)):
        end_x = player.pos[0] + rays_length * math.cos(player.angle + math.radians(i))
        end_y = player.pos[1] + rays_length * math.sin(player.angle + math.radians(i))
        map_screen.coords(player.rays[int(rays_nb / 2) + i],
            player.pos[0] + minimap_dim / 4,
            player.pos[1] + minimap_dim / 4,
            end_x,
            end_y)

def draw_rays(player, map_screen):
    player.rays = [None] * rays_nb

    for i in range(int(rays_nb / 2)):
        end_x = player.pos[0] + rays_length * math.cos(player.angle + math.radians(-i))
        end_y = player.pos[1] + rays_length * math.sin(player.angle + math.radians(-i))
        player.rays[i] = map_screen.create_line(player.pos[0] + minimap_dim / 4,
            player.pos[1] + minimap_dim / 4,
            end_x,
            end_y,
            width=0.05, fill='#FFFF00')

    for i in range(int(rays_nb / 2)):
        end_x = player.pos[0] + rays_length * math.cos(player.angle + math.radians(i))
        end_y = player.pos[1] + rays_length * math.sin(player.angle + math.radians(i))
        player.rays[int(rays_nb / 2) + i] = map_screen.create_line(player.pos[0] + minimap_dim / 4,
            player.pos[1] + minimap_dim / 4,
            end_x,
            end_y,
            width=0.05, fill='#FFFF00')

def move_player(player, direction):
    player.pos[0] += minimap_dim / 8 * math.cos(player.angle + direction * math.pi / 180)
    player.pos[1] += minimap_dim / 8 * math.sin(player.angle + direction * math.pi / 180)
    display_rays(player, map_screen)
    map_screen.coords(player.point, player.pos[0], player.pos[1], player.pos[0] + minimap_dim / 2, player.pos[1] + minimap_dim / 2)

def change_angle(player, direction):
    player.angle += (10 * math.pi / 180) * direction
    if player.angle > (360 * math.pi / 180):
        player.angle %= (360 * math.pi / 180)
    if player.angle < (0 * math.pi / 180):
        player.angle += (360 * math.pi / 180)
    display_rays(player, map_screen)

player = Player([0, 0], 0)
map_screen = tkinter.Canvas(window, width=250, height=250, bg='#0055a0')
game_screen = tkinter.Canvas(window, width=1600, height=900, bg='#00eeee')
load_map_from_file(argv, player, map_screen)
draw_rays(player, map_screen)
window.bind("<Escape>", lambda event : window.quit())
window.bind("<z>", lambda event : move_player(player, 0))
window.bind("<q>", lambda event : move_player(player, 270))
window.bind("<s>", lambda event : move_player(player, 180))
window.bind("<d>", lambda event : move_player(player, 90))
window.bind("<Right>", lambda event : change_angle(player, 1))
window.bind("<Left>", lambda event : change_angle(player, -1))

map_screen.place(x=0, y=20)
game_screen.place(x=264, y=20)
window.tk.call('tk', 'scaling', 3.0)
window.mainloop()