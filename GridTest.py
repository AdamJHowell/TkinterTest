import tkinter


def verify():
  print( user_input.get() )


root = tkinter.Tk()
root.title( "Grid Test" )
root.minsize( 200, 200 )  # width, height
root.geometry( "300x300+50+50" )
user_input = tkinter.StringVar( root )

tkinter.Label( root, text = "First" ).grid( row = 0 )
tkinter.Label( root, text = "Second" ).grid( row = 1 )

e1 = tkinter.Entry( root, bd = 3, textvariable = user_input )
e2 = tkinter.Entry( root, bd = 3 )

e1.grid( row = 0, column = 1 )
e2.grid( row = 1, column = 1 )

tkinter.Button( root, text = "Verify", command = verify ).grid( row = 6, column = 0 )
tkinter.Button( root, text = "Exit", command = root.quit ).grid( row = 6, column = 1 )

root.mainloop()
