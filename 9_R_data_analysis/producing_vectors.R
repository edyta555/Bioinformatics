#protein.RData
load("/home/tomasz/Pulpit/data science/szczurek/zadzalR/protein.RData")
library(leaps)
regfit.best = regsubsets(Y~., data = data.train , nvmax =10, method="forward")
coef5=coef(regfit.best,5)

testframe=as.data.frame(data.test)
colnames(testframe) <- names(data.train[,1:(dim(data.train)[2]-1)])
test.mat = model.matrix(~., data = testframe)
pred.protein=test.mat[,names(coef5)]%*%coef5

#cancer.RData
load("/home/tomasz/Pulpit/data science/szczurek/zadzalR/results_cancer2.RData")
library(MASS)

V100=cbind(Z100, data.train$Y)
colnames(V100)[dim(V100)[2]]=names(data.train)[dim(data.train)[2]]
test100 = data.test[,names(Z100)]
test100[1:dim(test100)[1],1:dim(test100)[2]]=sapply(test100,as.numeric)
lda.fit.100 = lda(Y~., data=V100)
res.100 = predict(lda.fit.100, test100)
pred.cancer.100=res.100$class

library(randomForest)
V50=cbind(Z50, data.train$Y)
colnames(V50)[dim(V50)[2]]=names(data.train)[dim(data.train)[2]]
test50 = data.test[,names(Z50)]
test50[1:dim(test50)[1],1:dim(test50)[2]]=sapply(test50,as.numeric)

bag.V50 = randomForest(Y~.,data=V50,mtry=7,importance=TRUE)
yhat.bag = predict(bag.V50 , newdata=test50)
pred.cancer.50=yhat.bag

save(pred.protein, pred.cancer.50, pred.cancer.100, file="Michalska.RData")