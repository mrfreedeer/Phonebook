import json
import collections

class Contact(object):
    def __init__(self):
        self._info = collections.OrderedDict()
    def add(self,user, field, parameter = None, value = None):
        if not(user in self._info):
            if isinstance(parameter, dict):
                d = {field : parameter}
                self._info[user] = d
            else:
                s = {parameter : value}
                d = {field : s}
                self._info[user] = d
        else:
            temp = collections.OrderedDict()
            if isinstance(parameter,dict):
                for x in self._info[user]:
                    temp[x] = self._info[user][x]
                temp[field] = parameter
                self._info[user] = temp
            else:
                temp = collections.OrderedDict()
                for x in self._info[user]:
                    if x != field:
                        temp[x] = self._info[user][x]
                    else:
                        p = {}
                        for y in self._info[user][field]:
                            p[y] = self._info[user][field][y]
                        p[parameter] = value
                        temp[field] = p
                self._info[user] = temp
    def surrender(self):
        return self._info
    @property
    def cprint(self):
        for x in self._info:
            print("Contacto: ", x,"\n")
            for y in self._info[x]:
                print("\n", y, ":\n")
                for z in self._info[x][y]:
                    print(z,":\t",self._info[x][y][z])

class PhoneBook(object):
    def __init__(self):
        self._contacts = []
    def add(self, user, field = None, parameter = None, value = None):
        if isinstance(user, Contact):
            self._contacts.append(user)
        else:
            c = Contact()
            c.add(user,field,parameter,value)
    def tojson(self):
        temp = []
        for x in self._contacts:
            temp.append(x.surrender())
        return temp
    def fromjson(self, data):
        for x in data:
            for y in x:
                c = Contact()
                for z in x[y]:
                    c.add(y,z,x[y][z])
                self.add(c)
    @property
    def cprint(self):
        for x in self._contacts:
            x.cprint
            print("\n\n")


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
    load = True

    if not load:
        random = collections.OrderedDict()
        random2 = collections.OrderedDict()
        random = {'Nombre' : 'Juan', 'Apellidos' : 'Ospina'}
        random2 = {'Casa' : 3205093, 'Cel' : 3175114183}
        emails = {'Trabajo' : 'juanpablo.ospina@utp.edu.co', 'Casa' : 'juanpabloospina1998@gmail.com', 'Test' : 'juanpabloospina1998@hotmail.com'}
        c = Contact()
        c.add('Juan', 'Información', random)
        c.add('Juan','Teléfonos',random2)
        c.add('Juan','Teléfonos','Trabajo',3333330)
        c.add('Juan','Emails',emails)

        random3 = collections.OrderedDict()
        random4 = collections.OrderedDict()
        random5 = collections.OrderedDict()
        random3 = {'Nombre' : 'Juan', 'Apellidos' : 'Zurita'}
        random4 = {'Casa' : 30000001, 'Cel' : 3000114183}
        random5 = {'Trabajo' : 'juanpabloospina1998@yahoo.com'}
        o = Contact()
        o.add('Juan','Infomación',random3)
        o.add('Juan','Teléfonos',random4)
        o.add('Juan','Emails',random5)

        p = PhoneBook()
        p.add(c)
        p.add(o)
        p.cprint
        savePbk(p)

    else:
        p = loadPbk()
        p.cprint
if __name__ == '__main__':
    main()
