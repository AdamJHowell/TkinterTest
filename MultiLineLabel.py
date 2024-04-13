import tkinter


def verify():
  # Print to the console.
  print( user_input.get() )
  # Print to the Text() object.
  text_box.insert( tkinter.END, user_input.get() )


root = tkinter.Tk()
root.title( "Grid Test" )
root.minsize( 200, 200 )  # width, height
root.geometry( "408x305+50+50" )
user_input = tkinter.StringVar( root )

# First grid row.
tkinter.Label( root, text = "First name" ).grid( row = 0 )
entry_first_name = tkinter.Entry( root, bd = 3, textvariable = user_input )
entry_first_name.grid( row = 0, column = 1, columnspan = 2 )

# Second grid row.
tkinter.Label( root, text = "Last name" ).grid( row = 1 )
entry_last_name = tkinter.Entry( root, bd = 3 )
entry_last_name.grid( row = 1, column = 1, columnspan = 2 )

# Third grid row.
text_box = tkinter.Text( root, height = 14, width = 50 )
text_box.grid( row = 2, columnspan = 3 )

# Last grid row.
tkinter.Button( root, text = "Verify", command = verify ).grid( row = 6, column = 0 )
tkinter.Button( root, text = "Exit", command = root.quit ).grid( row = 6, column = 1 )

root.mainloop()
