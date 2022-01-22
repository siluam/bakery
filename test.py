from inspect import isclass
def convert(converting, **kwargs):
    for key, value in kwargs.items():
        if value and isclass(eval(key[1:])):
            return(eval(key[1:])(converting))
string = "Hello!"
print(convert(string, _list = True))
