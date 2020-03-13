load("/home/tomasz/Pulpit/data science/szczurek/zadzalR/cancer.RData")
X=data.train[,1:(dim(data.train)[2]-1)]
#for(i in 1:dim(X)[1]){
#for(j in 1:dim(X)[2]){
#if(X[i,j]==TRUE){
#  X[i,j]=1
#}
#  if(X[i,j]==FALSE){
#    X[i,j]=0
#}
#}
#}
X[1:dim(X)[1],1:dim(X)[2]]=sapply(X,as.numeric)
#X=sapply(X,as.numeric)
b=duplicated(t(X))
v=NULL
for(i in 1:dim(X)[2]){if(!b[i]){v=c(v,i)}}
Z = X[,v]
for(i in 1:(dim(Z)[2]-1)){if(sum(Z[,i])==0){print(i)}}
Z=Z[,-1]
M=cor(Z)

maxCor=0
for(i in 1:dim(M)[1]){
  M[i,i]=0
  j=which.max(M[i,])
  c = abs(M[i,j])
  #if(c >0.99){print(c);print(i);print(j)}
  maxCor =max(c,maxCor)
}
print(maxCor)
V=cbind(Z, data.train$Y)
colnames(V)[dim(V)[2]]=names(data.train)[dim(data.train)[2]]
library("subselect")
res=trim.matrix(cor(Z),tolval=e-3)
Z2=Z[,-res$numbers.discarded]
dim(Z2)
Z2Hmat <- ldaHmat(Z2,V$Y)
resAnneal=anneal(Z2Hmat$mat,kmin=100,kmax=100,H=Z2Hmat$H, force=TRUE)
Z100=Z2[,resAnneal$subsets]
resAnneal50=anneal(Z2Hmat$mat,kmin=50,kmax=50,H=Z2Hmat$H, force=TRUE)
Z50=Z2[,resAnneal50$subsets]

#load("/home/tomasz/Pulpit/data science/szczurek/zadzalR/results_cancer2.RData")
library(MASS)

V50=cbind(Z50, data.train$Y)
colnames(V50)[dim(V50)[2]]=names(data.train)[dim(data.train)[2]]

cvlda = function(Vn,...){
k=10
v=NULL
set.seed(1)
folds=sample(1:k,nrow(Vn),replace=TRUE)
for(j in 1:k){
  lda.fitn = lda(Y~. , data =  Vn[folds!=j,])
  Vntest = Vn[folds==j,]
  lda.predn = predict(lda.fitn, Vntest)
  #lda.pred50$class
  v=c(v,mean(Vntest$Y==lda.predn$class))
}
mean(v)
}
cvlda(V50)

V100=cbind(Z100, data.train$Y)
colnames(V100)[dim(V100)[2]]=names(data.train)[dim(data.train)[2]]
cvlda(V100)
#[1] 0.6053063

#KNN
#knn . pred = knn ( train .X , test .X , train . Direction , k =3)
library(class)
cvknn = function(Vn,Zn,pk){
  k=10
  v=NULL
  set.seed(1)
  folds=sample(1:k,nrow(Vn),replace=TRUE)
  for(j in 1:k){
    knn.predn = knn(Zn[folds!=j,] , Zn[folds==j,] ,  Vn$Y[folds!=j], k =pk)
    Vntest = Vn[folds==j,]
   
    #lda.pred50$class
    v=c(v,mean(Vntest$Y==knn.predn))
  }
  mean(v)
}
cvknn(V50,Z50,3)
#[1] 0.469989
cvknn(V50,Z50,2)
#[1] 0.4524918
cvknn(V50,Z50,4)
#0.4764715
cvknn(V50,Z50,5)
#0.4773509
cvknn(V50,Z50,6)
#0.4807683
cvknn(V50,Z50,7)
#0.481767
cvknn(V50,Z50,8)
#0.4783396

cvknn(V100,Z100,5)
# 0.4903822
cvknn(V100,Z100,6)
# 0.4915134
cvknn(V100,Z100,7)
#0.4898919
#trees
library(randomForest)

cvrf = function(Vn,m,...){
  k=10
  v=NULL
  set.seed(1)
  folds=sample(1:k,nrow(Vn),replace=TRUE)
  for(j in 1:k){
    print(j)
    bag.Vn = randomForest(Y~.,data=Vn[folds!=j,],mtry=m,importance=TRUE)
    yhat.bag = predict(bag.Vn , newdata=Vn[folds == j ,])
    v=c(v,mean(mean(yhat.bag==Vn$Y[folds == j])))
  }
  mean(v)
}
cvrf(V50,7)
# 0.5361706
cvrf(V100,10)
#0.5873933
