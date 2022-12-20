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
    


# factory method
class ShyQuery():
    def __init__(self) -> None:
        pass
        

    def validateQuery(self, database:ShyDB, tableName:str, id:str) -> list:
        for entity in database.DB[tableName]:
            # print(entity)
            if( id == entity['_id']):
                return [True,entity]

        # if no such id was found
        print('no such data exist 😑')
        return [False, None]

    def deleteEntity(self, database:ShyDB, tableName:str, id:str) -> bool:
        validEntity = self.validateQuery(database,tableName, id)
        if(validEntity[0]):
            database.DB[tableName].remove(validEntity[1])
            # for updateEntity() => (i know its not good practice for methods to depend each other)
            return True
            
    def updateEntity(self, database:ShyDB, tableName:str, id:str, query:dict) -> None:
        # UPDATE can be combination of DELETE and CREATE 
        deletedEntity = self.deleteEntity(database, tableName, id)
        if(deletedEntity):
            createEntity(database, tableName, query)

            
    
    def getAll(self, database:ShyDB, tableName:str) -> list:
        # returns a list
        return database.DB[tableName]

class Page():
    def __init__(self, title, func = []):
        self.func = func
        self.title = title

    def render(self):
        print("you are in {} Page 😁".format(self.title))
        for i in self.func : 
            print('- ',i)
        # for chaining methods
        return self
    
    def showAll(self):
        return self
    

class GeoPage(Page):
    def __init__(self, title, func = [], items = []):
        super().__init__(title, func)
        self.items = items

    
    def showAll(self):
        print("=" * 20)
        for i in self.items:
            print(i)

# like a DO-WHILE where DO => __init__ & WHILE => goto()
class Renderer():
    def __init__(self, page:Page) -> None:
        self.page = page.render().showAll()
        self.valid = False

    def goto(self, page) -> bool:
        self.userInput = input('choose one of the above :')

        if (self.userInput in self.page.func and self.page.title == 'main'):
            if self.userInput == 'exit':
                # exit program
                return True
            page.render().showAll()

        if(self.userInput in page.func and page.title == 'sub'):
            if self.userInput == 'back':
                self.valid = False
                self.page.render().showAll()
            
            if self.userInput == 'add':
                token = validate()
                return token

# ================ create & insert data to DB ===================
q = ShyQuery()
db = ShyDB()
db.createSchema('street',{'name' : str, 'city' : str})
db.createTable('street')
db.createSchema('city',{'name' : str, 'country' : str})
db.createTable('city')
db.addEntity('city', {'name':'karaj', 'country':'IR'})
db.addEntity('city', {'name':'tehran', 'country':'IR'})
db.addEntity('city', {'name':'texas', 'country':'US'})
db.addEntity('street', {'name':'flk-13', 'country':'krj'})
db.addEntity('street', {'name':'hemmat', 'country':'teh'})
db.addEntity('street', {'name':'us-street', 'country':'LA'})
# ===============================================================

# Global variables

city = q.getAll(db,'city')
street = q.getAll(db,'street')

main = Page('main',[*db.DB.keys(), "exit"])

sub = GeoPage('sub', ['add','back'],[])

r = Renderer(main)

while(True):
    done = r.goto(sub)
    if (done):
        break


# while(True):

#     x = input("choose one of the above: \n")
    
#     if (x == "exit"):
#         break
    
#     # I know its bad code but at least you dont run into a bug :) 
#     elif(x == "add" or x == "back" or x == "city" or x == "street"):
#         if (not token):
#             token = validate()
        
#         if(token):
#             if (x == "city"):
#                 a2 = GeoPage('sub-page',["add", "back"], city)
#                 print(a2)

#             if (x == "street"):
#                 a2 = GeoPage('sub-page', ["add", "back"], street)
#                 print(a2)

#             if (x == "add"):
#                 query = input("pls enter a complete query: \n")
#                 db.addEntity(x,query)
#                 print(a2)
            
#             if (x == "back"):
#                 token = False
#                 print(a)
            
#             else:
#                 pass
#     else:
#         pass
