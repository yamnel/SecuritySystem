"""
        Security System v0.5

This program grants or denies access to a User depending on the correctness
of their passwords.

The User has to input 2 forms of valid identification and his/her correct ID #.

by by Yamnel Serra and Steven Isbel
Class CEN 4930 ST: Cyberphysical Systems
Instructor - Dr. Janusz Zalewski
"""
import sys

import os
from PyQt5.Qt import *

from User import User

"""This is the Main & GUI Class"""


class SystemGUI(QWidget):
    def __init__(self):
        super().__init__()

        """ This block of code is a mock Database for example purposes"""
        # ------------ from Database -------------------------------
        self.usr1 = User(user_id='8101', pin='0001', card='123')  # creating a test user
        self.usr_credentials = [('pin', 'card')]  # what the user uses to enter the room
        self.room_number = '429'  # room we are entering

        self.usr2 = User(user_id='8102', pin='0002', card='123')  # creating a test user
        self.usr_credentials = [('pin', 'card')]  # what the user uses to enter the room
        self.room_number = '429'  # room we are entering

        self.usr3 = User(user_id='8103', pin='0003', card='123')  # creating a test user
        self.usr_credentials = [('pin', 'card')]  # what the user uses to enter the room
        self.room_number = '429'  # room we are entering

        self.user_list = [self.usr1, self.usr2, self.usr3]
        # ------------ end Database -------------------------------

        """
        The buffers hold the keystrokes in arrays, the arrays later
        get joined together to form strings, and those are stored in the
        input QLineEdit objects. The labels help the user identify what
        they should input into the box.
        """
        self.usr_id_buffer = []
        self.pin_buffer = []
        self.card_buffer = []

        self.usr_id_label = QLabel("ID#: ")
        self.usr_id_input = QLineEdit()

        self.card_label = QLabel("Card: ")
        self.card_input = QLineEdit()

        self.pin_label = QLabel("Pin: ")
        self.pin_input = QLineEdit()

        self.init_ui()  # holds the GUI outline

    # ActionListener
    def button_click(self):
        digit = self.sender()

        """
        If Clear is pressed the boxes get emptied.
        """
        if digit.text() == 'Clear':
            return self.empty_input_boxes()

        """
        If Enter is pressed...
        * both input boxes get stored as string tuples into pin_pad_input
        * The user ID entered gets checked against the database

        * If a match is not found:
            - The entry is denied and admin is alerted.

        * If a match is found:
            - pin_pad_input get compared with it's corresponding value in the User's profile.
                + If they are correct the User is given clarence to enter.
                + If they are not correct the User is denied entry and the Admin is alerted.

        """
        if digit.text() == "Enter":
            self.card_buffer = self.pin_input.text()

            pin_pad_input = (str(self.pin_input.text()), str(self.card_input.text()))
            print(pin_pad_input)

            for user in self.user_list:  # comparing with DATABASE

                # User ID  match found
                if self.usr_id_input.text() == user.get_name():
                    self.check_access(user, self.room_number, self.usr_credentials, pin_pad_input)
                    self.empty_input_boxes()
                    break

                # User ID Match is not found
                else:
                    print("Invalid ID.")
                    self.alert_admin()
                    self.empty_input_boxes()
                    break
            return  # exits out of the function

        if len(self.usr_id_buffer) < 4:  # Allows only 4 ID characters
            temp_digit = int(digit.text())
            self.usr_id_buffer.append(temp_digit)
            self.usr_id_input.setText(''.join(str(e) for e in self.usr_id_buffer))

        elif len(self.pin_buffer) < 4:  # Allows only 4 Pin characters
            temp_digit = int(digit.text())
            self.pin_buffer.append(temp_digit)
            self.pin_input.setText(''.join(str(e) for e in self.pin_buffer))

        else:
            temp_digit = int(digit.text())  # Card digits can be longer (Unspecified as of yet)
            self.card_buffer.append(temp_digit)
            self.card_input.setText(''.join(str(e) for e in self.card_buffer))

    """
    The init_ui Function holds the layout of the GUI
    and where every object is located.
    """

    # ----------------------initUI--------------------------------
    def init_ui(self):
        grid = QGridLayout()

        self.setLayout(grid)

        number_btns = ['1', '2', '3',
                       '4', '5', '6',
                       '7', '8', '9',
                       'Clear', '0', 'Enter']

        positions = [(i, j) for i in range(5) for j in range(3)]

        for position, number in zip(positions, number_btns):

            if number == '' or number == ' ':  # Skips the spaces in the number btns
                continue

            button = QPushButton(number)
            button.clicked.connect(self.button_click)
            grid.addWidget(button, *position)

        # Object positioning for the grid Layout
        grid.addWidget(self.usr_id_label, 4, 0)
        grid.addWidget(self.usr_id_input, 4, 1, 2, 2)
        grid.addWidget(self.pin_label, 6, 0)
        grid.addWidget(self.pin_input, 6, 1, 2, 2)
        grid.addWidget(self.card_label, 8, 0)
        grid.addWidget(self.card_input, 8, 1, 2, 2)

        self.move(300, 150)  # Initial position
        self.setWindowTitle('PinPad')
        self.show()
        # ----------------------End initUI--------------------------------

    """ This serves to clear the boxes."""

    def empty_input_boxes(self):
        self.usr_id_buffer, self.pin_buffer, self.card_buffer = [], [], []
        self.card_input.setText("")
        self.pin_input.setText("")
        self.usr_id_input.setText("")

    """
    Function checks that the user has access to the room
    and that the user's entered passwords are valid.

    - param password (tuple) : is the input from the user
    - param input_type (List of tuple): is the source of the input
        (ex. card reader, pin pad, biometrics scanner)

    - param room (string): is the room number the user is trying to access
    """

    def check_access(self, user, room, input_type, password):

        inp = self.switch(user, input_type)  # Holds a tuple with the User's real passwords

        if password == inp:  # this checks both inputs are correct
            print("Password verified!")

            try:
                if user.access_to_rooms[room]:  # Checks that the uses has access to this room
                    print("Door Opens!")
                else:
                    print("You don't have access to this room!")

            except KeyError:
                print("You don't have access to this room!")
        else:
            self.alert_admin()
            print("Invalid Password!")
        self.empty_input_boxes()

    """
    The switch function works like a switch does in other languages.

    It returns the value of the passwords associated with
    the User's account depending on the input source.

    The return value is a tuple.

    - param user: is the user object
    - param inp (list of tuples): is a list of tuples holding one tuple
        whose values are the two forms of identification the user is
        attempting to use.
    """

    @staticmethod
    def switch(user, inp):
        l = {
            'pin': user.get_pin(),
            'biometrics': user.get_biometrics(),
            'card': user.get_card()
        }

        for val1, val2 in inp:
            return l[val1], l[val2]

    """
    The alert_admin: send the admin an Alert
    via ssh, that someone is attempting to enter a room
    without proper authentication or clearance.
    """

    @staticmethod
    def alert_admin():
        # user_ip = 'Yamnel@10.0.0.6'  # My house's local
        user_ip = 'Yamnel@10.100.201.34'  # School's
        path = '~/Desktop/Warning.py'  # Path to warning on my machine

        try:
            os.system('ssh {} nohup python {} &'.format(user_ip, path))
        except Exception:
            print("Admin was not reached!!! ", Exception)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui_window = SystemGUI()
    sys.exit(app.exec_())
