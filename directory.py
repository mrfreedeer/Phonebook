import json
import collections

class Name(object):
    def __init__(self, namedir = None,  pref = None, first = None, middle = None, surn = None, suff = None):
        if namedir == None:
            self._namedict = collections.OrderedDict()
            self._namedict = {'prefix' : pref, 'firstname' : first, 'middlename' : middle, 'surname' : surn, 'suffix' : suff}
        else:
            self._namedict = namedir
    def __str__(self):
        return 'Prefijo: {}\nNombre: {}\nSegundo Nombre: {}\nApellidos: {}\nSufijo: {}'.format(self._namedict['prefix'],self._namedict['firstname'],self._namedict['middlename'],self._namedict['surname'],self._namedict['suffix'])
    @property
    def cprint(self):
        for x in self._namedict:
            if self._namedict[x] != None:
                print(x,self._namedict[x],)
    def add(self, atribute, value = None):
        l = ['prefix', 'firstname','middlename','surname','suffix']
        if not isinstance(atribute,dict):
            assert atribute in l
            self._namedict[atribute] = value
        else:
            for x in atribute:
                assert x in l
                self._namedict[x] = atribute[x]
    def surrender(self):
        return self._namedict

class Phones(object):
    def __init__(self, type = None, phone = None):
        if isinstance(type,dict):
            self._phones = type
        else:
            self._phones = {type : phone}
    def add(self, obj, phone = None):
        if isinstance(obj,dict):
            self._phones = obj
        else:
            self._phones[obj] = phone
    @property
    def cprint(self):
        print("\nTelefonos:",)
        for x in self._phones:
            print(x," : ",self._phones[x])
    def surrender(self):
        return self._phones
class Email(object):
    def __init__(self,obj = None, email = None):
        if isinstance(obj, dict):
            self._emails = obj
        else:
            self._emails = {obj : email}
    def add(self,obj, email = None):
        if isinstance(obj, dict):
            for x in obj:
                self._emails[x] = obj[x]
        else:
            self._emails[obj] = email
    def surrender(self):
        return self._emails
    @property
    def cprint(self):
        print("\nEmails: ",)
        for x in self._emails:
            print(x,":\t",self._emails[x])

class PhoneBook(object):
    def __init__(self):
        self._contents = []
        self._contacts = collections.OrderedDict()
    def add(self,name, namedir, phone = None, emails = None, valuename = None, phonevalue = None, emailvalue = None):
        temp = collections.OrderedDict()
        if isinstance(namedir, Name):
            temp[info] = namedir
        elif isinstance(namedir, dict):
            n = Name()
            n.add(namedir)
            temp['info'] = n
        else:
            n = Name()
            n.add(name,valuename)
            temp = {'info' : n}

        if isinstance(phone, Phones):
            temp['phones'] = phone
        elif isinstance(phone,dict):
            m = Phones(phone)
            temp['phones'] = m
        else:
            if phone is not None:
                p = Phones(phone,phonevalue)
                temp['phones'] = p

        if isinstance(emails, Email):
            temp['emails'] = emails
        elif isinstance(emails,dict):
            e = Email(emails)
            temp['emails'] = e
        else:
            e = Email(emails,emailvalue)
            temp['emails'] = e

        self._contacts[name] = temp
    def classify(self):
        for x in self._contacts:
            for y in self._contacts[x]:
                if type(self._contacts[x][y]) not in self._contents:
                    self._contents.append(type(self._contacts[x][y]))

    def tag(self,type):
        if type == Name:
            return 'info'
        elif type == Phones:
            return 'phones'
        else:
            return 'emails'
    def untag(self,tag):
        if tag == 'info':
            return Name
        elif tag == 'phones':
            return Phones
        else:
            return Email

    def tojson(self):
        self.classify()
        converted = {}
        z = {}
        for x in self._contacts:
            for y in self._contents:
                z[self.tag(y)] = self._contacts[x][self.tag(y)].surrender()
            converted[x] = z
        return converted
    def fromjson(self, jsondict):
        temp = {}
        for x in jsondict:
            for y in jsondict[x]:
                k = jsondict[x][y]
                i = self.untag(y)
                temp[y] =i(k)
            self._contacts[x] = temp

    @property
    def cprint(self):
        first = True
        for x in self._contacts:
            print("Contacto:\t", x, "\n")
            #print (self._contacts[x]['info'])
            for y in self._contacts[x]:
                k = self.untag(y)
                self._contacts[x][y].cprint


def loadPbk():
    json_data=open("/home/juan/Escritorio/Python/PhoneBook.txt").read()
    data = json.loads(json_data)
    p = PhoneBook()
    p.fromjson(data)
    return p
def savePbk(p):
    with open("/home/juan/Escritorio/Python/PhoneBook.txt","w") as f:
        json.dump(p.tojson(),f)


def main():
    load = False
    write = True
    if load:
         p = loadPbk()
         p.cprint
    else:
        s = Name()
        random = {'firstname' : 'Juan', 'surname' : 'Ospina'}
        random2 = {'Casa' : 3205093, 'Cel' : 3175114183}
        emails = {'Trabajo' : 'juanpablo.ospina@utp.edu.co', 'Casa' : 'juanpabloospina1998@gmail.com', 'Test' : 'juanpabloospina1998@hotmail.com'}
        e = Email(emails)
        s.add('firstname','Juan')
        p = PhoneBook()
        print("\n\n->   ",p._contacts)
        p.add('Juan',random, random2,e)

        p.cprint
        if write:
            savePbk(p)


if __name__ == '__main__':
    main()
