from re import split

def camelize(string):
        s = ''.join([a.capitalize() for a in split('([^a-zA-Z0-9])', string) if a.isalnum()])
        return s[0].lower() + s[1:]

cols = ['Team Name', 'Hero', 'All Damage Done', "Enemies EMP'd"]
res = [camelize(c) for c in cols]
print(res)