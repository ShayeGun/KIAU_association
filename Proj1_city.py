def generateID(database, tableName) -> str:
    id = int()
    for entity in database.DB[tableName]:
        if (entity['_id'] == str(id)):
            id += 1

    return str(id)

def addID(database, tableName, data) -> None:
    id = generateID(database, tableName)
    data.update({'_id' : id})

def createEntity(database, tableName, data) -> None:
    temp = {}
    id = generateID(database, tableName)
    temp.update({'_id' : id})

    for (k,v) in data.items():
        if (k in database.DBSchema[tableName].keys() and type(v) == database.DBSchema[tableName][k]):
            temp.update({k : v})
        else:
            pass
    # remove empty entities
    if (len(temp) > 1):
        database.DB[tableName].append(temp)

def validate():
    username = input('please enter username :\n')
    password = input('please enter password :\n')
    if(username == "shy" and password == "shy"):
        return True
    else:
        print("you're not shy honey🙃")
        return False

def inputToDict() -> dict:
    dic = {}
    while(True):
        key = input('please input a key :\n')
        val = input('please input a value :\n')
        dic.update({key : val})

        x = input('wanna add more ?\n')
        if (x == 'no' or x == 'exit'):
            break
        
    return dic

class ShyDB():
    def __init__(self):
        self.DB = {}
        self.DBSchema = {}

    def createTable(self,tableName:str) -> None:
        self.DB.update({tableName : []})

    def createSchema(self,tableName:str, data:dict) -> None:
        self.DBSchema[tableName] = data
    
    def addEntity(self, tableName:str, data:dict) -> None:
        if (not tableName in self.DB.keys()):
            self.createTable(tableName)

        createEntity(self, tableName, data)
    
    def validateQuery(self, tableName:str, id:str) -> list:
        for entity in self.DB[tableName]:
            # print(entity)
            if( id == entity['_id']):
                return [True,entity]

        # if no such id was found
        print('no such data exist 😑')
        return [False, None]

    def deleteEntity(self, tableName:str, id:str) -> bool:
        validEntity = self.validateQuery(self,tableName, id)
        if(validEntity[0]):
            self.DB[tableName].remove(validEntity[1])
            # for updateEntity() => (i know its not good practice for methods to depend each other)
            return True
            
    def updateEntity(self, tableName:str, id:str, query:dict) -> None:
        # UPDATE can be combination of DELETE and CREATE 
        deletedEntity = self.deleteEntity(self, tableName, id)
        if(deletedEntity):
            createEntity(self, tableName, query)

            
    
    def getAll(self, tableName:str) -> list:
        # returns a list
        return self.DB[tableName] 

class Page():
    def __init__(self, title, func = []):
        self.func = func
        self.title = title

    def render(self, nav:str):
        print("\n\nyou are in {} Page 😁\n".format(self.title))
        print(nav, '\n')

        for i in self.func : 
            print('- ',i)
        # for chaining methods
        # print('\n\n', self, '\n\n')
        return self
        
    
    def showItems(self):
        return self
    

class GeoPage(Page):
    def __init__(self, title, func = []):
        super().__init__(title, func)

    
    def showItems(self, db:list):
        print("=" * 20)
        for i in db:
            print(i['name'])

class Navigator():
    def __init__(self) -> None:
        self.nav = []
    
    def addNav(self, endPoint:str) -> list:
        self.nav.append(endPoint)

        self.showNav()

    def delNav(self) -> str:
        return self.nav.pop()
    
    def showNav(self) -> list:
        return self.nav
    
    def printNav(self,beginning:str)-> str:
        str = beginning
        for i in self.nav:
            str += f' -> {i}'
        
        return str
# for adding new logics/methods (open/close)
class Logic():
    def __init__(self) -> None:
        self.methods = {}

    def augment(self, data:dict) -> dict :
        if (not data):
            return
        
        # get first element of dict
        key = [*data.keys()][0]
        value = [*data.values()][0]
        def check():
            pass
        if (not type(value) is type(check)):
            print('value of dict must be of type function !')
            return
        
        # insert new method to self.methods
        self.methods.update({key : value})
        return self.methods

    def call(self, name:str, opt:dict = {}) -> None:

        func = self.methods[name]
        
        if (not func):
            print('no such method exist')
            return
        
        func(opt)

    def remove(self, name:str) -> None:
        if (not self.methods[name]):
            print('no such method exist')
            return
        self.methods.pop(name)

# ================ create & insert data to DB ===================
db = ShyDB()
db.createSchema('street',{'name' : str, 'city' : str})
db.createTable('street')
db.createSchema('city',{'name' : str, 'country' : str})
db.createTable('city')
db.addEntity('city', {'name':'karaj', 'country':'IR'})
db.addEntity('city', {'name':'tehran', 'country':'IR'})
db.addEntity('city', {'name':'texas', 'country':'US'})
db.addEntity('street', {'name':'flk-13', 'city':'krj'})
db.addEntity('street', {'name':'hemmat', 'city':'teh'})
db.addEntity('street', {'name':'us-street', 'city':'LA'})
# ===============================================================

# ================ create & insert methods ===================
def add(opt:dict) -> None:
    dic = inputToDict()
    tableName = opt['navbar'].showNav()[-1]
    opt['database'].addEntity(tableName, dic)
    data = opt['database'].getAll(tableName)
    opt['page'].render(opt['navbar'].printNav('Home')).showItems(data)

def show(opt:dict):
    print(opt)
    opt['navbar'].addNav(opt['input'])
    tableName = opt['navbar'].showNav()[-1]
    data = opt['database'].getAll(tableName)
    opt['page'].render(opt['navbar'].printNav('home')).showItems(data)

def back(opt:dict):
    opt['navbar'].delNav()
    opt['page'].render(opt['navbar'].printNav('Home'))

logic = Logic()
logic.augment({'add' : add})
logic.augment({'city' : show})
logic.augment({'street' : show})
logic.augment({'back' : back})

# ===============================================================

''' Global variables '''

main = Page('main',[*db.DB.keys(), "exit"])
sub = GeoPage('sub', ['add','back'])
nav = Navigator()

# nav.addNav('street')
main.render(nav.printNav('homy')).showItems()

while(True):
    x = input('choose one of the above :👀\n')
    if x == 'exit':
        break

    elif x == 'back' and nav.showNav():
        logic.call(x,{
        'database' : db,
        'navbar' : nav,
        'page' : main,
        'input' : x
    })
        

    else:
        logic.call(x,{
            'database' : db,
        'navbar' : nav,
        'page' : sub,
        'input' : x
        })

