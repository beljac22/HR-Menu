from employee import *
from pytest import *

@fixture
def employee():
    return Salaried("Bob","bob@acme-machining.com",60000.0)

# constructor
def test_ID_num_set(employee):
    with raises(AttributeError):
        employee.id_number = 324

def test_bad_salary(employee):
    with raises(ValueError):
        Salaried("Bob","bob@acme-machining.com",49999.0)

def test_bad_email(employee):
    with raises(ValueError):
        Salaried("Bob","bob@acme-machining.gov",50000.0)

def test_bad_name(employee):
    with raises(ValueError):
        Salaried("","bob@acme-machining.com",50000.0)

def test_normal_construction(employee):
    Salaried("Bob","bob@acme-machining.com",60000.0)

# email
def test_email_empty(employee):
    with raises(ValueError):
        employee.email = ""

def test_long_email(employee):
    employee.email = "bob@acme-machining.com"*999
    assert employee.email == "bob@acme-machining.com"*999

def test_email_wrong_type(employee):
    with raises(ValueError):
        employee.email =  999

def test_partial_email_str(employee):
    with raises(ValueError):
        employee.email = "bob@ame-machining.com"

def test_normal_email(employee):
    employee.email = "bob@acme-machining.com"
    assert employee.email == "bob@acme-machining.com"

# name
def test_empty_name(employee):
    with raises(ValueError):
        employee.name = ""

def test_long_name(employee):
    employee.name = "Bob" * 20000
    assert employee.name == "Bob" * 20000

def test_special_characters(employee):
    employee.name = "#$@#$@!%$%%$^%&^*&^(^(*&|||||\\\\\\\\\\"
    assert employee.name == "#$@#$@!%$%%$^%&^*&^(^(*&|||||\\\\\\\\\\"

def test_short_name(employee):
    employee.name = "B"
    assert employee.name == "B"

def test_int_name(employee):
    with raises(ValueError):
        employee.name = 74534

# image path
def test_default_image_path(employee):
    assert employee.image == "./images/placeholder.png"

def test_new_image_path(employee):
    employee.image = "./testimage/path.png"
    assert employee.image == "./testimage/path.png"

def test_int_image_path(employee):
    with raises(ValueError):
        employee.image = 34234234

def test_empty_image_path(employee):
    with raises(ValueError):
        employee.image = ""

def test_long_image_path(employee):
    employee.image = "randomtext"*9001
    assert employee.image == "randomtext"*9001

# salary
def test_empty_salary(employee):
    with raises(ValueError):
        employee.yearly = None

def test_large_sal(employee):
    employee.yearly = 999999999999.0
    assert employee.yearly == 999999999999.0

def test_low_edge_salary(employee):
    with raises(ValueError):
        employee.yearly = 49999.0

def test_on_edge_salary(employee):
    with raises(ValueError):
        employee.yearly = 50000.0

def test_upper_edge_salary(employee):
    employee.yearly = 50001.0
    assert employee.yearly == 50001.0

def test_str_salary(employee):
    with raises(ValueError):
        employee.yearly = "hello"

def test_int_salary(employee):
    with raises(ValueError):
        employee.yearly = 4234234