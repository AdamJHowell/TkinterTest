import os
import tkinter
from os.path import join, getsize
from pathlib import Path
from tkinter import END
from typing import List


def verify() -> bool:
  """
  Validates the user settings and searches the specified directory.
  :return: True if the search is successful, False otherwise.
  :rtype: bool
  """
  # Retrieve the user settings.
  directory = directory_value.get()
  extensions = [word for word in extension_value.get().split()]

  # Verify that the directory exists.
  if not os.path.isdir( directory ):
    status_label_text.set( "Invalid Directory!" )
    print( f"'{directory}' is an invalid Directory!" )
    return False

  # Update the status before searching.
  print( f"Search beginning in this directory: {directory}" )
  print( f"Looking for the following extensions: {extensions}" )
  print( "Searching..." )
  status_label_text.set( f"Searching in {directory}..." )

  # Perform the actual search.
  files = find_all_files( directory )

  # Show the results.
  print( f"Search complete, found {len( files )} files." )
  status_label_text.set( f"Search complete, found {len( files )} files." )
  file_match_list = []
  for filename in files:
    file_extension = filename[filename.rfind( '.' ):]
    if file_extension in extensions:
      file_match_list.append( filename )
  print( f"Number of files with matching extensions: {len( file_match_list )}" )
  for file in file_match_list:
    text_box.insert( tkinter.END, file )
    text_box.insert( tkinter.END, "\n" )
  return True


def clear_text() -> None:
  """
  Clears the text box.
  """
  text_box.delete( "1.0", END )


def find_all_files( root_dir: str ) -> List[str]:
  """
  List all files in the specified directory.
  :param root_dir: The directory to start searching from.
  :return: A list of all files in the specified directory.
  :rtype: List[str]
  """
  all_files: List[str] = []
  dirpath: str
  dirnames: List[str]
  filenames: List[str]
  for dirpath, dirnames, filenames in os.walk( root_dir ):
    print( f"Directory '{dirpath}' consumes {format( sum( getsize( join( dirpath, name ) ) for name in filenames ), ',' )} bytes on disk (not including subdirectories)." )

    # Convert dirpath to Path object.
    pathlib_dirpath = Path( dirpath )
    all_files.extend( filenames )

    # Convert dirnames and filenames to Path containers.
    pathlib_dirnames: List[Path]
    pathlib_dirnames = [pathlib_dirpath / dirname for dirname in dirnames]
    pathlib_filenames: List[Path]
    pathlib_filenames = [pathlib_dirpath / filename for filename in filenames]

    # Process the Path objects.
    print( f"Directory: {dirpath}" )
    if len( pathlib_dirnames ) > 0:
      subdir_suffix = "Subdirectory"
      if len( pathlib_dirnames ) != 1:
        subdir_suffix = "Subdirectories"
      print( f"  {len( pathlib_dirnames )} {subdir_suffix}: {pathlib_dirnames}" )
      for i, dirname in enumerate( pathlib_dirnames, start = 1 ):
        # dirname is a pathlib.Path object.
        print( f"    Directory {i} name: {dirname}" )
    if len( pathlib_filenames ) > 0:
      file_text = "file"
      if len( pathlib_filenames ) != 1:
        file_text = "files"
      print( f"  {len( pathlib_filenames )} {file_text}: {pathlib_filenames}" )
      for i, filename in enumerate( pathlib_filenames, start = 1 ):
        # filename is a string.
        print( f"    File {i} name: {filename}" )
    print()
  return all_files


if __name__ == "__main__":
  root = tkinter.Tk()
  root.title( "Find files" )
  root.minsize( 200, 200 )  # width, height
  root.geometry( "408x305+50+50" )
  directory_value = tkinter.StringVar( root )
  extension_value = tkinter.StringVar( root )
  status_label_text = tkinter.StringVar( root )
  status_label_text.set( "Idle" )

  # First grid row.
  tkinter.Label( root, text = "Directory" ).grid( row = 0 )
  directory_entry = tkinter.Entry( root, bd = 3, textvariable = directory_value )
  directory_entry.grid( row = 0, column = 1, columnspan = 2, sticky = "nsew" )
  directory_entry.insert( END, "C:\\Media\\Music" )

  # Second grid row.
  tkinter.Label( root, text = "Extensions" ).grid( row = 1 )
  extension_entry = tkinter.Entry( root, bd = 3, textvariable = extension_value )
  extension_entry.grid( row = 1, column = 1, columnspan = 2, sticky = "nsew" )
  extension_entry.insert( END, ".flac .m4a .mp3" )

  # Third grid row.
  text_box = tkinter.Text( root, height = 14, width = 50 )
  text_box.grid( row = 2, columnspan = 3, sticky = "nsew" )
  root.grid_rowconfigure( 2, weight = 1 )

  # Fourth grid row.
  tkinter.Label( root, text = "Status: " ).grid( row = 6, column = 0, sticky = "nsew" )
  tkinter.Label( root, textvariable = status_label_text ).grid( row = 6, column = 1, columnspan = 2, sticky = "nsew" )

  # Last grid row.
  tkinter.Button( root, text = "Search", command = verify ).grid( row = 7, column = 0, sticky = "nsew" )
  tkinter.Button( root, text = "Clear", command = clear_text ).grid( row = 7, column = 1, sticky = "nsew" )
  tkinter.Button( root, text = "Exit", command = root.quit ).grid( row = 7, column = 2, sticky = "nsew" )

  # Configure column resizing behavior
  root.columnconfigure( 0, weight = 1 )
  root.columnconfigure( 1, weight = 1 )
  root.columnconfigure( 2, weight = 1 )

  # Create a Scrollbar
  scrollbar = tkinter.Scrollbar( root, command = text_box.yview )
  scrollbar.grid( row = 2, column = 3, sticky = "ns" )  # Grid positioning and anchoring for the scrollbar.

  # Configure the Text widget to use the scrollbar
  text_box.config( yscrollcommand = scrollbar.set )

  root.mainloop()
