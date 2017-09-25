import json

class Name(object):
    def __init__(self, pref = None, first = None, middle = None, surn = None, suff = None):
        self._namedict = {'prefix' : pref, 'firstname' : first, 'middlename' : middle, 'surname' : surn, 'suffix' : suff}
    @property
    def prefix(self):
        return self._namedict['prefix']
    @property
    def firstname(self):
        return self._namedict['firstname']
    @property
    def middlename(self):
        return self._namedict['middlename']
    @property
    def surname(self):
        return self._namedict['surname']
    @property
    def suffix(self):
        return self._namedict['suffix']
    def __str__(self):
        return 'Prefijo: {}\nNombre: {}\nSegundo Nombre: {}\nApellidos: {}\nSufijo: {}'.format(self._namedict['prefix'],self._namedict['firstname'],self._namedict['middlename'],self._namedict['surname'],self._namedict['suffix'])
    @property
    def cprint(self):
        for x in self._namedict:
            if self._namedict[x] != None:
                print(x,self._namedict[x],)
        print (self._namedict)
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
        for x in self._phones:
            print(x," : ",self._phones[x])
    def surrender(self):
        return self._phones

class PhoneBook(object):
    def __init__(self):
        self._contacts = {}
    def add(self,name, namedir, phone = None, valuename = None, phonevalue = None):
        temp = {}
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

        self._contacts[name] = temp

    def tojson(self):
        converted = {}
        for x in self._contacts:
            z = {'info' : self._contacts[x]['info'].surrender()}
            z['phones'] = self._contacts[x]['phones'].surrender()
            converted[x] = z
        return converted
    def fromjson(self, jsondict):
        for x in jsondict:
            y = jsondict[x]['info']
            z = jsondict[x]['phones']
            n = Name()
            n.add(y)
            m = Phones(z)
            temp ={'info' : n, 'phones' : m}
            self._contacts[x] = temp

    @property
    def cprint(self):
        for x in self._contacts:
            print("Contacto:\t", x, "\n")
            print(self._contacts[x]['info'])
            if 'phones' in self._contacts[x].keys():
                z = self._contacts[x]['phones']
                z.cprint



def main():
    """s = Name()
    random = {'firstname' : 'Juan', 'surname' : 'Ospina'}
    random2 = {'Casa' : 3205093, 'Cel' : 3175114183}

    s.add('firstname','Juan')
    p = PhoneBook()
    p.add('Juan',random, random2)
    p.cprint

    with open("/home/juan/Escritorio/Python/PhoneBook.txt","w") as f:
        json.dump(p.tojson(),f)

    """
    json_data=open("/home/juan/Escritorio/Python/PhoneBook.txt").read()
    data = json.loads(json_data)
    p = PhoneBook()
    p.fromjson(data)
    p.cprint
    #print("\n\n\n",data)




if __name__ == '__main__':
    main()
