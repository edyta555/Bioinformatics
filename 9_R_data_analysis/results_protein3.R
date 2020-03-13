load("/home/tomasz/Pulpit/data science/szczurek/zadzalR/protein.RData")
X=data.train[,1:dim(data.train)[2]-1]
any(duplicated(t(X)))
M=cor(X)
maxCor=0
for(i in 1:dim(M)[1])  # for each row
{
  M[i,i]=0
  maxCor =max(abs(M[i,which.max(M[i,])]),maxCor)
}
maxCor
#[1] 0.1479086

#---forward stepwise regr
library(leaps)
  predict.regsubsets = function(object, newdata, id,...){
    form = as.formula(object$call[[2]])
    mat=model.matrix(form,newdata)
    coefi=coef(object,id=id)
    xvars=names(coefi)
    mat[,xvars]%*%coefi
  }

#  --- cross-validation
  k=10
  l=10
  set.seed(1)
  folds=sample(1:k,nrow(data.train),replace=TRUE)
  cv.errors=matrix(NA,k,l,dimnames=list(NULL,paste(1:l)))
  for(j in 1:k){
    fwd.fit=regsubsets(Y~.,data=data.train[folds!=j,],nvmax=l,method="forward")
    for(i in 1:l){
      pred=predict(fwd.fit,data.train[folds==j,],id=i)
      cv.errors[j,i]=mean((data.train$Y[folds==j]-pred)^2)
    }
  }

  mean.cv.errors=apply(cv.errors,2,mean)
  mean.cv.errors
  mean.cv.errors[which.min(mean.cv.errors[1:l])]
  5 
  1.081719 
  regfit.best = regsubsets(Y~., data = data.train , nvmax =10, method="forward")
  coef(regfit.best,5)
  
#--ridge
  # Chapter 6 Lab 2: Ridge Regression and the Lasso
#load("/home/tomasz/Pulpit/data science/szczurek/zadzalR/protein.RData")
x=model.matrix(Y~.,data.train)[,-1]
y=data.train$Y
library(glmnet)
grid=10^seq(10,-2,length=100)
set.seed(1)
cv.out=cv.glmnet(x,y,alpha=0,lambda=grid)
plot(cv.out)
bestlam=cv.out$lambda.min
bestlam
#0.6579332
cv.out$cvm[85]
#412.3325

#lasso
set.seed(1)
cv.out_lasso=cv.glmnet(x,y,alpha=1,lambda=grid)
plot(cv.out_lasso)
bestlam=cv.out_lasso$lambda.min
bestlam
#0.07054802
cv.out_lasso$cvm[93]
#1.128402

out_lasso = glmnet(x,y,alpha=1,lambda=grid)
lasso.coef=predict(out_lasso,type="coefficients",s=bestlam)
lasso.coef[lasso.coef!=0]
