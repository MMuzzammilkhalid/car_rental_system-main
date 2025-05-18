# models/user.py

from abc import ABC, abstractmethod

class User(ABC):
    """
    Abstract base class for all user types (e.g., Admin, Customer).
    Enforces a common interface and shared attributes.
    """

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    @abstractmethod
    def view_profile(self):
        """
        Abstract method that must be implemented by subclasses.
        Displays the user's profile information.
        """
        pass
