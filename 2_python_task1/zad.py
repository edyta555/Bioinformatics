def read_reads(plik1='odczytyA.txt'):
#zwraca odczyty z pliku w postaci listy elementow
#[nr chromosomu,poczatek odczytu, dlugosc odczytu]
    D=[]
    f=open(plik1,'r')
    for line in f.readlines():
        t=line.split()  
        D.append(map(int,t))
    f.close()
    return D

def compute_coverage(odczyty):
#oblicza pokrycie (Chr, Covs) na podstawie listy odczytow, gdzie
#Chr to lista numerow chromosomow, a Covs to lista list o elementach [pokrycie,poczatek pokrycia, koniec pokrycia]
#odpowiadajacych kolejnym pokryciom na danym chromosomie
    Chr,M1,M2=helper_lists(odczyty) ## zwraca (Chr,M1, M2), gdzie Chr-lista nr chrom,M1-lista poczatkow odczytow, M2-lista koncow posortowana
    Covs=[]
    for i in range(len(Chr)):
        Covs.append(compute_coverage_chrom(M1[i],M2[i]))
    return Chr, Covs

def write_coverage(pokrycie, plik_wyjsciowy='pokryciaA.txt'):
#wypisuje pokrycie do pliku
    Chr, Covs=pokrycie
    f=open(plik_wyjsciowy,'w')
    for i in range(len(Chr)):
        for c in Covs[i]:
            f.write(str(c[0]) +' '+ str(Chr[i]) + ' ' +str(c[1])+ ' ' + str(c[2])+'\n')


def multiply_coverage(plikA='odczytyA.txt', plikB='odczytyB.txt', plik_wyjsciowy='iloczyn_pokryc.txt'):
#wypisuje do pliku iloczyn pokryc z zadanych plikow
    Chr1, Covs1=compute_coverage(read_reads(plikA))
    Chr2, Covs2=compute_coverage(read_reads(plikB))
    write_coverage(multiply_coverage_data(Chr1, Covs1, Chr2, Covs2), plik_wyjsciowy)

def multiply_coverage_data(Chr1, Covs1, Chr2, Covs2):
#oblicza iloczyn pokryc 
    Chr3=[]
    Covs3=[]
    i=0
    j=0
    while (i <len(Chr1)) and (j <len(Chr2)):
        if Chr1[i]==Chr2[j]:
            mult=Chr_multiply_coverage(Covs1[i], Covs2[j])
            if len(mult)>0:
                Chr3.append(Chr1[i])
                Covs3.append(mult)
            i=i+1
            j=j+1
        elif Chr1[i]<Chr2[j]:
            i=i+1
        else: # Chr1[i]>Chr2[j]
            j=j+1
    return Chr3, Covs3

def Chr_multiply_coverage(Cov1, Cov2):
#zwraca liste elementow [wysokosc pokrycia,poczatek pokrycia, koniec pokrycia] odpowiadajaca iloczynowi zadanych jako takie listy pokryc z 2 chromosomow
    i=0
    j=0
    l0=0
    Cov3=[]
    while (i < len(Cov1)) and (j < len(Cov2)):
        if Cov1[i][2] <= Cov2[j][1]:
            i=i+1
        elif Cov1[i][1] >= Cov2[j][2]:
            j=j+1
        else:
            l=Cov1[i][0]*Cov2[j][0]
            m1=max(Cov1[i][1],Cov2[j][1]) 
            m2=min(Cov1[i][2],Cov2[j][2])  
            cont=False #czy kontynuowac poprzednie pokrycie
            if (len(Cov3)>0): 
                if Cov3[-1][0]==l and Cov3[-1][2]==m1:
                    cont=True        
            if cont:
                Cov3[-1][2]=m2
            else:  
                Cov3.append([l,m1,m2])
            if Cov1[i][2]<Cov2[j][2]:
                i=i+1
            elif Cov1[i][2]>Cov2[j][2]:
                j=j+1
            else: #Covs2[i][2]==Covs1[j][2]
                i=i+1
                j=j+1
    return Cov3

def helper_lists(odczyty):
# zwraca (Chr,M1, M2), gdzie Chr to lista numerow chromosomow, M1 to lista o elementach [xi1,xi2,xi3,...], gdzie xij to poczatek j-tego odczytu i-tego chromosomu, a
# M2 to lista o elementach [yi1,yi2,yi3,...], gdzie yij to j-ty rosnaco koniec odczytu i-tego chromosomu
    Chr=[] 
    L1=[] 
    L2=[] 
    M1=[] 
    M2=[] 
    Chr.append(odczyty[0][0])
    for x in odczyty:
        if Chr[-1]==x[0]:  
            L1.append(x[1])
            L2.append(x[1]+x[2])
        else:
            Chr.append(x[0])
            M1.append(L1)
            L2.sort()
            M2.append(L2)
            L1=[x[1]]
            L2=[x[1]+x[2]]
    M1.append(L1)
    L2.sort()
    M2.append(L2)              
    return Chr,M1,M2
   
def compute_coverage_chrom(x,y):
#liczy pokrycie w chromosomie na podstawie list poczatkow i koncow odczytow
    C=[]
    h=0 #wysokosc pokrycia
    i=0 
    j=0
    s=0 #poczatek pokrycia
    while i<len(x):
        if x[i]==y[j]:
            i,j=skip_equal(i,j,x,y)
        elif x[i]<y[j]:
            s,h,i = cover_up(i,x,s,h,C)
        else:
            s,h,j = cover_down(j,y,s,h,C)
    while j<len(y):
        s,h,j=cover_down(j,y,s,h,C)
    return C

def cover_up(i,x,s,h,C):
#dodaje pokrycie (jesli h>0) i idzie w gore
    if h>0:
        C.append([h,s,x[i]])
    s=x[i]
    p=i
    i=przejdz(i,x);
    h=h+i-p
    return s,h,i

def cover_down(j,y,s,h,C):
#dodaje pokrycie i schodzi w dol
    C.append([h,s,y[j]])
    p=j
    j = przejdz(j,y)
    s=y[p]                      
    h=h-(j-p);
    return s, h, j

def skip_equal(i,j,x,y):
# przesuwa indeksy 'i' i 'j' dopoki x[i]=y[j]
    dalej=True 
    while i<len(x) and dalej:
        if x[i]==y[j]:
            i=i+1;
            j=j+1;
        else:
            dalej=False 
    return i,j

def przejdz(i,x):
# ustawia i zaraz za blokiem x-ow o wartosci x[i]
    p=i; 
    i=i+1 
    dalej=True 
    while i<len(x) and dalej:
        if x[i]==x[p]:
            i=i+1;
        else:
            dalej=False
    return i
