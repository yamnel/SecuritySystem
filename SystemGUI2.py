import sys, os
from PyQt5.Qt import *
from User import User


class SystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        # holders hold the text entered by the user and create a string.
        self.pin_holder = []
        self.card_holder = []



        self.card_label = QLabel("Card: ")
        self.card_input = QLineEdit()

        self.pin_label = QLabel("Pin: ")
        self.pin_input = QLineEdit()

        self.initUI()
        # self.main()


        # ------------ Main() -------------------------------
        # creating a test user
        self.usr = User(user_id='8108', pin='0000', card='123')

        # what the user uses to enter the room
        self.usr_credentials = [('pin', 'card')]

        self.room_number = '429'

        # pin_pad_input = (str(self.userNameEdit), str(self.showPassEdit))

    # ActionListener
    def buttonClick(self):
        digit = self.sender()

        # Handle Clear button
        if (digit.text() == 'Clear'):
            # print("clr pressed, clearing")  # TESTING
            self.pin_holder = []
            self.card_input.setText("")

            self.card_holder = []
            self.pin_input.setText("")
            return

        # Handle Enter button
        if (digit.text() == "Enter"):
            # print("Enter was pressed")  # TESTING

            self.card_holder = self.pin_input.text()
            # print(self._userName)

            pin_pad_input = (str(self.pin_input.text()), str(self.card_input.text()))
            print(pin_pad_input)

            self.check_access(self.usr, self.room_number, self.usr_credentials, pin_pad_input)

            # self.close()
            return

        # Test-----
        # print(digit.text() + " was pressed")

        # #Test -----
        # print(int(''.join((map(str, self.__password)))))
        #


        if ((len(self.pin_holder) < 4)):
            tempDigit = int(digit.text())
            self.pin_holder.append(tempDigit)

            # Test -----
            # print(int(''.join((map(str, self.pin_holder)))))
            # str1 = ''.join(str(e) for e in self.pin_holder)

            self.pin_input.setText(''.join(str(e) for e in self.pin_holder))

        else:
            tempDigit = int(digit.text())
            self.card_holder.append(tempDigit)

            # Test -----
            # print(int(''.join((map(str, self.card_holder)))))
            # str1 = ''.join(str(e) for e in self.card_holder)

            self.card_input.setText(''.join(str(e) for e in self.card_holder))

            # ----------------------End buttonClick------------------------

    # Getters
    # def get_password(self):
    #     return self.__password
    # def get_userName(self):
    #     return self._userName

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

        grid.addWidget(self.pin_label, 4, 0)
        grid.addWidget(self.pin_input, 4, 1, 2, 2)
        grid.addWidget(self.card_label, 6, 0)
        grid.addWidget(self.card_input, 6, 1, 2, 2)

        self.move(300, 150)
        self.setWindowTitle('PinPad')
        self.show()
        # ----------------------End initUI--------------------------------

    # the password is the input from the user
    # the input_type is the source of the input
    # ( ex. card reader, pin pad, biometrics scanner)

    def check_access(self, user, room, input_type, password):
        inp = self.switch(user, input_type)

        # print("\nThe user's saved passwords are: ", ", ".join(inp), "\nThe entered passwords were: ",
        #       ", ".join(password), "\n")  # Testing

        if password == inp:  # this checks both passwords are correct
            print("Password verified!")

            try:
                if user.access_to_rooms[room]:
                    print("Door Opens!")
                else:
                    print("You don't have access to this room!")
            # catches
            except KeyError:
                print("You don't have access to this room!")
        else:
            try:
                self.alert_admin()
            except Exception:
                print("Admin was not reached!!! ", Exception)
            print("Invalid Password!")

        self.pin_holder, self.card_holder = [], []
        self.card_input.setText("")
        self.pin_input.setText("")



    # it returns the value of the access type
    # depending on the input source
    # it works like a switch does in other languages
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
        #user_ip = 'Yamnel@10.0.0.6'
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
