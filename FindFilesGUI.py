import os
import threading
import tkinter
from os.path import join, getsize
from pathlib import Path
from tkinter import END, filedialog
from typing import List


def verify() -> None:
  """
  Validates the user settings and searches the specified directory.
  """
  # Retrieve the user settings.
  directory = directory_value.get()
  extensions = list( extension_value.get().split() )

  # Verify that the directory exists.
  if not os.path.isdir( directory ):
    status_label_text.set( "Invalid Directory!" )
    print( f"'{directory}' is an invalid Directory!" )
    return

  # Update the status before searching.
  print( f"Search beginning in this directory: {directory}" )
  print( f"Looking for the following extensions: {extensions}" )
  print( "Searching..." )
  status_label_text.set( f"Searching in {directory}..." )
  # Start the search in a new thread
  threading.Thread(
    target = threaded_search,
    args = (directory, extensions),
    daemon = True
  ).start()


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
  """
  dirpath: str
  dir_names: List[str]
  filenames: List[str]
  all_files: List[str] = []
  try:
    for dirpath, dir_names, filenames in os.walk( root_dir ):
      print( f"Directory '{dirpath}' consumes {format( sum( getsize( join( dirpath, name ) ) for name in filenames ), ',' )} bytes on disk (not including subdirectories)." )

      # Convert dirpath to Path object.
      pathlib_dirpath = Path( dirpath )
      all_files.extend( filenames )

      # Print the directory and file names.
      print_dirs_and_files( dirpath, dir_names, filenames, pathlib_dirpath )
  except Exception as exception:
    print( f"An error occurred while searching for files: {exception}" )
    status_label_text.set( "Error during search!" )
  return all_files


def print_dirs_and_files( dirpath: str, dir_names: list[str], filenames: list[str], pathlib_dirpath: Path ) -> None:
  """
  Print the directory and file names in a formatted way.
  :param dirpath: The path of the current directory returned by os.walk().
  :param dir_names: List of directory names returned by os.walk().
  :param filenames: List of file names returned by os.walk().
  :param pathlib_dirpath: The Path object of the current directory.
  """
  # Convert dir_names and filenames to Path containers.
  pathlib_dir_names: List[Path]
  pathlib_dir_names = [pathlib_dirpath / dirname for dirname in dir_names]
  pathlib_filenames: List[Path]
  pathlib_filenames = [pathlib_dirpath / filename for filename in filenames]
  # Process the Path objects.
  print( f"Directory: {dirpath}" )
  if len( pathlib_dir_names ) > 0:
    subdir_suffix = "Subdirectory"
    if len( pathlib_dir_names ) != 1:
      subdir_suffix = "Subdirectories"
    print( f"  {len( pathlib_dir_names )} {subdir_suffix}: {pathlib_dir_names}" )
    for i, dirname in enumerate( pathlib_dir_names, start = 1 ):
      # dirname is a pathlib.Path object.
      print( f"    Directory {i} name: {dirname}" )
  if len( pathlib_filenames ) > 0:
    file_text = "file"
    if len( pathlib_filenames ) != 1:
      file_text = "files"
    print( f"  {len( pathlib_filenames )} {file_text}: {pathlib_filenames}" )
    for i, filename in enumerate( pathlib_filenames, start = 1 ):
      print( f"    File {i} name: {filename}" )
  print()


def directory_check_callback( entry, *_args ) -> None:
  """
  This callback function checks if the directory specified in the entry widget exists.
  If the directory does not exist, it changes the background color of the entry widget to red.
  """
  directory = directory_value.get()
  if not os.path.isdir( directory ):
    entry.configure( { "background": "red" } )
  else:
    entry.configure( { "background": "white" } )


def threaded_search( directory, extensions ) -> None:
  """
  This function is run in a separate thread to perform the file search.
  It finds all files in the specified directory with the given extensions.
  :param directory: The directory to search in.
  :param extensions: A list of file extensions to search for.
  """
  # Perform the actual search in a background thread.
  files = find_all_files( directory )
  file_match_list = []
  extensions = [ext.lower() for ext in extensions]
  for filename in files:
    extension = os.path.splitext( filename )[1].lower()
    if extension in extensions:
      file_match_list.append( filename )
  # Use after() to schedule UI update in the main thread.
  root.after( 0, show_search_results, file_match_list )


def show_search_results( file_match_list ) -> None:
  """
  This function updates the text box with the search results.
  :param file_match_list: A list of files that match the search criteria.
  """
  text_box.delete( "1.0", END )
  for file in file_match_list:
    text_box.insert( tkinter.END, file + "\n" )
  status_label_text.set( f"Search complete, found {len( file_match_list )} files." )


def browse_directory( entry_widget, fallback_directory: str ) -> None:
  """
  Opens a file dialog to select a directory and updates the entry widget with the selected directory.
  :param entry_widget: The Entry widget to update with the selected directory.
  :param fallback_directory: The directory to use as the initial directory in the file dialog.
  """
  current_dir = entry_widget.get()
  selected_dir = filedialog.askdirectory(
    title = "Select a directory",
    initialdir = current_dir if current_dir else fallback_directory )
  if selected_dir:
    entry_widget.delete( 0, END )
    entry_widget.insert( 0, selected_dir )


if __name__ == "__main__":
  default_directory = "C:\\Media\\Music"
  root = tkinter.Tk()
  root.title( "Find files" )
  root.geometry( "408x305+50+50" )
  root.minsize( 200, 200 )  # width, height
  directory_value = tkinter.StringVar( root )
  directory_value.trace( "w", lambda *args: directory_check_callback( directory_entry, *args ) )
  extension_value = tkinter.StringVar( root )

  # First grid row.
  tkinter.Label( root, text = "Directory" ).grid( row = 0, sticky = "w" )
  directory_entry = tkinter.Entry( root, bd = 3, textvariable = directory_value )
  directory_entry.grid( row = 0, column = 1, columnspan = 2, sticky = "nsew" )
  directory_entry.insert( END, default_directory )

  # Create a button to browse for the directory.
  tkinter.Button(
    root,
    text = "Browse...",
    command = lambda: browse_directory( directory_entry, default_directory )
  ).grid( row = 0, column = 3, sticky = "ew" )

  # Second grid row.
  tkinter.Label( root, text = "Extensions" ).grid( row = 1, sticky = "w" )
  extension_entry = tkinter.Entry( root, bd = 3, textvariable = extension_value )
  extension_entry.grid( row = 1, column = 1, columnspan = 2, sticky = "nsew" )
  extension_entry.insert( END, ".flac .m4a .mp3" )

  # Third grid row.
  text_box = tkinter.Text( root, height = 14, width = 50 )
  text_box.grid( row = 2, columnspan = 3, sticky = "nsew" )
  root.grid_rowconfigure( 2, weight = 1 )

  # Fourth grid row.
  status_label_text = tkinter.StringVar( root )
  status_label_text.set( "Idle" )
  tkinter.Label( root, text = "Status: " ).grid( row = 6, column = 0, sticky = "nsew" )
  tkinter.Label( root, textvariable = status_label_text ).grid( row = 6, column = 1, columnspan = 2, sticky = "w" )

  # Last grid row.
  tkinter.Button( root, text = "Search", command = verify ).grid( row = 7, column = 0, sticky = "ew" )
  tkinter.Button( root, text = "Clear", command = clear_text ).grid( row = 7, column = 1, sticky = "ew" )
  tkinter.Button( root, text = "Exit", command = root.quit ).grid( row = 7, column = 2, sticky = "e" )

  # Configure column resizing behavior
  root.columnconfigure( 0, weight = 0 )
  root.columnconfigure( 1, weight = 0 )
  root.columnconfigure( 2, weight = 1 )
  root.columnconfigure( 3, weight = 0 )

  # Create a Scrollbar
  scrollbar = tkinter.Scrollbar( root, command = text_box.yview )
  scrollbar.grid( row = 2, column = 3, sticky = "ns" )  # Grid positioning and anchoring for the scrollbar.

  # Configure the Text widget to use the scrollbar
  text_box.config( yscrollcommand = scrollbar.set )

  root.mainloop()
