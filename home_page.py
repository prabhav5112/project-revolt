#Import required modules,as may in one line
import matplotlib.pyplot as plt,tkinter as tk,mysql.connector as sqltor,pandas as pd,numpy as np,math, tkinter.ttk as ttk
#Import tkinter modules
from tkinter import font,ttk,messagebox
#Import PIL modules
#from PIL import Image
#Import datetime modules
#from datetime import date,timedelta,datetime
#Import sqlalchemy
#from sqlalchemy import create_engine

BG_COLOR = "#fc8803"
FG_COLOR = "#03e3fc"
WIDTH = 300
EL_BG_COLOR = ["#e06666","#6acf3e","#9beb34","#eba434"]
theme = "light"
if theme == "dark":
	FG_COLOR,BG_COLOR = "white","gray15"
elif theme == 'light':
	FG_COLOR,BG_COLOR = "black","white"

#Connect to the MySQL database using mysql.connector
#cnx=sqltor.connect(host="localhost",user="ppk",password="sql876",database="project_bkup")
#Declare cursor object
#cursor=cnx.cursor()

def all_children (window) :
	_lst = window.winfo_children()
	for item in _lst :
		if item.winfo_children() :
			_lst.extend(item.winfo_children())
	return _lst

def theme_change():
	global theme,FG_COLOR,BG_COLOR,EL_BG_COLOR
	i = 0
	frame.configure(bg = 'gray15')
	if theme == "light":
		theme = "dark"
	else:
		theme = "light"
	photo = tk.PhotoImage(file = "Logos/rEVolt_{}.png".format(theme))
	title.configure(image = photo)
	title.image = photo
	if theme == "dark":
		FG_COLOR,BG_COLOR = "white","gray15"
	elif theme == 'light':
		FG_COLOR,BG_COLOR = "black","white"
	window.config(bg = BG_COLOR)
	for el in all_children(window):
		try:
			if el['bg'] not in EL_BG_COLOR:
				el['bg'] = BG_COLOR
				el['fg'] = FG_COLOR
			el['highlightbackground'] = FG_COLOR
		except:
			pass
	menu(menubar)
	pack_buttons()

def center_align(wdw,rval=False):
	w = wdw.winfo_reqwidth()
	h = wdw.winfo_reqheight()
	ws = wdw.winfo_screenwidth()
	hs = wdw.winfo_screenheight()
	x = (ws - w)/2.2
	y = (hs - h)/2.2
	if rval == True:
		return x-w,y-h
	else:
		wdw.geometry('+%d+%d' % (x, y))

def about():
	win = tk.Toplevel()
	if theme ==  "dark":
		FGCOLOR = BDCOLOR = "DarkSlateGray4"
	else:
		FGCOLOR = "#6aa84f"
		BDCOLOR = "#e06666"
	win['bg'] = BG_COLOR
	win.title("About")
	frame = tk.Frame(win,bg = BG_COLOR,highlightbackground = BDCOLOR, highlightthickness = 5)
	#heading = tk.Label(win,text = 'About The Project',font = (None ,12,"bold"),bg = BG_COLOR,fg = FGCOLOR).pack()
	t=tk.Label(frame,text='\nProvides accurate information on EVs \nand custom filters for market research\n and also automated EV purchase suggestions',bg = BG_COLOR,fg = FGCOLOR,font = (None ,12,"bold")).pack()
	credits = tk.Label(frame,text = '\nby\nPrabhav B Kashyap\nS Prajwall Narayana\nKrishnatejaswi S\nVinayak C',font = (None ,10,"bold"),bg = BG_COLOR,fg = FGCOLOR).pack()
	frame.pack()
	center_align(win)

#Initialise tk window
window = tk.Tk()
screen_width = window.winfo_screenwidth()
#COnfigure window background
window.config(bg = BG_COLOR)
#Set title for the window
window.title("Home Page")
#COnfigure the window geometry
window.geometry("1920x1080")
#Icon image
#p1 = Image("/home/prabhav/Desktop/RVCE/EL/EELE/{}.jpeg".format("ev.jpeg")) 
#Configure iconphoto
#window.iconphoto(False, p1) 
#Initialise window elements
# "#144be3" "#5214e3"

frame = tk.Frame(window)
heading = tk.Frame(window,bg = BG_COLOR)
bottomframe_left = tk.Frame(window,bg = BG_COLOR)
label = tk.Label(bottomframe_left,text = 'Explore by category',padx = 10,bg = EL_BG_COLOR[0],fg = FG_COLOR,pady = 10, highlightbackground = "black",highlightthickness = 1)
tw_btn = tk.Button(bottomframe_left,text = "Two wheelers",command = None, padx = 80, pady = 40, activebackground = "grey", font = ("Ubuntu mono" , 20), fg = "gray15")
fw_btn = tk.Button(bottomframe_left, text = "Four wheelers", command = None, padx = 320, pady = 40,activebackground = "grey", font = ("Ubuntu mono" , 20), fg = "gray15")

