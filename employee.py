import abc
from enum import Enum
import datetime
from os import path

class Role(Enum):
    """
    Jack Bellgowan
    Enumeration holding variables associating to manager types 1-3
    """
    CEO = 1
    CFO = 2
    CIO = 3

class Department(Enum):
    """
    Jack Bellgowan
    Enumeration holding variables associating to department types 1-5
    """
    ACCOUNTING = 1
    FINANCE = 2
    HR = 3
    R_AND_D = 4
    MACHINING = 5

class InvalidRoleException(Exception):
    """
    Jack Bellgowan
    Custom exception type raised when invalid role is given
    """
    def __init__(self, message: str):
        """
        Excepts message as a str parameter, raises an exception called
        InvalidRoleException with the message var as a message
        """
        super().__init__(message)

class InvalidDepartmentException(Exception):
    """
    Jack Bellgowan
    Custom exception type raised when invalid department is given
    """
    def __init__(self, message: str):
        """
        Jack Bellgowan
        Excepts message as a str parameter, raises an exception called
        InvalidDepartment Exception with the message var as a message
        """
        super().__init__(message)

class Employee(abc.ABC):
    """
    Jack Bellgowan
    Abstract Basic class holding info about an object of parent type employee
    """
    CURRENT_ID: int = 1
    IMAGE_PLACEHOLDER: str = "./images/placeholder.png"
    def __init__(self, name: str, email: str):
        """
        Jack Bellgowan
        Accepts employee name as a str, and email as a str.
        """
        self.name: str = name
        self.email: str = email
        self._id_number: int = Employee.CURRENT_ID
        self.image: str = Employee.IMAGE_PLACEHOLDER
        # adds to CURRENT_ID so next employee has unique ID
        Employee.CURRENT_ID += 1

    @property
    def email(self) -> str:
        """
        Jack Bellgowan
        getter for self._email
        returns str
        """
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        """
        Jack Bellgowan
        Setter for self._email, checks if email is empty or not
        the correct domain.
        Raises ValueError if email is invalid.
        returns None
        """
        # Checks content of email
        if not isinstance(email, str) or not email or "@acme-machining.com" not in email:
            raise ValueError("Invalid email")
        # sets email
        self._email: str = email

    @property
    def name(self) -> str:
        """
        Jack Bellgowan
        getter for self._name
        returns str
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Jack Bellgowan
        Setter for self._name, checks if name is empty.
        Raises ValueError if name is invalid.
        returns None
        """
        # Checks content of name
        if not name or not isinstance(name,str):
            raise ValueError("Invalid name")
        # sets name
        self._name: str = name

    @property
    def image(self) -> str:
        """
        Jack Bellgowan
        getter for self._image
        Returns str
        """
        return self._image

    @image.setter
    def image(self, image: str) -> None:
        """
        Jack Bellgowan
        Setter for self._image, checks if image is empty.
        Raises ValueError if image is invalid.
        returns None
        """
        # Checks content of image
        if not image or not isinstance(image,str) or not path.exists(image):
            raise ValueError("Invalid image")
        # sets image
        self._image: str = image

    @property
    def id_number(self) -> int:
        """
        Jack Bellgowan
        getter for self._id_number
        returns int
        """
        return self._id_number

    def __str__(self) -> str:
        """
        Jack Bellgowan
        returns basic text representation of an object of type
        Employee as type str.
        Returns str.
        """
        return f"{self._id_number}:{self.name}"

    @abc.abstractmethod
    def calc_pay(self) -> float:
        """Jack Bellgowan
        This function calculates the weekly pay
        for the current employee in our pay report"""
        pass

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Employee as type str.
        Returns str.
        """
        return f"{self.name},{self.email},{self.image}"

class Salaried(Employee):
    """Jack Bellgowan
    Class holding info for all objects of type Salaried."""
    def __init__(self, name: str, email: str, yearly: float):
        """constructor"""
        super().__init__(name, email)
        self.yearly: float = yearly

    @property
    def yearly(self) -> float:
        """Jack Bellgowan
        getter for self._yearly
        Returns float
        """
        return self._yearly

    @yearly.setter
    def yearly(self, yearly: float) -> None:
        """Jack Bellgowan
        Setter for self._yearly, checks if yearly is non-negative and
        over 50000.
        Raises ValueError if yearly is invalid.
        returns None
        """
        # Checks value of yearly
        if not isinstance(yearly, float) or yearly <= 50000:
            raise ValueError("Invalid yearly salary")
        # sets yearly
        self._yearly: float = yearly

    def calc_pay(self) -> float:
        """Jack Bellgowan
        This function calculates the weekly pay
        for the current salaried employee in our pay report"""
        return self.yearly / 52

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Salaried as type str.
        Returns str.
        """
        return f"{super().__repr__()},{self.yearly}"

