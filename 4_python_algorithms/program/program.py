def ordl(l):
    return ord(l)-97
def chrl(n):
    return chr(n+97)
ileL=26 

class Tree:
    def __init__(self,node=None):
        self.root=node

class Node:
    def __init__(self):
        self.jest_slowo=False
        self.ile_potomkow=0
        self.children=[]
        for i in range(0,ileL):
            self.children.append(None)

    def insert(self,s):
    #zwraca informacje czy wstawiane slowo jest nowe w slowniku
        ret=False
        if self.children[ordl(s[0])]==None:
            self.children[ordl(s[0])]=Node()
            ret=True

        if len(s)==1:
            if not self.children[ordl(s[0])].jest_slowo:
                self.children[ordl(s[0])].jest_slowo=True
                ret=True
        else:
            ret=self.children[ordl(s[0])].insert(s[1:])
        if ret:
            self.ile_potomkow+=1;
        return ret
    
    def printAscR(self,pocz):
        if self.jest_slowo:
            print pocz
        for i in range(0,ileL):
            if self.children[i]!=None:
                self.children[i].printAscR(pocz + chrl(i))

    def printAsc(self):
        self.printAscR('')

    def printDescR(self,pocz):
        for i in range(0,ileL):
            j=ileL-i-1
            if self.children[j]!=None:
                self.children[j].printDescR(pocz + chrl(j))
        if self.jest_slowo:
            print pocz

    def printDesc(self):
        self.printDescR('')

    def findByWord(self,s):
        j=ordl(s[0])
        if self.children[j]==None:
            return None 
        else: 
            if len(s)==1:
                if  self.children[j].jest_slowo: 
                    ktorewpod=1
                else:
                    return None
            else:
                ktorewpod=self.children[j].findByWord(s[1:])
            if ktorewpod==None: 
                return None 
            ilewcz=self.jest_slowo + ktorewpod
            for i in range(0,j):
                if (self.children[i]!=None):
                    ilewcz=ilewcz+ self.children[i].ile_potomkow +self.children[i].jest_slowo
        return ilewcz

    def findByPref(self,s):
        j=ordl(s[0])
        if self.children[j]==None:
            return 0
        else: 
            if len(s)==1:
                return self.children[j].ile_potomkow + self.children[j].jest_slowo
            else:
                return self.children[j].findByPref(s[1:])

    def findByNumberR(self,k):
    #znajdz k-te slowo sposrod potomkow danego wezla, zakladajac ze takie slowo wystepuje
        i=-1
        ile=0
        ile_wcz=0
        while (ile<k):
            i=i+1;
            if (self.children[i]!=None):
                ile_wcz=ile+self.children[i].jest_slowo
                ile=ile_wcz + self.children[i].ile_potomkow
        if (k==ile_wcz): #i-te dziecko to koniec szukanego slowa
            return chrl(i)
        else:
            return chrl(i)+self.children[i].findByNumberR(k-ile_wcz)

    def findByNumber(self,k):
    #znajdz k-te slowo sposrod potomkow danego wezla
        if (0>=k) or (k> self.ile_potomkow):
            return None
        else:#k-te slowo wystepuje
            return self.findByNumberR(k)

    def remove(self,s):
    #zwraca true jesli usunal cos w poddrzewie
        j=ordl(s[0])
        if self.children[j]==None:
            return False
        else:
            if len(s)==1:
                if (self.children[j].jest_slowo):
                    self.children[j].jest_slowo=False
                    ret=True
                else: 
                    ret=False  
            else:
                ret=self.children[j].remove(s[1:])
            if ret:
                self.ile_potomkow-=1;                                                  
                if self.children[j].ile_potomkow + self.children[j].jest_slowo==0:
                    self.children[j]=None
            return ret

if __name__ == "__main__":
    import sys
    koniec=False
    r=Node()
    while not koniec:
        l=sys.stdin.readline()
        arg=l.split()
        l=arg[0]
        if l=='k': 
            koniec=True
        elif l=='i':
            r.insert(arg[1])
        elif l=='r':
            r.remove(arg[1])
        elif l=='f':
            n=r.findByWord(arg[1])
            if n==None:
                print 0
            else:
                print n
        elif l=='p':
            print r.findByPref(arg[1])
        elif l=='a': 
            r.printAsc()
        elif l=='d': 
            r.printDesc()
        elif l=='n': 
            print r.findByNumber(int(arg[1]))