bottomframe_right = tk.Frame(window)
label_right = tk.Label(bottomframe_right,text = 'Search by brand',padx = 10,bg = EL_BG_COLOR[1],fg = FG_COLOR,pady = 10, highlightbackground = "black",highlightthickness = 1)
img_frame = tk.Frame(window,bg = BG_COLOR, highlightbackground= FG_COLOR, highlightthickness=5)
#vsclbr = tk.Scrollbar(img_frame, orient = 'vertical')
#vsclbr.pack(side = "right", fill = "y")
blog = tk.Label(img_frame, text = "According to an independent study by CEEW Centre for Energy Finance (CEEW-CEF), \nthe EV market in India will be a US$206 billion opportunity by 2030 if India maintains steady progress to meet its ambitious 2030 target.\n This would require a cumulative investment of over US$180 billion in vehicle production and charging infrastructure. Another report by India Energy Storage Alliance (IESA)\n projects that the Indian EV market will grow at a CAGR of 36% till 2026. The EV battery market is also projected to grow at a CAGR of 30 percent during the same period.", padx = 10,bg = "white",fg = FG_COLOR,pady = 10, highlightbackground = "black",highlightthickness = 1, font = (None,10,'bold'))
blog.pack(pady = 10)
#img_label = tk.Label(img_frame,text = '',padx = 10,bg = BG_COLOR,fg = FG_COLOR,pady = 10)
canvas = tk.Canvas(img_frame, bg = BG_COLOR,height = 120,width = 140)
logo = tk.PhotoImage(file="Logos/rEVolt_{}.png".format(theme))
title = tk.Label(heading,image = logo)
title.image = logo
#logo = tk.PhotoImage(file="Logos/rvce_logo.png")
#rvlogo = tk.Label(heading,image = logo)
#rvlogo.image = logo
#rvlogo.pack(anchor = tk.N,side = "left")
#admin_login_button = tk.Button(heading,text = "Login",padx = 20,bg = BG_COLOR,fg = FG_COLOR )
#Pack the heading
heading.pack()
#Configure the labels
#label.config(font=("None", 12,"bold"))
#img_label.config(font=("None", 12,"bold")) 
#Pack the label
#img_label.pack(fill = 'x',expand = True)
#Pack login button
#admin_login_button.pack(side = "right",anchor = tk.NE)
#Initialise refresh label,dt
dt = tk.Label(window, text = "Compare and choose between EVs",bg = BG_COLOR,fg = FG_COLOR, font = ("Helvetica",20))
#Pack the window title
title.pack(side = "top")
#Pack the label dt
dt.pack()
'''#Initialise a tk frame
frame = tk.Frame(window)
#Pack the frame
frame.pack(fill = 'x',side = 'top',anchor = tk.N)'''
#Initialise a tk menu
menubar = tk.Menu(window,bg = BG_COLOR,fg = FG_COLOR)
#Initialise file menu in the menubar
file = tk.Menu(menubar,tearoff = 0)
help = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label ='File', menu = file) 
menubar.add_cascade(label ='Help', menu = help) 
def pack_buttons():
	for widget in logo_frame.winfo_children():
		widget.destroy()
	i = 0
	for img in img_list:
		photo = tk.PhotoImage(file = "Logos/"+img+"_"+theme+".png")
		btn =  tk.Button(logo_frame, command = None, image = photo, activebackground = "black")
		btn.image = photo
		btn.grid(row = i//5,column = i%5,padx = 40, pady = 30)
		i += 1
#New comment
def menu(menubar):
	#Initialise file menu in the menubar
	menubar['bg'] = BG_COLOR
	menubar['fg'] = FG_COLOR
	file.delete(0,5)
	help.delete(0,1)
	#Add various options
	file.add_command(label ='Change theme', command = theme_change, background = BG_COLOR,foreground = FG_COLOR) 
	#file.add_command(label ='Open...', command = None,background = BG_COLOR,foreground = FG_COLOR) 
	file.add_command(label ='Admin logins', background = BG_COLOR,foreground = FG_COLOR) 
	file.add_command(label = "Backup",background = BG_COLOR,foreground = FG_COLOR ) 
	#Add a seperator
	file.add_separator(background = BG_COLOR) 
	#Add exit option
	file.add_command(label ='Exit',background = BG_COLOR,foreground = FG_COLOR, command = lambda : window.destroy())
	help.add_command(label ='About         ', command=about, background = BG_COLOR,foreground = FG_COLOR) 
	#Configure window to have menubar
	window.config(menu = menubar)
menu(menubar)
#Configure icon for tkinter window
photo = tk.PhotoImage(file = "Logos/ev.png")
window.iconphoto(True, photo)
img_frame.pack(side = "bottom",fill = "both", expand = True)
#Pack bottomframe_left
bottomframe_left.pack(side = "left",anchor = tk.N,fill = "x",expand = True)
#Pack bottomframe_right
bottomframe_right.pack(side = "right",anchor = tk.N,fill = "x",expand = True)
img_list = ["ather_logo","mg_logo","tata_logo", "hyundai_logo","hero_logo", "ola_logo","tvs_logo"]
logo_frame = tk.Frame(bottomframe_right, bg = BG_COLOR, borderwidth = 0)
pack_buttons()
#ather_btn.pack(side = "bottom",anchor = tk.S)
logo_frame.pack(side = "bottom", anchor = "c",fill = "both")


#Pack the label
label.pack(fill = 'x',anchor = tk.N)
#Pack the buttons
tw_btn.pack(side = 'bottom',fill = 'x',anchor = tk.S, padx = 40, pady = 20)
fw_btn.pack(side = 'bottom',fill = 'x',anchor = tk.S, padx = 40, pady = 20)
#Pack the label
label_right.pack(side = 'top',fill = 'x',anchor = tk.E)

#Create an image on canvas
#can_img = canvas.create_image((450,300),image = None)
#canvas.pack()      
#img = tk.PhotoImage(file="search_cropped.png")  
#x,y = center_align(img_frame,True)    
#print(x,y)
#canvas.create_image(80, 60, image=img)
#Pack the canvas
#canvas.pack(side = "right",expand = True,fill = 'both',anchor = tk.NE)
#Execution stops here
window.bind("<Control-w>",lambda : window.destroy())
window.mainloop()
print('Exit')
