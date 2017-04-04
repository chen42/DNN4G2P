from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras import regularizers
from keras.utils import np_utils
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from keras.preprocessing.image import ImageDataGenerator
import random
import sys

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

def augment(data):
    sim=np.copy(data) # the simulation data is a  copy of the original data 
    print ("original data copied")
    print (sim.shape)
    nb_features=data.shape[1]
    nb_samples=data.shape[0]
    nb_swap=int(nb_features*0.1) # swap 20% of the SNPs with another sample
    for j in range(nb_samples):
        feature2swap=[]
        sample2swap=random.randrange(nb_samples) #  
        for i in range(nb_swap):
            feature2swap.append(random.randrange(1,nb_features))
        sim[j][feature2swap]= data[sample2swap][feature2swap] 
    print ("data swap done")
    return sim


dataset = pd.read_csv("./chr1_all.csv", delimiter=",",dtype='float', na_filter=True)
dataset = dataset.values
dataset = dataset.astype(dtype="int")
print ("data set shape" + str(dataset.shape))

genotype_cnt=dataset.shape[1]-1

# split into input (X) and output (Y) variables
X = dataset[:,1:genotype_cnt]
Y = dataset[:,0]

# split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)


augmentData=0
if augmentData:
    print (X_train.shape)
    aug1=augment(X_train)
    aug2=augment(X_train)
    aug3=augment(X_train)
    X0=np.append(X_train, aug1, axis=0)
    X1=np.append(X0, aug2, axis=0)
    X_train=np.append(X1, aug3, axis=0)
    print (X_train.shape)
    y0=np.append(y_train,y_train)
    y1=np.append(y0,y_train)
    y_train=np.append(y1,y_train)

y_train=np_utils.to_categorical(y_train)
y_test =np_utils.to_categorical(y_test)

print ("Data loaded\n")
model = Sequential()
#model.add(Dropout(input_shape=(genotype_cnt-1,), rate=0.30))
model.add(Dense(units=200, input_dim=genotype_cnt-1,  kernel_initializer='uniform', activation='relu'))

model.add(Dense(units=200, kernel_initializer='uniform', activation='relu', kernel_regularizer=regularizers.l1(0.1)))
model.add(Dense(units=200, kernel_initializer='uniform', activation='relu', kernel_regularizer=regularizers.l1(0.1)))
model.add(Dense(units=200, kernel_initializer='uniform', activation='relu', kernel_regularizer=regularizers.l1(0.1)))
#model.add(Dropout(0.30))
model.add(Dense(units=5, kernel_initializer='uniform', activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit model
model.fit(X_train, y_train, epochs=100, batch_size=400)

#evaluate the model
scores = model.evaluate(X_test, y_test)
print ("\nTest set:\n")
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))




