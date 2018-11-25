import re

#pattern = re.compile(r';.*#\W([^a-zA-Z ]*)')
pattern = re.compile(r';\sfully-qualified\W*#\W([^a-zA-Z ]*)')
    
def emoji_list():
    text = open("emoji-test.txt","r")
    lines = text.readlines()
    return set(re.findall(pattern, '\n'.join(lines)))
