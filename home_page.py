#Import required modules
import matplotlib.pyplot as plt,tkinter as tk,mysql.connector as sqltor,pandas as pd,numpy as np,math, tkinter.ttk as ttk
#Initialise constants used 
BG_COLOR = "#fc8803"
FG_COLOR = "#03e3fc"
WIDTH = 300
EL_BG_COLOR = ["#e06666","#6acf3e","#9beb34","#eba434"]
theme = "light"
if theme == "dark":
	FG_COLOR,BG_COLOR = "white","gray15"
elif theme == 'light':
	FG_COLOR,BG_COLOR = "black","white"
BG_THEMES = {"dark":{"tv_even": "seashell4","tv_odd" : "cadet blue","fg": "black","stv_even":"thistle4","stv_odd":"slate gray"},"light":{"tv_even": "light blue","tv_odd" : "LightSeaGreen","fg": "black","stv_even":"powder blue","stv_odd":"SteelBlue2"}}
tw_df = pd.read_csv("tw_dataset.csv")
fw_df = pd.read_csv("fw_dataset.csv")
fw_df = fw_df.dropna(how='all')
tw_df = tw_df.dropna(how='all')
tw_df.fillna(0,inplace=True)
fw_df.fillna(0,inplace=True)

#Define a function which returns a list of all widgets present on screen
def all_children (window) :
	_lst = window.winfo_children()
	for item in _lst :
		if item.winfo_children() :
			_lst.extend(item.winfo_children())
	return _lst

#Define a function to change the bg and fg colors if a user wants to change theme
def theme_change():
	global theme,FG_COLOR,BG_COLOR,EL_BG_COLOR
	#Change the ttk style depending upon the theme
	style = ttk.Style()
	style.configure('Treeview', rowheight=40,fieldbackground=FG_COLOR)
	style.configure("Treeview.Heading",background = FG_COLOR,foreground  = "tan4",padding = 10)
	style.configure("Vertical.TScrollbar", background=FG_COLOR, bordercolor=BG_COLOR, arrowcolor=BG_COLOR)
	#Change the theme depending upon its current value
	if theme == "light":
		theme = "dark"
	else:
		theme = "light"
	#Change the logos based on theme
	photo = tk.PhotoImage(file = "Logos/rEVolt_{}.png".format(theme))
	title.configure(image = photo)
	title.image = photo
	logo = tk.PhotoImage(file="Logos/rvce_logo_{}.png".format(theme))
	rvlogo.configure(image = logo)
	rvlogo.image = logo
	#Change fg and bg colour based on theme
	if theme == "dark":
		FG_COLOR,BG_COLOR = "white","gray15"
	elif theme == 'light':
		FG_COLOR,BG_COLOR = "black","white"
	#Configure the window background colour
	window.config(bg = BG_COLOR)
	#Change fg and bg colours of all elements
	for el in all_children(window):
		try:
			
			if el['bg'] not in EL_BG_COLOR:
				el['bg'] = BG_COLOR
				el['fg'] = FG_COLOR
		except:
			pass
	#Update the menubar
	menu(menubar)
	#Update the buttons depending upon the theme
	pack_buttons()
	
#Function to return the main screen	
def main_screen(tree_frame):
	#Kill the frame displaying the treeview
	tree_frame.destroy()
	#Pack the main screen elements
	heading.pack(fill = "x")
	dt.pack()
	img_frame.pack(side = "bottom",fill = "both", expand = True)
	bottomframe_left.pack(side = "left",anchor = tk.N,fill = "x",expand = True)
	bottomframe_right.pack(side = "right",anchor = tk.N,fill = "x",expand = True)

#Function to center align an element
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
		
def write_tree(df,tv,verscrlbr):
	# Store the column names in a list
	columns = list(df.columns)
	#Initialise d_tags to differentiate between odd and even rows
	d_tags = {0:"even",1:"odd"}
	#Set the columns of the treeview as "columns"
	tv["columns"]=(columns)
	#Store the length of the dataframe in a variable
	counter = len(df)
	#Ghost columns
	tv.column('#0', width=0)
	tv.heading('#0', text='', anchor="center")
	#Give headings to the treeview columns
	for x in range(len(columns)):
		if columns[x] == "Charging Time":
			tv.column(columns[x],width = 150, anchor="center")
		else:
			tv.column(columns[x],width = 60, anchor="center")
		tv.heading(columns[x], text=columns[x],command=lambda _col= columns[x]: treeview_sort_column(tv, _col, False))
	#Insert rows into the treeview
	for i in range(len(df)):
		tv.insert('', 0, values=list(df.iloc[i]), tag = d_tags[i%2])
	#Pack the treeview
	tv.pack(side ='top',fill = 'x')
	#Configure even rows to have a certain colour
	tv.tag_configure('even', background = BG_THEMES[theme]['stv_even'],foreground = BG_THEMES[theme]['fg']) 
	#Configure odd rows to have a certain colour
	tv.tag_configure('odd', background = BG_THEMES[theme]['stv_odd'],foreground = BG_THEMES[theme]['fg']) 
	#Set the command of the vertical scrollbar as the yview of the tree
	verscrlbr['command'] = tv.yview
	#Set yscrollcommand for the treeview
	tv.configure(yscrollcommand = verscrlbr.set)
	
