"""
    Date: 17-18/12/2022
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
    Note:
        This is a project to re-create a warehouse.
        Data handling can be simplified using DataFrames (Pandas) or SQLite.
"""
# IMPORTS =====
from tabulate import tabulate  # Pretty tables

# CONSTANTS =====
# Files
INVENTORY = 'inventory.txt'
# Selection menu
MENU = '''
+-- Main menu --+
+-- Select one of the following Options below:
\t0  - Refresh data from file
\t1  - Create new shoe data
\t2  - View details of all shoes available
\t3  - Search specific shoe using shoe code
\t4  - Retrieve total value per item
\t5  - Retrieve shoe with lowest stock (re-stock)
\t6  - Retrieve shoe with highest stock
\t+- e  - Exit
+\tSelect number: '''


# DEFINITION OF CLASS ===================
class Shoe:
    """
    Shoe class to include the definition of a shoe.
    Variables:
        country = Country of item.
        code = Code of item.
        product = Product of item.
        cost = Cost of item.
        quantity = Total quantity of the item in the warehouse.
    """

    def __init__(self, country, code, product, cost, quantity):
        # strip used to prevent any unwanted spaces.
        self.country = country.strip()
        self.code = code.strip()
        self.product = product.strip()
        # Blocks to create cost and quantity out of the parameters.
        # Change the values into float.
        try:
            # try-except block to prevent issues whilst using cast into float.
            self.cost = float(cost)

        except ValueError:
            print(f'Product {self.code} has a wrong cost ({cost}).')
            print('Value assigned to 0.')
            self.cost = 0

        # Quantity data gathering
        try:
            # try-except block to prevent issues whilst using cast into float.
            self.quantity = float(quantity)
            # assert to prevent unrealistic quantity in shoe.
            assert self.quantity > 0, 'Quantity of item must be over 0.'

        except ValueError:
            print(f'Product {self.code} has a wrong quantity ({quantity}).')
            print('Value assigned to 0.')
            self.quantity = 0

    def get_cost(self) -> float:
        """
        Retrieve the cost of the item.
        :return: cost of item.
        """
        return self.cost

    def get_quantity(self) -> float:
        """
        Retrieve the quantity of the item.
        :return: cost of item.
        """
        return self.quantity

    def get_value(self):
        """
        Calculate and returns the value of the item:
        value = cost * quantity
        :return: Value of the item.
        """
        return self.cost * self.quantity

    def __str__(self) -> str:
        """
        Prepare the representation of shoes based on properties.
        Country, Code, Product, Cost, Quantity
        :return: String.
        """
        return f'{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}'


# Functions of warehouse ==============
def update_inventory(mode: str = 'full', shoe_to_include: str = 'ERR,ERR,ERR,ERR,ERR') -> bool:
    """
    Management of inventory file (add new data or update current).
    :param mode: Tells the function what to do; full update all file, single add new item.
    :param shoe_to_include: Single shoe to add (select mode == 'single').
    :return: bool. True if all went fine. False otherwise.
    """
    # Selection of mode.
    if mode == 'full':
        # Update whole file.
        updated_data_inventory = f'{", ".join(header)}'  # Include the header in the data.
        # Loop over all items and fill the data for input in the file.
        for shoe in shoe_list:
            updated_data_inventory += f'\n{str(shoe)}'

        try:
            # try-except to catch any possible issue.
            # Note: Write will create the new file if it does not exist.
            with open(INVENTORY, 'w') as file:
                file.write(updated_data_inventory)

        except OSError:
            # NOTE: This is not recommended, normally this should be scoped for possible issues.
            return False

    elif mode == 'single':
        # Append one new item to file.
        if shoe_to_include == 'ERR,ERR,ERR,ERR,ERR':
            # Default value, therefore, do not do anything.
            return False

        else:
            try:
                # try-except to catch any possible issue.
                # Note: Append will create the new file if it does not exist.
                with open(INVENTORY, 'a') as file:
                    file.write(f'\n{shoe_to_include}')

            except OSError:
                # NOTE: This is not recommended, normally this should be scoped for possible issues.
                return False

    else:
        # Not probable but included this option.
        return False
    # Default return is True. Only when something is wrong returns False.
    return True


