"""
Class holds all the security information for the users
trying to gain access to the secure room.
"""


class User(object):
    def __init__(self, user_id, pin, card=None, biometrics=None):

        self.__user_id = str(user_id)  # Number that identifies the User

        # Forms of secure identification (passwords)
        self.__pin = str(pin)
        self.__card = str(card)
        self.__biometrics = str(biometrics)

        # Possible rooms the user has access to
        # by default the User will have access to room '429'!
        self.access_to_rooms = {'429': True}

    # getters
    def get_name(self):
        return self.__user_id

    def get_pin(self):
        return self.__pin

    def get_card(self):
        return self.__card

    def get_biometrics(self):
        return self.__biometrics

    def rename(self, new_name=None):
        if new_name is None:
            self.__user_id = self.get_name()
        else:
            self.__user_id = new_name

    # functions grant or remove access to rooms
    def set_access_to(self, *rooms, access=False):
        for key in rooms:
            self.access_to_rooms[str(key)] = access

    def grant_access_to_room(self, room):
        self.access_to_rooms[str(room)] = True

    def remove_access_to_room(self, room):
        self.access_to_rooms[str(room)] = False
