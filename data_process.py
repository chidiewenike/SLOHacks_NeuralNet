import firebase_admin
import datetime
from time import sleep
from firebase_admin import credentials
from firebase_admin import firestore
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
day = {}
day["SUNDAY"] = 0
day["MONDAY"] = 1
day["TUESDAY"] = 2
day["WEDNESAY"] = 3
day["THURSDAY"] = 4
day["FRIDAY"] = 5
day["SATURDAY"] = 6

def build_model(sample_size):
  model = keras.Sequential([
    keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(1,)),
    keras.layers.Dense(64, activation=keras.activations.linear),
    keras.layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['accuracy'])
  return model

cred = credentials.Certificate('pH_cred.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

collection = 0
day_set = []
time_set = []
output_set = []
training_samples = []
out = []
for i in range (20):
    count = 0
    collection += 1
    # docs = db.collection(u'parking_locations_count').document(u'R2').collection(str(collection)).get()#getCollections()#.document(u'FRIDAY 0800').get()

    # for doc in docs:
    #     curr_sample = doc.to_dict()
    #     output_set.append(int(curr_sample["count"]))
    #     time_set.append(int(curr_sample["time"]))        

    docs = db.collection(u'parking_locations_count').document(u'R3').collection(str(collection)).get()#getCollections()#.document(u'FRIDAY 0800').get()

    for doc in docs:
        curr_sample = doc.to_dict()
        output_set.append(int(curr_sample["count"]))
        time_set.append(int(curr_sample["time"]))

    # docs = db.collection(u'parking_locations_count').document(u'R4').collection(str(collection)).get()#getCollections()#.document(u'FRIDAY 0800').get()

    # for doc in docs:
    #     curr_sample = doc.to_dict()
    #     output_set.append(int(curr_sample["count"]))
    #     time_set.append(int(curr_sample["time"]))


# for i in range(output_set):
#     count = 0



print(output_set)
print(time_set)
training_samples.append(time_set)
# training_samples.append(day_set)
training_samples = np.array(training_samples)
output_set = np.array(output_set)
training_samples = training_samples.transpose()
model = build_model(len(training_samples))
history = model.fit(training_samples, output_set , epochs=100)

dirList = os.listdir()

count = 0

inDir = False

while not(inDir):

    count+=1

    modelStorage1 = "model" + "_" + str(count) + ".h5" 

    inDir = True

    for file in dirList:

        if modelStorage1 in file:

            inDir = False


# frozen_graph = freeze_session(K.get_session(),
#                               output_names=[out.op.name for out in model.outputs]) 

# tf.train.write_graph(frozen_graph, "my_model.pb", as_text=False)

model.summary()

print("Model1 saved: " + modelStorage1)

model.save(modelStorage1)
min = 0
hour = 0
num = []
num_str = []
for i in range(288):
    min += 5

    if (min == 60):
        hour += 1
        min = 0

        if (hour == 24):
            hour = 0
    num.append(int(str(hour+100)[1:] + str(min+100)[1:]))
    num_str.append((str(hour+100)[1:] + str(min+100)[1:]))

test_predictions = model.predict(num).flatten()
print(test_predictions)
print(num)
plt.scatter(num,test_predictions,s=0.5)
plt.ylabel('Spots Taken')
plt.xlabel('Time (24 Hour Time)')
plt.title('Neural Network Prediction')
plt.show()
