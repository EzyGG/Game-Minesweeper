from tkinter import *
import random 

# minesweeper grid's lines
def msweeper_grid(nb_col, nb_row, dim, origin):
    x1= origin
    y1= origin
    x2 = x1 + (dim*nb_col)
    y2 = y1 + (dim*nb_row)
    col = 0
    # vertical lines
    while col <= nb_col:
        col+=1
        can.create_line(x1,y1,x1,y2,width=2, fill="black") 
        x1+=dim 
    x1 = origin
    ligne = 0
    # horizontal lines
    while ligne <= nb_row:
        ligne+=1
        can.create_line(x1,y1,x2,y1,width=2, fill="black") 
        y1+=dim 

def init_level():
    global nb_col, nb_row, nb_mines 
    level_ = level.get()
    # easy level
    if level_ == 1:
        nb_col, nb_row, nb_mines = Level.easy[0],Level.easy[1],Level.easy[2]
    # medium level  
    elif level_  == 2:
        nb_col, nb_row, nb_mines = Level.medium[0],Level.medium[1],Level.medium[2]
    # hard level
    else:
        nb_col, nb_row, nb_mines = Level.hard[0],Level.hard[1],Level.hard[2]
    can.configure(width=(nb_col*dim)+gap , height=(nb_row*dim)+gap)
    init_game()

def init_game():
    global nb_hiden_mines, nb_seen_tiles, playing, first_move
    playing = True
    first_move = True
    nb_seen_tiles = 0
    can.delete(ALL)
    nb_hiden_mines = nb_mines
    update_counter()  
    # tab_mine and tab_displayed init
    y = 0
    while y < nb_row:
        x = 1
        y += 1
        while x <= nb_col:
            tab_mine[x,y]= 0
            tab_displayed[x,y]= ""
            # grid's tiles
            can.create_rectangle((x-1)*dim+gap,(y-1)*dim+gap,x*dim+gap,y*dim+gap,width=0, fill="grey")
            x += 1
    msweeper_grid(nb_col, nb_row, dim, gap) # grid's lines
    # random positioning of mines
    nb_neighb_mines = 0
    while nb_neighb_mines < nb_mines:
        col = random.randint(1, nb_col)
        lig = random.randint(1, nb_row)
        if tab_mine[col, lig] != 9: 
            tab_mine[col, lig] = 9 # <-- mine : 9
            nb_neighb_mines += 1

def update_counter():
    mine_count.configure(text=str(nb_hiden_mines))
    tile_count.configure(text=str((nb_col*nb_row)-nb_seen_tiles))

# nb of neighboring mines
def nb_neighb_mines(col, row):
    if col > 1:
        min_col = col - 1
    else:
        min_col = 1
    if col < nb_col:
        max_col = col + 1
    else:
        max_col = col       
    if row > 1:
        min_row = row - 1
    else:
        min_row = 1
    if row < nb_row:
        max_row = row + 1
    else:
        max_row = nb_row
    nb_mines = 0
    index_row = min_row
    while index_row <= max_row:
        index_col = min_col
        while index_col <= max_col:
            if tab_mine [index_col,index_row] == 9:
                nb_mines += 1  
            # print(f"for ({row},{col}) , vérif ({index_row},{index_col})")     
            index_col += 1      
        index_row += 1
    return nb_mines