def read_shoes_data() -> None:
    """
    Load data into system from inventory file.
    :return: None
    """
    print('\n+-- Loading warehouse stock file -----------+')
    # Gather data from inventory.
    global header, shoe_list  # Variables as global so the outer scope it is modified.
    # Clean global variables
    shoe_list = []
    header = ''
    try:
        # try-expect block to prevent issues whilst loading data.
        # Read inventory data with a loop per each line:
        # First row is stored as it contains the header: Country,Code,Product,Cost,Quantity.
        counter = 0  # Counter is used for first iteration only (to gather the header).
        for line in open(INVENTORY, 'r'):
            # Delete the \n at the end of the line and split the line.
            raw_data = line. \
                replace('\n', ''). \
                split(',')
            if len(raw_data) < 2:
                # Empty row, possible issue in file.
                print('+- #  Check file for possible empty rows.')

            else:
                # Gather the data in the list of shoes and heading in heading variable
                if counter == 0:
                    # Get rid of empty spaces in header.
                    header = [x.strip() for x in raw_data]
                    counter = 1

                else:
                    # Create an instance of Shoe object:
                    shoe_item = Shoe(
                        country=raw_data[0],
                        code=raw_data[1],
                        product=raw_data[2],
                        cost=raw_data[3],
                        quantity=raw_data[4]
                                     )
                    # Get shoes data into general list
                    shoe_list.append(shoe_item)

    except FileNotFoundError:
        print(f'{INVENTORY} file not found.')

    else:
        print('+-- Warehouse stock file loaded ------------+\n')


def capture_shoes() -> None:
    """
    Create a new item (shoe) and append it to the inventory.
    :return : None.
    """
    print('\n+-- Fill the form to add a new shoe.')
    # Create an instance of Shoe object.
    # Strip possible unwanted spaces.
    shoe_item = Shoe(
        country=input('+- Country: ').strip(),
        code=input('+- Shoe code [example SKU12345]: ').strip(),
        product=input('+- Name of product: ').strip(),
        cost=input('+- Base cost: ').strip(),
        quantity=input('+- Quantity of shoes: ').strip()
    )
    # Check if the user wants the item included.
    print('\n+-- Confirm that you want to add the following product (y/n):')
    one_item_list = [(str(shoe_item).split(','))]
    print(tabulate(one_item_list, headers=header))
    if input('+- Confirm > ').lower() == 'y':
        # Include new shoe into list.
        shoe_list.append(shoe_item)
        # Update inventory file.
        status_update = update_inventory(mode='single', shoe_to_include=str(shoe_item))
        if status_update:
            print('+-- Included in inventory.\n')
        else:
            print('+-- Issue whilst saving data into file. Process aborted.\n')
            # Delete last item added (new shoe).
            shoe_list.pop(-1)

    else:
        print('+-- Process aborted.\n')


def view_all(raw_list, header_of_list) -> None:
    """
    Print in screen a table with the data gathered.
    Note this function can handle a single item or multiple items.
    :param raw_list: List of items to print.
    :param header_of_list: Header for the list.
    :return: None
    """
    items_data = []
    # Loop over data. Note str item will retrieve the __str__ which is a str.
    # split will create a list out of the str retrieved.
    # Check if a single parameter is in raw_list, if yes, convert to list.
    if type(raw_list) != list:
        raw_list = [raw_list]

    for item in raw_list:
        items_data.append(str(item).split(','))
    # Using tabulate to pretty print.
    print('\n\n+-------------- Reporting data ---------------------------+\n')
    print(tabulate(items_data, headers=header_of_list))
    print('+------------------------------------------------------------+\n')


def re_stock() -> None:
    """
    Find the item with lower quantity; if multiple items found with quantity equals 0 user will be warned.
    Ask for re-stock; if confirmed, it will be updated in the master file.
    :return: None.
    """
    print('\n+-- Searching for shoe with lowest quantity.')
    # Loop over the shoes, stop when the one it is found (minimum quantity it is 0).
    # If more than one item has quantity equal to 0, send a message to user but retrieve only the last one found.
    items_found = 0
    lowest = 10_000  # Big number so all are lower.
    for item in shoe_list:
        if item.get_quantity() <= lowest:
            lowest = item.get_quantity()  # Update lowest value.
            lowest_quantity_item = item
            # Only add 1 to the items found if there are multiple items with lowest == 0 or first iteration.
            items_found += 1 if lowest == 10_000 or lowest == 0 else 0

    else:
        print('+- Search finished. Details of shoe below.')

    if items_found > 1:
        print('+- Note: Multiple items found with quantity equal 0. Only one retrieved.')

    one_item_list = [(str(lowest_quantity_item).split(','))]
    print(tabulate(one_item_list, headers=header))
    if input('+- Would you like to re-stock item? (y/n) -> ').lower() == 'y':
        try:
            # try-except block to prevent issues whilst using cast.
            re_stock_quantity = int(input('+- Input quantity of items to order re-stock: '))
            # assert prevents unrealistic values.
            assert re_stock_quantity > 0

        except ValueError:
            print('+- Please only input a number when required.')
            print('+-- Process aborted.\n')

        except AssertionError:
            print('+- Please input a quantity over 0.')
            print('+-- Process aborted.\n')

        else:
            # If all is correct, then re-stock the product adding the new stock to the actual one.
            lowest_quantity_item.quantity += re_stock_quantity
            # Update the item in the list with the new stock.
            shoe_list[shoe_list.index(lowest_quantity_item)] = lowest_quantity_item
            # Update inventory file.
            status_update = update_inventory(mode='full')
            if status_update:
                print('+-- Update completed.\n')
            else:
                print('+-- Issue whilst saving data into file. Process aborted.\n')
    else:
        print('+-- Process ended.\n')


