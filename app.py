from flask import Flask, render_template
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import accuracy_score

import pandas as pd

import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import csv

app=Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data=pd.read_csv("C:\\Users\\vharikrishnan\\AppData\\Local\\Programs\\Python\\Python36\\dataset.csv")
    f1=open("C:\\Users\\vharikrishnan\\AppData\\Local\\Programs\\Python\\Python36\\FlaskApp\\static\\css\\Mostinterested.csv","w")
    f2=open("C:\\Users\\vharikrishnan\\AppData\\Local\Programs\\Python\\Python36\\FlaskApp\\static\\css\\Interested.csv","w")
    f3=open("C:\\Users\\vharikrishnan\\AppData\\Local\Programs\\Python\\Python36\\FlaskApp\\static\\css\\Notinterested.csv","w")
    f1.write("Company name,Subscription business,Zuora customer,Occurance,Visit Duration,Page Views,demographics\n")
    f2.write("Company name,Subscription business,Zuora customer,Occurance,Visit Duration,Page Views,demographics\n")
    f3.write("Company name,Subscription business,Zuora customer,Occurance,Visit Duration,Page Views,demographics\n")
    not_interested =['Not in vision']
    most_interested =['Ideal Customers']
    interested =['Typical Customers']
    features=["Subscription business","Zuora customer","Occurance","Visit Duration"]
    x=data[features]
    y=data.promotion
    nb_model = GaussianNB()
    nb_model.fit(x, y)
    def Convert(string):
        li = list(string.split(","))
        return li
    preds=[]
    result_record=[]
    with open('C:\\Users\\vharikrishnan\\AppData\\Local\\Programs\\Python\\Python36\\dataset_predict.txt', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            result_record=(f'{row["Subscription business"]},{row["Zuora customer"]},{row["Occurance"]},{row["Visit Duration"]}')
            line_count += 1
            result_record=(Convert(result_record))
            result_record= list(map(int, result_record))
            preds1 = nb_model.predict([result_record])
            print(preds1)
            if preds1 == most_interested :
                f1.write(f'{row["Company name"]},{row["Subscription business"]},{row["Zuora customer"]},{row["Occurance"]},{row["Visit Duration"]},{row["Page Views"]},{row["demographics"]}\n')
            elif preds1 == interested :
                f2.write(f'{row["Company name"]},{row["Subscription business"]},{row["Zuora customer"]},{row["Occurance"]},{row["Visit Duration"]},{row["Page Views"]},{row["demographics"]}\n')
            elif preds1 == not_interested :
                f3.write(f'{row["Company name"]},{row["Subscription business"]},{row["Zuora customer"]},{row["Occurance"]},{row["Visit Duration"]},{row["Page Views"]},{row["demographics"]}\n')
            else :
                x=x+0
            preds.extend(preds1)
        print(f'Processed {line_count} lines.')
    ax=plt.subplots()
    N, bins, patches=plt.hist(preds,edgecolor='white',linewidth=1)
    plt.title('Prediction Results',fontsize=18)
    cmap = plt.get_cmap('jet')
    low = cmap(0.5)
    medium =cmap(0.25)
    high = cmap(0.8)
    for i in range(0,1):
        patches[i].set_facecolor(low)
    for i in range(1,5):    
        patches[i].set_facecolor(medium)
    for i in range(6,len(patches)):
        patches[i].set_facecolor(high)
    handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in [low,medium,high]]
    labels= ["Ideal Customers","Typical Customers", "Not in vision"]
    plt.legend(handles, labels)
    plt.xticks(fontsize=14)  
    plt.yticks(fontsize=14)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    #plt.show()
    plt.savefig("C:\\Users\\vharikrishnan\\AppData\\Local\\Programs\\Python\\Python36\\FlaskApp\\static\\css\\prediction.png")
    f1.close()
    f2.close()
    f3.close()
    return render_template('submit.html')

@app.route('/back', methods=['POST'])
def back():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)


