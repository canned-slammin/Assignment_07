#---------------------------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# SBurner, 2021-Nov-20, Made appropriate edits per Assignment 06
# SBurner, 2021-Nov-28, Added exception handling and binary data
#---------------------------------------------------------------#

# -- MODULES -- #
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:

    def add_cd(dicRow,table):
        """Function to append new cd into program memory.
        Reads user input for ID, Title, and Artist, and adds it to a 
        2D table (list of dictionaries) as one row dictionary in the table.
        
        Args:
            dicRow (dictionary): a list of items to add to the table
            table (2D list): a list of dictionaries that holes the CD inventory
        Returns:
            None.
        """

        # Add item to the table
        if dicRow != None:
            table.append(dicRow)  
        
    def del_cd(table):
        """
        Function to delete a dict row from the inventory table

        Parameters
        ----------
        table : list of dicts
            2D data structure (list of dicts) that holds the data during runtime

        Returns
        -------
        None.

        """

        try:
            # ask user which ID to remove
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # search thru table and delete CD
            intRowNr = -1
            blnCDRemoved = False
            for row in table:
                intRowNr += 1
                if row['ID'] == intIDDel:
                    del table[intRowNr]
                    blnCDRemoved = True
                    break
                if blnCDRemoved:
                    print('The CD was removed')
                else:
                    print('Could not find this CD!')
        except ValueError:
            input('Invalid input, ID must be a number. Press [ENTER] to continue')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        """
    
        try:
            with open(file_name,'rb') as objFile:
                table = pickle.load(objFile)
        except FileNotFoundError:
            input('Existing inventory not found, press [ENTER] to proceed')
            table = []
            
        return table

    @staticmethod
    def write_file(file_name, table):
        """
        Function to append or overwrite text file of CD inventory.

        Parameters
        ----------
        file_name : string
            name of text file to write data to.
        table : 2D list of dictionaries
            2D data structure with rows of dictonaries containing CD inventory data.

        Returns
        -------
        None.
        """
    
        with open(file_name, 'wb') as objFile:
            pickle.dump(table,objFile)
            print("file saved!")

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def collect_data():
        """
        Collect user input and convert to dictionary

        Returns
        -------
        dicRow : dictionary
            User input values tagged to ID, Title, and Artist keys.

        """
        
        # Ask user for new ID, CD Title and Artist
        strID = input('Enter ID: ').strip()
        try:
            intID = int(strID)    
            strTitle = input('What is the CD\'s title? ').strip()
            stArtist = input('What is the Artist\'s name? ').strip()
            dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
            return dicRow
        except ValueError:
            input('Invalid input, ID must be a number')
        
# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        DataProcessor.add_cd(IO.collect_data(),lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.2 run delete function
        DataProcessor.del_cd(lstTbl)
        # display updated Inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName,lstTbl)
            input('Press [ENTER] to return to the menu.')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




