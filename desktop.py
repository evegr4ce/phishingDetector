import tkinter as tk
import requests
from bs4 import BeautifulSoup
import urlExtraction
import pickle
import pandas as pd
import URLFeatureExtraction

root = tk.Tk()

#making the tkinter screen
root.geometry("500x500")
root.title("Phishing detector")


def fetch_data():
    url = url_entry.get()

    feature_names = ['URL', 'HasAt', 'URLLen', 'URLDepth', 'Redirection', 'domainType', 'ShortURL',
                      'OddChar', 'Prefix/Suffix', 'numPer', 'HasIP', 'Web_Traffic', 'DomainAge',
                      'Text', 'iFrame', 'mouseOver', 'rightClick', 'Forwarding', 'Label']

    if url:
        # response = requests.get(url)
        # if response.status_code == 200:# checking the status code
        extracted_data = urlExtraction.featureExtraction(url)#extract the data
        data = {name:ft for name,ft in zip(feature_names, extracted_data)}
        features = pd.DataFrame(data, columns=feature_names, index=[0])
        x = features.iloc[:, 1:-2]
        print(x)
        x = x.reset_index(drop=True)

        with open("mlpModel.pkl", "rb") as f:
            model = pickle.load(f)

        prediction = model.predict(x)
        print(prediction[0])
        display_data(prediction[0])

        # else:
        #     display_data("Error: unable to get data")
    else:
        display_data("please enter a URL")


#replacing old content with new content
def display_data(data):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, data)



#setting up the tkinter page
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

#adding a button to check the url
button = tk.Button(root, text =" Check URL", command=fetch_data)
button.pack(pady =10)


result_text = tk.Text(root, wrap= tk.WORD, height=10, width=60)
result_text.pack(padx=10, pady=5)


root.mainloop()
