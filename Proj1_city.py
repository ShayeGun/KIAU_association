class Page():
    def __init__(self,title,arr = [],msg = ''):
        self.arr = arr
        self.msg = msg
        self.title = title

    def __str__(self):
        string = "you are in {} Page 😁\n".format(self.title)
        for i in range(len(self.arr)):
            string += "{}) {}\n".format(i+1,self.arr[i])
        
        string += self.msg
        
        return string

class GeoPage(Page):
    def __init__(self, title, arr,arr2):
        super().__init__(title, arr)
        self.arr2 = arr2

    def add(self,name):
        self.arr2.append(name)
        return

    def __str__(self):
        string = super().__str__() + "=" * 20 + "\n"

        for i in range(len(self.arr2)):
            string += "{}\n".format(self.arr2[i])

        return string

def validate(page, username, password):
    if(username == "shy" and password == "shy"):
        return True
    else:
        page.msg = "you're not shy honey🙃"
        print(page)
        page.msg = ''
        return False

a = Page('main',["city", "street", "exit"])
print(a)

# Global variables
username = ''
password = ''
token = False
city = ["c1","c2","c3"]
street = ["s1","s2","s3"]

while(True):

    x = input("choose one of the above: \n")
    
    if (x == "exit"):
        break
    
    # I know its bad code but at least you dont run into a bug :) 
    elif(x == "add" or x == "back" or x == "city" or x == "street"):
        if (not token):
            username = input("plz enter my username :\n")
            password = input("plz enter my password : \n")
            token = validate(a, username, password)
        
        if(token):
            if (x == "city"):
                a2 = GeoPage('sub-page',["add", "back"], city)
                print(a2)

            if (x == "street"):
                a2 = GeoPage('sub-page', ["add", "back"], street)
                print(a2)

            if (x == "add"):
                name = input("pls enter a name: \n")
                a2.add(name)
                print(a2)
            
            if (x == "back"):
                token = False
                print(a)
            
            else:
                pass
    else:
        pass

    