def search_shoe(code_of_shoe):
    """
        Search for the shoe based on the argument/code.
        :param code_of_shoe: Code of the shoe to search.
        :return: Shoe if found, None if not.
        """
    # Loop over data.
    # Note strip is used to prevent any unwanted spaces in the item.
    for item in shoe_list:
        if item.code.strip() == code_of_shoe:
            # Found. return will directly end the function (and loop).
            return item

    else:
        # Not found.
        print(f'+- Shoe with code {code_of_shoe} not found.')

    return 'not_found'


def value_per_item() -> None:
    """
    Calculate the total value of each batch and print the list with all items.
    :return: None.
    """
    print('\n+-- Gathering data and retrieving information.')
    new_header = header[:]
    new_header.append('Total Value')
    value_of_items = []
    for shoe in shoe_list:
        # Get the value from the class: value = quantity * cost.
        # Join in f-string for latter.
        total_value = f'{str(shoe)}, {shoe.get_value()}'

        value_of_items.append(total_value.split(','))

    else:
        print('+- Data gathered. Details of shoes below.')
    # Print data.
    print(tabulate(value_of_items, headers=new_header))
    print('+------------------------------------------------------------+\n')


def highest_qty() -> None:
    """
        Find the item with highest quantity.
        If multiple items share the highest quantity, print all.
        :return: None.
    """
    print('\n+-- Searching for shoe with highest quantity (stock) available.')
    highest = -1  # Low number so all are higher.
    for item in shoe_list:
        quantity_of_current_item = item.get_quantity()
        if quantity_of_current_item > highest:
            # Note, if multiple items have equal quantity, only retrieve the first one found.
            highest = quantity_of_current_item  # Update highest value.
            highest_quantity_item = item

    else:
        print('+- Search finished. Details of shoe for sale below.')

    one_item_list = [(str(highest_quantity_item).split(','))]
    print(tabulate(one_item_list, headers=header))
    print('+------------------------------------------------------------+\n')


# MAIN =======
if __name__ == '__main__':
    # The list will be used to store a list of objects of shoes.
    shoe_list = []
    header = ''  # Holds the header of inventory file.
    print('\n+----------- Warehouse -----------+')
    # First load the program with the inventory data:
    read_shoes_data()

    while True:
        # Print a menu for the user each iteration.
        selection = input(MENU).lower()

        if selection == '0':  # Refresh data from file
            print('+-- NOTE: Data not saved will be lost.')
            # Confirmation of refresh.
            if input('+- Confirm that you want to refresh data (y/n) -> ').lower() == 'y':
                read_shoes_data()
            else:
                print('+- Process aborted. Refresh cancelled.\n')

        elif selection == '1':  # Create new shoe data
            capture_shoes()

        elif selection == '2':  # View details of all shoes available
            # Print in screen the shoe_list.
            # header is needed to give context.
            view_all(shoe_list, header)

        elif selection == '3':  # Search specific shoe using shoe code
            shoe_wanted = search_shoe(input('+- Enter code of shoe to find [example SKU12345]: '))
            if shoe_wanted != 'not_found':
                # Using tabulate to pretty print.
                print('+-- Shoe found:')
                print(tabulate([str(shoe_wanted).split(',')], headers=header))
                print('+------------------------------------------------------------+\n')

        elif selection == '4':  # Retrieve value per item
            value_per_item()

        elif selection == '5':  # Retrieve shoe with lowest stock (re-stock)
            re_stock()

        elif selection == '6':  # Retrieve shoe with highest quantity
            highest_qty()

        elif selection == 'e':  # exit
            # Exit application
            print('\n+----------- Session Ended -----------+')
            exit()

        else:
            print("You have made a wrong choice. Please try again.")
