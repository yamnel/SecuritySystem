import os
import sys

from PyQt5.Qt import *

from User import User


class SystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        # holders hold the text entered by the user and create a string.
        self.usr_id_buffer = []
        self.pin_buffer = []
        self.card_buffer = []

        self.usr_id_label = QLabel("ID#: ")
        self.usr_id_input = QLineEdit()

        self.card_label = QLabel("Card: ")
        self.card_input = QLineEdit()

        self.pin_label = QLabel("Pin: ")
        self.pin_input = QLineEdit()

        self.initUI()

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

    # ActionListener
    def buttonClick(self):
        digit = self.sender()

        # Handle Clear button
        if (digit.text() == 'Clear'):
            self.empty_input_boxes()
            return

        # Handle Enter button
        if digit.text() == "Enter":
            self.card_buffer = self.pin_input.text()

            pin_pad_input = (str(self.pin_input.text()), str(self.card_input.text()))
            print(pin_pad_input)

            for user in self.user_list:
                if self.usr_id_input.text() == user.get_name():
                    self.check_access(user, self.room_number, self.usr_credentials, pin_pad_input)
                    self.empty_input_boxes()
                    break
                else:
                    print("Invalid ID.")
                    self.empty_input_boxes()
                    break
            return

        if ((len(self.usr_id_buffer) < 4)):
            tempDigit = int(digit.text())
            self.usr_id_buffer.append(tempDigit)
            self.usr_id_input.setText(''.join(str(e) for e in self.usr_id_buffer))

        elif ((len(self.pin_buffer) < 4)):
            tempDigit = int(digit.text())
            self.pin_buffer.append(tempDigit)
            self.pin_input.setText(''.join(str(e) for e in self.pin_buffer))

        else:
            tempDigit = int(digit.text())
            self.card_buffer.append(tempDigit)
            self.card_input.setText(''.join(str(e) for e in self.card_buffer))

    def initUI(self):
        grid = QGridLayout()

        self.setLayout(grid)

        number_btns = ['1', '2', '3',
                       '4', '5', '6',
                       '7', '8', '9',
                       'Clear', '0', 'Enter']

        positions = [(i, j) for i in range(5) for j in range(3)]

        for position, number in zip(positions, number_btns):

            if number == '' or number == ' ':
                continue

            button = QPushButton(number)
            button.clicked.connect(self.buttonClick)
            grid.addWidget(button, *position)

        grid.addWidget(self.usr_id_label, 4, 0)
        grid.addWidget(self.usr_id_input, 4, 1, 2, 2)
        grid.addWidget(self.pin_label, 6, 0)
        grid.addWidget(self.pin_input, 6, 1, 2, 2)
        grid.addWidget(self.card_label, 8, 0)
        grid.addWidget(self.card_input, 8, 1, 2, 2)

        self.move(300, 150)
        self.setWindowTitle('PinPad')
        self.show()
        # ----------------------End initUI--------------------------------

    def empty_input_boxes(self):
        self.usr_id_buffer, self.pin_buffer, self.card_buffer = [], [], []
        self.card_input.setText("")
        self.pin_input.setText("")
        self.usr_id_input.setText("")

    """
    the password is the input from the user
    the input_type is the source of the input
    ( ex. card reader, pin pad, biometrics scanner)
    """

    def check_access(self, user, room, input_type, password):

        inp = self.switch(user, input_type)

        if password == inp:  # this checks both passwords are correct
            print("Password verified!")

            try:
                if user.access_to_rooms[room]:
                    print("Door Opens!")
                else:
                    print("You don't have access to this room!")

            except KeyError:
                print("You don't have access to this room!")
        else:
            try:
                self.alert_admin()
            except Exception:
                print("Admin was not reached!!! ", Exception)
            print("Invalid Password!")

        self.usr_id_buffer, self.pin_buffer, self.card_buffer = [], [], []
        self.card_input.setText("")
        self.pin_input.setText("")
        self.usr_id_input.setText("")

    """
    It works like a switch does in other languages.
    It returns the value of the access type
    depending on the input source
    """

    def switch(self, user, inp):
        l = {
            'pin': user.get_pin(),
            'biometrics': user.get_biometrics(),
            'card': user.get_card()
        }

        for val1, val2 in inp:
            # print((l[val1], l[val2])) # Testing
            return l[val1], l[val2]

    def alert_admin(self):
        # user_ip = 'Yamnel@10.0.0.6'
        user_ip = 'Yamnel@10.100.201.34'

        path = 'python3 ~/Desktop/Warning.py'
        try:
            os.system('ssh {} nohup python /Users/Yamnel/Desktop/Warning.py &'.format(user_ip))
        except Exception:
            print("Admin was not reached!!! ", Exception)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui_window = SystemGUI()
    sys.exit(app.exec_())
