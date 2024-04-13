import fnmatch
import os
import tkinter
from tkinter import END
from typing import List


def verify():
  print( "\nResults:" )
  # Retrieve the values.
  directory = directory_value.get()
  extensions = [word for word in extension_value.get().split()]
  # Print to the console.
  print( directory )
  print( extensions )
  # Print to the Text() object.
  text_box.insert( tkinter.END, directory )
  text_box.insert( tkinter.END, "\n" )
  print( "Searching..." )
  files = find_files_by_extension( directory, extensions )
  print( "Search complete." )
  print( f"Number of files: {len( files )}" )
  print( files )
  for file in files:
    text_box.insert( tkinter.END, file )
    text_box.insert( tkinter.END, "\n" )


def find_files_by_extension( directory: str, extensions: List[str] ) -> List[str]:
  """
  List all files in the specified directory and its subdirectories that have the given extensions.
  @param directory: The directory to search for audio files.
  @param extensions: The extensions to search for.
  @return: A list of audio files.
  """
  print( f"Searching {directory} for extensions {extensions}..." )
  audio_files = []
  for root_dir, dirs, files in os.walk( directory ):
    for extension in extensions:
      for filename in fnmatch.filter( files, f'*.{extension}' ):
        audio_files.append( os.path.join( root_dir, filename ) )
        print( filename )
  return audio_files


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
directory_entry.insert( END, "C:\\Media\\Music\\Rush" )

# Second grid row.
tkinter.Label( root, text = "Extensions" ).grid( row = 1 )
extension_entry = tkinter.Entry( root, bd = 3, textvariable = extension_value )
extension_entry.grid( row = 1, column = 1, columnspan = 2 )
extension_entry.insert( END, ".flac .m4a .txt .mp3" )

# Third grid row.
text_box = tkinter.Text( root, height = 14, width = 50 )
text_box.grid( row = 2, columnspan = 3 )

# Last grid row.
tkinter.Button( root, text = "Search", command = verify ).grid( row = 6, column = 0 )
tkinter.Button( root, text = "Exit", command = root.quit ).grid( row = 6, column = 1 )

root.mainloop()
