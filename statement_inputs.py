#import wx
from Tkinter import *
import tkFileDialog

'''''''''
def get_RadianceFolder():

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    #filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    directory = askdirectory()

    def get_filepaths(directory):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

        return file_paths  # Self-explanatory.

    # Run the above function and store its results in a variable.
    full_file_paths = get_filepaths(directory)
    Radiance_Files = [s for s in full_file_paths if s.endswith('_rd')]
    Header_Files = [s for s in full_file_paths if s.endswith('_rd.hdr')]


    return Radiance_Files, Header_Files
'''''

'''''''''
def get_RawFile():
    def get_path(wildcard):
        app = wx.App(None)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            path = None
        dialog.Destroy()
        return path

    wildcard = "Python source (*.py)|*.py|" "All files (*.*)|*.*"

    Raw_File = get_path(wildcard)
    Raw_File = str(Raw_File)
    Header_File = Raw_File + '.hdr'

    return Raw_File, Header_File


def dialog_box(message_for_the_variable):
    def ask(parent=None, message=''):
        dlg = wx.TextEntryDialog(parent, message)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result

    # Initialize wx App
    app = wx.App()
    app.MainLoop()

    # Call Dialog
    variable_output = ask(message = message_for_the_variable)
    variable_output = str(variable_output)
    return variable_output
'''''''''

def get_RawFile():
    
    Tk().update()
    Tk().withdraw
    Raw_File = tkFileDialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    Tk().destroy()
    Header_File = Raw_File + '.hdr'
    
    return Raw_File, Header_File

def dialog_box(message_for_the_variable):
    
    master = Tk()
    Label(master, text=message_for_the_variable).grid(row=0)
    
    e1 = Entry(master)
    e1.grid(row=0, column=1)
    Button(master, text='Enter Varianble', command=master.quit).grid(row=0, column=4, sticky=W, pady=5)
    mainloop()
    variable_output = e1.get()
    
    return variable_output