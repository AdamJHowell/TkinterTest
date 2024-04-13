import tkinter

root = tkinter.Tk()

tkinter.Label( root, text = "Input:" ).grid( row = 0, column = 0 )
tkinter.Entry( root, width = 100 ).grid( row = 0, column = 1 )

frame = tkinter.Frame()
frame.grid( row = 1, column = 0, columnspan = 2, sticky = 'w' )
tkinter.Button( frame, text = 'Confirm' ).grid( row = 0, column = 0, sticky = 'w' )
tkinter.Button( frame, text = 'C' ).grid( row = 0, column = 1, sticky = 'w' )
tkinter.Button( frame, text = 'Q', command = frame.quit ).grid( row = 0, column = 2, sticky = 'w' )

root.mainloop()
