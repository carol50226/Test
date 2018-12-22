import tkinter as tk

win = tk.Tk()
#title
win.title("Carol test")

#size
win.geometry("400x200") #widthxheight
win.minsize(width=400,height=200)
win.maxsize(width=800,height=400)
#win.resizable(0,0) #init 

#function
def say_hi():
    print("HI!!!")

def get_value():
    value = en.get()
    lb.config(text=value)
#icon
#win.iconbitmap("github512.ico")
#background
win.config(bg="black")
#
win.attributes("-alpha",1)
#top most
win.attributes("-topmost", 1) # 1 = True, 0 = False

#label
lb = tk.Label(text="label")
lb.pack()

#entry
en= tk.Entry()
en.pack()

#Button
btn=tk.Button(text="Click me")
btn.config(bg="yellow")
btn.config(width=10,height=2)
btn.config(command=say_hi)
btn.pack()


btn2=tk.Button(text="get value")
btn2.config(bg="red",width=10,height=2)
btn2.config(command=get_value)
btn2.pack()




win.mainloop()
print ('hello world')