class Hourly(Employee):
    """Jack Bellgowan
    Class holding info for all objects of type Hourly."""
    def __init__(self, name: str, email: str, hourly: float):
        """Jack Bellgowan
        constructor taking name as a type str corresponding to employee name,
        email as a type str corresponding to employee email, and hourly as a float
         corresponding to employee wage
        """
        super().__init__(name, email)
        self.hourly: float = hourly

    @property
    def hourly(self) -> float:
        """Jack Bellgowan
        getter for self._hourly
        Returns float
        """
        return self._hourly

    @hourly.setter
    def hourly(self, hourly: float) -> None:
        """Jack Bellgowan
        Setter for self._hourly, checks if hourly is
        between 15 and 99.99.
        Raises ValueError if hourly is invalid.
        returns None
        """
        # Checks value of hourly
        if not 15 < hourly < 99.99 or not isinstance(hourly, float):
            raise ValueError("Invalid hourly salary")
        # sets hourly
        self._hourly: float = hourly

    def calc_pay(self) -> float:
        """Jack Bellgowan
        This function calculates the weekly pay
        for the current hourly employee in our pay report"""
        return self.hourly * 40

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Hourly as type str.
        Returns str.
        """
        return f"{super().__repr__()},{self.hourly}"

class Executive(Salaried):
    """Jack Bellgowan
    Class holding info for all objects of type Executive."""
    def __init__(self, name: str, email: str, yearly: float, role: Role):
        """Jack Bellgowan
        constructor taking name as a type str corresponding to employee name,
        email as a type str corresponding to employee email, Role for the employee's Role, and yearly as a float
        corresponding to employee salaru
        returns None
        """
        super().__init__(name, email, yearly)
        # sets the employee's Role
        self.role: Role = role

    @property
    def role(self) -> Role:
        """Jack Bellgowan
        getter for self._yearly
        Returns Role
        """
        return self._role

    @role.setter
    def role(self, role: Role) -> None:
        """Jack Bellgowan
        Setter for self._role, checks if role is not 1-3
        Raises an InvalidRoleException if role is invalid.
        returns None
        """
        # Checks value of role
        if not 1 <= role.value <= 3 or not isinstance(role, Role):
            raise InvalidRoleException("Invalid role")
        # sets role
        self._role: Role = role

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Executive as type str.
        Returns str.
        """
        return f"Executive,{super().__repr__()},{self.role}"

class Manager(Salaried):
    """Jack Bellgowan
    Class holding info for all objects of type Manager."""
    def __init__(self, name: str, email: str, yearly: float, department: Department):
        """Jack Bellgowan
        constructor taking name as a type str corresponding to employee name,
        email as a type str corresponding to employee email, an employee department
        for their department and yearly as a float
        corresponding to employee salary
        """
        super().__init__(name, email, yearly)
        # sets employee department
        self.department: Department = department

    @property
    def department(self) -> Department:
        """Jack Bellgowan
        getter for self._yearly
        Returns Department
        """
        return self._department

    @department.setter
    def department(self, department: Department) -> None:
        """Jack Bellgowan
        Setter for self._department, checks if role is not 1-5
        Raises an InvalidDepartmentException if department is invalid.
        returns None
        """
        # Checks value of department
        if not 1 <= department.value <= 5 or not isinstance(department, Department):
            raise InvalidDepartmentException("Invalid department")
        # sets department
        self._department: Department = department

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Manager as type str.
        Returns str.
        """
        return f"Manager,{super().__repr__()},{self.department}"

class Permanent(Hourly):
    """Jack Bellgowan
    Class holding info for all objects of type Permanent."""
    def __init__(self, name: str, email: str, hourly: float, hired_date: datetime.date):
        """
        Jack Bellgowan
        constructor taking name as a type str corresponding to employee name,
        email as a type str corresponding to employee email, an employee department
        for their department and hourly as a float
        corresponding to employee wage, and hired date
        """
        super().__init__(name, email, hourly)
        self.hired_date: datetime.date = hired_date

    @property
    def hired_date(self) -> datetime.date:
        """Jack Bellgowan
        getter for self._hired_date
        Returns datetime
        """
        return self._hired_date

    @hired_date.setter
    def hired_date(self, hired_date: datetime.date) -> None:
        """Jack Bellgowan
        Setter for self._hired_date, checks if argument is datetime object
        Raises a ValueError if hired_date is invalid.
        returns None
        """
        # Checks value of hired date
        if not isinstance(hired_date, datetime.date):
            raise ValueError("Invalid hired date")
        # sets hired date
        self._hired_date: datetime.date = hired_date

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Permanent as type str.
        Returns str.
        """
        return f"Permanent,{super().__repr__()},"+self.hired_date.__repr__().replace(",","!")

class Temporary(Hourly):
    """Jack Bellgowan
    Class holding info for all objects of type Temporary."""
    def __init__(self, name: str, email: str, hourly: float, last_day: datetime.date):
        """Jack Bellgowan
        constructor taking name as a type str corresponding to employee name,
        email as a type str corresponding to employee email, an employee department
        for their department and hourly as a float
        corresponding to employee wage, and ending date
        """
        super().__init__(name, email, hourly)
        self.last_day: datetime.date = last_day

    @property
    def last_day(self) -> datetime.date:
        """Jack Bellgowan
        getter for self._hired_date
        Returns datetime
        """
        return self._last_day

    @last_day.setter
    def last_day(self, last_day: datetime.date) -> None:
        """Jack Bellgowan
        Setter for self._last_day, checks if argument is datetime object
        Raises a ValueError if last_day is invalid.
        returns None
        """
        # Checks value of last day
        if not isinstance(last_day, datetime.date):
            raise ValueError("Invalid last day")
        # sets last day
        self._last_day: datetime.date = last_day

    def __repr__(self) -> str:
        """Jack Bellgowan
        returns complex text representation of an object of type
        Temporary as type str.
        Returns str.
        """
        return f"Temporary,{super().__repr__()},"+self.last_day.__repr__().replace(",","!")
