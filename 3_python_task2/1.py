from turtle import *
import copy
from math import*
import random


def wczytaj(plik1='1.txt'):
    A=[]
    f=open(plik1,'r')
    for line in f.readlines():
        t=line.split()  
        A.append(map(float,t))
    f.close()
    return A 


def rysuj_rekurencyjnie(L,n):
    L1=L[0]
    L2=L[1:]
    speed(10)
    clear()
    ht() 
    tracer(0) 
    rysuj2(0,0,0,L1[1],L1[2],L2,n)
    update()


def rysuj_punktowo(L,p):
    x,y,n=L[0][1],L[0][2],int(L[0][0])
    A=L[1:]
    speed(10)
    clear()
    ht()    
    tracer(0)
    tab=[]
    s=0
    for i in range(n):
        s+= A[i][0]*A[i][1]
        tab.append(s)
    for i in range(n):
        tab[i]/=s
    for i in range(p):
        u=random.random()
        l=0
        while u>tab[l]:
            l+=1
        px,py=obroc_wektor(x*A[l][0],y*A[l][1],A[l][4])
        x=px+A[l][2]
        y=py+A[l][3]
        up()
        goto(x,y)
        down()
        dot(1)
    update()


def obroc_wektor(x,y,kat):
    cos_kata=cos(kat*pi/180)
    sin_kata=sin(kat*pi/180)
    return cos_kata*x-sin_kata*y, sin_kata*x+cos_kata*y
  

def rysuj2(x0,y0,kat,a,b,L2,n):
    if n==0:
        up()
        goto(x0,y0)
        down() 
        left(kat)
        for t in range(2):
            forward(a)
            left(90)
            forward(b)
            left(90)
        right(kat)
    else:
        for p in L2: 
            L2pom=copy.deepcopy(L2)
            for pom in L2pom:
                pom[2]*=p[0]
                pom[3]*=p[1]
            x1,y1=obroc_wektor(p[2],p[3],kat)
            rysuj2(x0+x1,y0+y1,kat+p[4],a*p[0],b*p[1],L2pom,n-1)  


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="nazwa pliku z danymi", required=False) 
    parser.add_argument("-n", help="liczba iteracji(dla -t 1-glebokosc rekurencji, -t 2-l.punktow", required=False)
    parser.add_argument("-t", help="1-rysowanie rekurencyjne, 2-rysowanie punktowe", required=False)
    args = parser.parse_args()
    if args.i == None:
        print 'wpisz -i oraz wskaz plik z danymi '
    if args.n == None:
        print 'wpisz -n oraz podaj liczbe iteracji  '
    if args.t != '1' and args.t != '2':
        print 'wpisz -t oraz wybierz rodzaj rysunku:1 lub 2'
    if args.i != None and args.n != None and args.t != None:
        if args.t=='1':
            rysuj_rekurencyjnie(wczytaj(args.i),int(args.n))
        if args.t=='2':
            rysuj_punktowo(wczytaj(args.i),int(args.n))
        raw_input('Wcisnij enter zeby zakonczyc')
   