# display on tile the nb of neighboring mines
def display_nb_neighb_mines (nb_neighb_mines__, col, lig):
    global nb_hiden_mines,nb_seen_tiles
    # if empty (not seen)
    if tab_displayed[col, lig] == "":
        nb_seen_tiles = nb_seen_tiles + 1
        if (tab_displayed[col, lig] == "f"): # <-- flag
            nb_hiden_mines = nb_hiden_mines + 1
            nb_seen_tiles = nb_seen_tiles - 1
            update_counter()
        tab_displayed[col, lig] = nb_neighb_mines__
        # create a seen tile
        can.create_rectangle((col-1)*dim+gap+3,(lig-1)*dim+gap+3,col*dim+gap-3,lig*dim+gap-3,width=0, fill="whitesmoke")
        colors = ['blue','green','red','indigo','orange','blueviolet','darkblue','dark']
        can.create_text(col*dim-dim//2+gap, lig*dim-dim//2+gap,text=str(nb_neighb_mines__),fill=colors[nb_neighb_mines__-1],font='Arial 22')

# reveal a space without mine around a tile
def empty_no_mine_zone(col, row):
    global nb_hiden_mines, nb_seen_tiles
    if tab_displayed[col, row] != 0:
        if (tab_displayed[col, row] == "f"): # <-- flag
            nb_hiden_mines = nb_hiden_mines + 1
            nb_seen_tiles = nb_seen_tiles - 1
        # create a seen tile
        can.create_rectangle((col-1)*dim+gap+3, (row-1)*dim+gap+3,col*dim+gap-3, row*dim+gap-3, width=0, fill="whitesmoke")
        tab_displayed[col, row] = 0
        nb_seen_tiles = nb_seen_tiles + 1
        # checking vertical cross tiles
        if col > 1:
            nb_neighb_mines__ = nb_neighb_mines(col-1, row)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col-1, row)
            else:
                display_nb_neighb_mines(nb_neighb_mines__, col-1, row)
        if col < nb_col:
            nb_neighb_mines__ = nb_neighb_mines (col+1, row)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col+1, row)
            else:
                display_nb_neighb_mines(nb_neighb_mines__, col+1, row)
        if row > 1:
            nb_neighb_mines__ = nb_neighb_mines (col, row-1)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col, row-1)
            else:
                display_nb_neighb_mines(nb_neighb_mines__, col, row-1)
        if row < nb_row:
            nb_neighb_mines__ = nb_neighb_mines (col, row+1)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col, row+1)
            else:
                display_nb_neighb_mines (nb_neighb_mines__, col, row+1)
        # checking diagonal cross tiles
        if col > 1 and row > 1:
            nb_neighb_mines__ = nb_neighb_mines(col-1, row-1)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col-1, row-1)
            else:
                display_nb_neighb_mines(nb_neighb_mines__, col-1, row-1)
        if col > 1 and row < nb_row:
            nb_neighb_mines__ = nb_neighb_mines(col-1, row+1)
            if nb_neighb_mines__== 0:
                empty_no_mine_zone(col-1, row+1)           
            else:
                display_nb_neighb_mines(nb_neighb_mines__, col-1, row+1)
        if col < nb_col and row > 1:
            nb_neighb_mines__ = nb_neighb_mines(col+1, row-1)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col+1, row-1)
            else:
                display_nb_neighb_mines (nb_neighb_mines__, col+1, row-1)
        if col < nb_col and row < nb_row:
            nb_neighb_mines__ = nb_neighb_mines(col+1, row+1)
            if nb_neighb_mines__ == 0:
                empty_no_mine_zone(col+1, row+1)
            else:
                display_nb_neighb_mines(nb_neighb_mines__, col+1, row+1)
        update_counter()

def win():
    can.create_text((nb_col/2)*dim-15+gap, (nb_row/2)*dim-5+gap, text='Won !', fill='Lime green', font='Times 60')

