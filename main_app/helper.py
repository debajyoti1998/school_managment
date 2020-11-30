import hashlib


def __is_email(x):
    a=0
    y=len(x)
    dot=x.find(".")
    at=x.find("@")
    for i in range (0,at):
        if((x[i]>='a' and x[i]<='z') or (x[i]>='A' and x[i]<='Z')):
            a=a+1
    if(a>0 and at>0 and (dot-at)>0 and (dot+1)<y):
        return True
    else:
        return False


def __is_alpha_num_space (data):
    if all(x.isalnum() or x.isspace() for x in data):
        return True
    else :
        return False

def __is_alpha_space (data):
    if all(x.isalpha() or x.isspace() for x in data):
        return True
    else :
        return False

def __is_alphabet (data):
    if all( x.isalpha() for x in data):
        return True
    else :
        return False

def __is_number (data):
    if all(x.isnumeric() for x in data):
        return True
    else :
        return False





def __create_encryption(input):
    application_salt = 'hicsjcbssduhcsdjbcj'
    new_pass = application_salt+ str(input)
    hashvalue= hashlib.sha256(new_pass.encode())
    x= hashvalue.hexdigest()
    return x