def apply_filters(df,chk_var,tv,verscrlbr):
	#Initialise an empty list
	lst = []
	#Store all the non-empty variables in the list
	for var in chk_var:
		if var.get() != "":
			lst += [var.get()]
	#Clear the treeview list items
	for item in tv.get_children():
		tv.delete(item)
	#Create a new dataframe with filters applied
	new_df = df[df.Manufacturer.isin(lst)]
	#Update the treeview
	write_tree(new_df,tv,verscrlbr)

def tree(df,chk = 0):
	if type(df) == str:
		chk = 1
		mfr = df
		df = pd.concat([fw_df[fw_df["Manufacturer"] == df] ,tw_df[tw_df["Manufacturer"] == df]],axis=0) 
	tree_frame = tk.Frame(window,bg=BG_COLOR)
	widget_frame = tk.Frame(tree_frame, bg = BG_COLOR)
	tv_frame = tk.Frame(tree_frame, bg = BG_COLOR)
	treeview = ttk.Treeview(tv_frame, columns= df.columns, show='headings',height = len(df))
	verscrlbr = ttk.Scrollbar(tv_frame,orient ="vertical")
	chk_var = []
	filt_btn = tk.Button(tree_frame, text = "Apply filters", command = lambda : apply_filters(df,chk_var,treeview,verscrlbr),activebackground = "grey", font = ("Ubuntu mono" , 15), bg = BG_COLOR,fg = FG_COLOR)
	for frame in [bottomframe_left,bottomframe_right,img_frame,heading,dt]:
		frame.pack_forget()
	back_btn = tk.Button(tree_frame, text = "<", command = lambda :main_screen(tree_frame),activebackground = "grey", font = ("Ubuntu mono" , 15), bg = BG_COLOR,fg = FG_COLOR)
	back_btn.pack(side = "top",anchor = tk.W)
	if chk == 0:
		mf_label = tk.Label(tree_frame, text = "Manufacturer",font = ("Ubuntu mono" , 15),bg = BG_COLOR, fg = FG_COLOR)
		i = 0
		for mfr in list(df["Manufacturer"].unique()):
			var = tk.StringVar()
			chkbtn = tk.Checkbutton(widget_frame, text = mfr,variable = var, onvalue=mfr, offvalue="", command=None,bg = BG_COLOR, fg = FG_COLOR,selectcolor = BG_COLOR)
			chkbtn.grid(row = (i//5)+1,column = i%5, padx = 10, pady = 10)
			i += 1
			chk_var += [var]
		if i > 5:
			mf_label.pack(side = "top",anchor = tk.W, padx = screen_width/5)
		else:
			mf_label.pack(side = "top",anchor = tk.W, padx = screen_width/(1.5*i))
		filt_btn.pack(side = "bottom")
		col = (i % 5) + 7
		i = 0
		for el in list(df.describe()["Price"])[3:]:
			var = tk.IntVar()
			chkbtn = tk.Checkbutton(widget_frame, text = str(el),variable = var, onvalue=1, offvalue=0, command=None,bg = BG_COLOR, fg = FG_COLOR,selectcolor = BG_COLOR)
			chkbtn.grid(row = (i//5)+1,column = col + i%5,padx = 10,pady = 10)
			i += 1
			#chk_var += [var]
	else:
		mfr = tk.Label(tree_frame, text = mfr,font = ("Ubuntu mono" , 25),bg = BG_COLOR,fg = FG_COLOR)
		mfr.pack()
	tree_frame.pack(fill = "both")
	verscrlbr.pack(side = "right",fill = 'y')
	widget_frame.pack(expand = True,fill = "both")
	tv_frame.pack(expand = True,fill = "both")
	write_tree(df,treeview,verscrlbr)
	
def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	if col not in  ["Manufacturer","Model"]:
		l = list(map(lambda x: [float(x[0]),x[1]], l))
	l.sort(reverse=reverse)
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)
	tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))

def about():
	win = tk.Toplevel()
	if theme == "dark":
		bd = "white"
	else:
		bd = "gray15"
	win['bg'] = BG_COLOR
	win.title("About")
	frame = tk.Frame(win,bg = BG_COLOR,highlightbackground = bd, highlightthickness = 5)
	t=tk.Label(frame,text='\nProvides accurate information on EVs \nand custom filters for market research\n and also automated EV purchase suggestions',bg = BG_COLOR,fg = FG_COLOR,font = ("Helvetica" ,12,"bold")).pack()
	credits = tk.Label(frame,text = '\nby\nS Prajwall Narayana\nPrabhav B Kashyap\nKrishnatejaswi S\nVinayak C',font = (None ,10,"bold"),bg = BG_COLOR,fg = FG_COLOR).pack()
	frame.pack()
	center_align(win)

#Initialise tk window
window = tk.Tk()
screen_width = window.winfo_screenwidth()
#COnfigure window background
window.config(bg = BG_COLOR)
#Set title for the window
window.title("Home Page")
#Configure the window geometry
window.geometry("1920x1080")
# "#144be3" "#5214e3"

#Initialise the frames which will be present on the window
heading = tk.Frame(window,bg = BG_COLOR,  width = screen_width)
bottomframe_right = tk.Frame(window)
bottomframe_left = tk.Frame(window,bg = BG_COLOR)
img_frame = tk.Frame(window,bg = BG_COLOR, highlightbackground= FG_COLOR, highlightthickness=5)
#Initialise the labels which will be present on the window
label = tk.Label(bottomframe_left,text = 'Explore by category',padx = 10,bg = EL_BG_COLOR[0],fg = FG_COLOR,pady = 10, highlightbackground = "black",highlightthickness = 1)
label_right = tk.Label(bottomframe_right,text = 'Search by brand',padx = 10,bg = EL_BG_COLOR[1],fg = FG_COLOR,pady = 10, highlightbackground = "black",highlightthickness = 1)
blog = tk.Label(img_frame, text = "If you don't know where to get started, but want to be a part of the rEVolution\n check out our personalized recommender system", padx = 10,bg = "white",fg = FG_COLOR,pady = 10, font = ("Ubuntu Mono",30,'bold'))
dt = tk.Label(window, text = "Compare and choose between EVs",bg = BG_COLOR,fg = FG_COLOR, font = ("Helvetica",20))
#Initialise the buttons which will be present on the window
tw_btn = tk.Button(bottomframe_left,text = "Two wheelers",command = lambda : tree(tw_df), padx = 80, pady = 40, activebackground = "grey", font = ("Ubuntu mono" , 20), fg = "gray15")
fw_btn = tk.Button(bottomframe_left, text = "Four wheelers", command = lambda : tree(fw_df), padx = 320, pady = 40,activebackground = "grey", font = ("Ubuntu mono" , 20), fg = "gray15")
cz_btn = tk.Button(img_frame, text = "Get personalized recommendations", command = None, padx = 320, pady = 40,activebackground = "grey", font = ("Ubuntu mono" , 20), fg = "gray15")
#Logos to be placed on screen
logo = tk.PhotoImage(file="Logos/rEVolt_{}.png".format(theme))
title = tk.Label(heading,image = logo,borderwidth=0)
title.image = logo
logo = tk.PhotoImage(file="Logos/rvce_logo_{}.png".format(theme))
rvlogo = tk.Label(heading,image = logo, borderwidth = 0)
rvlogo.image = logo
#Pack the label
label.pack(fill = 'x',anchor = tk.N)
#Pack the buttons
tw_btn.pack(side = 'bottom',fill = 'x',anchor = tk.S, padx = 40, pady = 20)
fw_btn.pack(side = 'bottom',fill = 'x',anchor = tk.S, padx = 40, pady = 20)
cz_btn.pack(pady = 30)
#Pack the label
label_right.pack(side = 'top',fill = 'x',anchor = tk.E)
blog.pack(pady = 10)
#Pack the logo
rvlogo.pack(side = "left", padx= 10)
#Pack the heading
heading.pack(fill = "x")
#Creata a label for the tagline
#Pack the window title
title.pack(side = "left", padx = screen_width/3.25)
#Pack the label dt
dt.pack()

style = ttk.Style()
style.configure('Treeview', rowheight=40,fieldbackground=BG_COLOR)
style.configure("Treeview.Heading",background = BG_COLOR,foreground = "tan4",padding = 10) 
style.configure("Vertical.TScrollbar", background=BG_COLOR, bordercolor=FG_COLOR, arrowcolor=BG_COLOR)

#Initialise a tk menu
menubar = tk.Menu(window,bg = BG_COLOR,fg = FG_COLOR)
#Initialise file menu in the menubar
file = tk.Menu(menubar,tearoff = 0)
help = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label ='File', menu = file) 
menubar.add_cascade(label ='Help', menu = help) 
def pack_buttons():
	dct = {"ather_logo":"Ather Energy","mg_logo":"MG Motors","tata_logo":"Tata Motors","hyundai_logo":"Hyundai Electric","hero_logo":"Hero Electric","ola_logo":"Ola Electric","tvs_logo":"TVS Motor"}
	for widget in logo_frame.winfo_children():
		widget.destroy()
	i = 0
	for img in img_list:
		photo = tk.PhotoImage(file = "Logos/"+img+"_"+theme+".png")
		var = dct[img]
		btn =  tk.Button(logo_frame, command = lambda var = var: tree(var), image = photo, activebackground = "black")
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
#Execution stops here
window.mainloop()
print('Exit')
