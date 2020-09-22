import importlib
import inspect
import os
import re
from freezegun import freeze_time
import session9
from session9 import *

MIN_TEST_CASES = 20
README_CONTENT_CHECK_FOR = ['decorator', 'odd', 'seconds', 'logs', 'factory', 'authentication', 'time', 'privilege']


# ----------------------------------------------Default checks Begin--------------------------------------------------#


def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"


def test_readme_contents():
    readme = open("README.md", "r", encoding="utf-8")
    readme_words = readme.read().split()
    readme.close()
    #readme_words = [word for line in open('README.md', 'r') for word in line.split()]
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"


def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"


def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 5


def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session9)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines" 

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


# def test_function_doc_string():
#     '''
#     Test case to check whether the functions have docstrings or not.
#     '''
#     functions = inspect.getmembers(session9, inspect.isfunction)
#     for function in functions:
#         assert function[1].__doc__

# def test_function_annotations():
#     '''
#     Test case to check whether the functions have annotations or not.
#     '''
#     functions = inspect.getmembers(session9, inspect.isfunction)
#     for function in functions:
#         assert function[1].__annotations__


# ----------------------------------------------Default checks End--------------------------------------------------#


# ----------------------------------------------Custom checks Begin-------------------------------------------------#


@freeze_time("2020-09-22 20:49:18")
def test_odd_it_even():
    @odd_it
    def add(a: int, b: int) -> int:
        return a + b
    assert add(1, 2) == None


@freeze_time("2020-09-22 20:49:21")
def test_odd_it_odd():
    def add(a: int, b: int) -> int:
        return a + b
    assert add(1, 2) == 3


@authenticate(curr_password=set_password(), user_password='root@123')
def add_1(a: int, b: int) -> int:
    return a+b


@authenticate(curr_password=set_password(), user_password='root@123')
def add_2(a: int, b: int) -> int:
    return a+b


def test_authenticate_correct_password():
    session9.get_password = lambda : 'root@123'
    assert add_1(1, 2) == 3, "Something wrong with authentication."


def test_authenticate_incorrect_password():
    session9.get_password = lambda : 'root@456'
    assert add_2(1, 2) == None, "Something wrong with authentication."


@Privilege("high")
def calc_sal_h(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Privilege("mid")
def calc_sal_m(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Privilege("low")
def calc_sal_l(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Privilege("no")
def calc_sal_n(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Privilege()
def calc_sal_(base, **kwargs):
    return sum([base]+list(kwargs.values()))




def test_privileges():
    _ = calc_sal_h(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1350000, "Privilege failed!"
    _ = calc_sal_m(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1300000, "Privilege failed!"
    _ = calc_sal_l(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1200000, "Privilege failed!"
    _ = calc_sal_n(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1000000, "Privilege failed!"
    _ = calc_sal_(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1000000, "Privilege failed!"


def test_singledispatch():
    assert htmlize(106) == '106(<i>0x6a</i>)'

    assert htmlize({'a': 1, 'b': 2, 'c': 3}) == """<ul>
<li>a=1</li>
<li>b=2</li>
<li>c=3</li>
</ul>"""

    assert htmlize([1, 2, 3, 4]) == """<ul>
<li>1(<i>0x1</i>)</li>
<li>2(<i>0x2</i>)</li>
<li>3(<i>0x3</i>)</li>
<li>4(<i>0x4</i>)</li>
</ul>"""

    assert htmlize(((1, 10), (2, 20), (3, 30))) == """<ul>
<li><ul>
<li>1(<i>0x1</i>)</li>
<li>10(<i>0xa</i>)</li>
</ul></li>
<li><ul>
<li>2(<i>0x2</i>)</li>
<li>20(<i>0x14</i>)</li>
</ul></li>
<li><ul>
<li>3(<i>0x3</i>)</li>
<li>30(<i>0x1e</i>)</li>
</ul></li>
</ul>"""

    assert htmlize('245 < 255') == '245 &lt; 255'

    assert htmlize('Any random text\n') == 'Any random text<br/>\n'

    assert htmlize(1.1232112) == '(<i>1.12</i>)'

# ----------------------------------------------Custom checks End---------------------------------------------------#