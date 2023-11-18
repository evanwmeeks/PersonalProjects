from tkinter import *
# from wasabi import WasabiUploader

root = Tk()
e = Entry(root, width=50, borderwidth=2)
e.pack()
e.insert(0, "Enter Your Name: ")
def newCommand():
    label = Label(root, text="Hello, " + e.get() + "!", padx=5)
    label.pack()

# # Creating a label widget

# myLabel1 = Label(root, text="Hello, World!")
# myLabel2 = Label(root, text="My Name is Evan")
#
# myLabel1.grid(row=0, column=1, padx=500)
# myLabel2.grid(row=2, column=1, padx=5)

# Creating buttons
myButton = Button(root, text = "Submit", command=newCommand)
myButton.pack()
root.mainloop()