import tkinter
from tkinter import END


def verify():
  print( "\nResults:" )
  # Print to the console.
  print( directory_value.get() )
  # Print to the Text() object.
  text_box.insert( tkinter.END, directory_value.get() )
  text_box.insert( tkinter.END, "\n" )
  print( extension_value.get() )


root = tkinter.Tk()
root.title( "Find files" )
root.minsize( 200, 200 )  # width, height
root.geometry( "408x305+50+50" )
directory_value = tkinter.StringVar( root )
extension_value = tkinter.StringVar( root )

# First grid row.
tkinter.Label( root, text = "Directory" ).grid( row = 0 )
directory_entry = tkinter.Entry( root, bd = 3, textvariable = directory_value )
directory_entry.grid( row = 0, column = 1, columnspan = 2 )
directory_entry.insert( END, "C:\\Media\\Music\\Rush\\" )

# Second grid row.
tkinter.Label( root, text = "Extensions" ).grid( row = 1 )
extension_entry = tkinter.Entry( root, bd = 3, textvariable = extension_value )
extension_entry.grid( row = 1, column = 1, columnspan = 2 )
extension_entry.insert( END, ".flac" )

# Third grid row.
text_box = tkinter.Text( root, height = 14, width = 50 )
text_box.grid( row = 2, columnspan = 3 )

# Last grid row.
tkinter.Button( root, text = "Search", command = verify ).grid( row = 6, column = 0 )
tkinter.Button( root, text = "Exit", command = root.quit ).grid( row = 6, column = 1 )

root.mainloop()