def lose():
    global playing
    playing  = False
    # display of mines
    row = 0
    while row < nb_row:
        col = 1
        row += 1
        while col <= nb_col:
            if tab_mine[col, row] == 9 and tab_displayed[col, row] == "":
                can.create_image(col*dim-dim//2+gap,row*dim-dim//2+gap, image = im_mine)
            elif tab_displayed[col, row] == "f" and tab_mine[col, row] != 9 :
                can.create_image(col*dim-dim//2+gap,row*dim-dim//2+gap, image = im_miss) # <-- miss flag
            col +=1
    can.create_text((nb_col/2)*dim-15+gap, (nb_row/2)*dim-5+gap, text='Failed !', fill='firebrick', font='Times 60')
    
# left click
def L_click(event):
    global nb_seen_tiles,first_move
    # disabled when fail or win screen
    if playing :
        # define the tile depending of the click's coordinates
        col = (event.x - gap) // dim +1
        row = (event.y - gap) // dim +1 
        if tab_displayed[col, row] == "":
            # if in the canvas
            if col>=1 and col<=nb_col and row>=1 and row<=nb_row:
                # avoid to first click on mine or on a single tile zone
                while nb_neighb_mines(col, row ) != 0 and first_move == True :
                    init_game()
                # click on mine
                if (tab_mine[col, row] == 9):
                    lose()
                else:
                    nb_neighb_mines__ = nb_neighb_mines(col, row )
                    if nb_neighb_mines__ >= 1:
                        display_nb_neighb_mines(nb_neighb_mines__, col, row ) 
                        update_counter()
                    # empty the no mine zone
                    else: 
                        empty_no_mine_zone(col, row)
            first_move = False
            if ((nb_col*nb_row) == nb_seen_tiles and nb_hiden_mines == 0):
                win()

# right click
def R_click(event):
    global nb_hiden_mines, nb_seen_tiles
    # disabled when fail or win screen
    if playing :
        # define the tile depending of the click's coordinates
        col = (event.x - gap)// dim+1
        row = (event.y - gap) // dim+1
        # empty --> flag
        if tab_displayed[col, row]=="":
            can.create_rectangle((col-1)*dim+gap+3,(row-1)*dim+gap+3,col*dim+gap-3,row*dim+gap-3,width=0, fill="whitesmoke")
            can.create_image(col*dim-dim//2+gap, row*dim-dim//2+gap,image = im_flag)
            tab_displayed[col, row]="f"
            nb_seen_tiles = nb_seen_tiles + 1
            nb_hiden_mines = nb_hiden_mines - 1
        # flag --> ?   
        elif tab_displayed[col, row] == "f":
            can.create_rectangle((col-1)*dim+gap+3,(row-1)*dim+gap+3,col*dim+gap-3,row*dim+gap-3,width=0, fill="grey")
            can.create_text(col*dim-dim//2+gap, row*dim-dim//2+gap,text="?", fill='black',font='Arial 20')
            tab_displayed[col, row] = "?"
            nb_seen_tiles = nb_seen_tiles - 1
            nb_hiden_mines = nb_hiden_mines + 1
        # ? -->
        elif tab_displayed[col, row] == "?":
            can.create_rectangle((col-1)*dim+gap+3,(row-1)*dim+gap+3,col*dim+gap-3,row*dim+gap-3,width=0, fill="grey")
            tab_displayed[col, row] = ""
        update_counter()
        # if ((nb_col*nb_row) == nb_seen_tiles and nb_hiden_mines == 0):
        #     win()

#-----------------------------------------------------------------------------
   
wind=Tk()
wind.title("Minesweeper")
wind.resizable(width=False, height=False)

class Level:
    easy = [10,10,15]
    medium = [15,15,35]
    hard = [20,20,85]
nb_col, nb_row, nb_mines = Level.easy[0],Level.easy[1],Level.easy[2] # ?????????????????????? 
dim, gap, nb_seen_tiles = 30,3,0
playing = True 
first_move = True
im_mine = PhotoImage(file = "mine.png")
im_miss = PhotoImage(file = "cross.png")
im_flag = PhotoImage(file = "flag.png")
tab_mine = {} 
tab_displayed = {} 

can=Canvas(wind, width=(nb_col*dim)+gap, height=(nb_row*dim)+gap, bg="grey")
can.bind("<Button-1>",L_click)
can.bind("<Button-3>",R_click)
can.pack(side=RIGHT)

# f1 <-- new game button
f1 = Frame(wind)
bou1 = Button(f1, width=14, text="New Game", font="Arial 10", command=init_game)
bou1.pack()
f1.pack(pady=10)

# f2 <-- radio buttons for levels
f2 = Frame(wind)
level=IntVar()
level.set(1)
case1=Radiobutton(f2,text='Easy', command=init_level, variable=level,value=1)
case1.grid(row=0,sticky=NW,padx=30)
case2=Radiobutton(f2,text='Medium', padx=3, command=init_level, variable=level,value=2)
case2.grid(row=1,sticky=NW,padx=30)
case3=Radiobutton(f2,text='Hard', padx=3, command=init_level, variable=level,value=3)
case3.grid(row=2,sticky=NW,padx=30)
f2.pack()

# f3 <-- mines and tiles count displays 
f3 = Frame(wind)
mine_label = Label (f3, text = "Remaining mines :")
mine_label.grid(row=4,column=1,sticky=NW)
mine_count = Label (f3, text = "100")
mine_count.grid(row=4,column=2,sticky=NE)
tile_label = Label (f3, text = "Tiles to treat :")
tile_label.grid(row=5,column=1,sticky=NW)
tile_count = Label (f3, text = "10")
tile_count.grid(row=5,column=2,sticky=NE)
f3.pack()

# f3 <-- minesweeper image
f4 = Frame(wind)
photo=PhotoImage(file="minesweeper.png")
label = Label(f4, image=photo)
label.pack(side=BOTTOM)
f4.pack(side=BOTTOM)

init_level()
wind.mainloop() 