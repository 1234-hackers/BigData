from matplotlib import pyplot as plt
import pandas as pd

import pyploy.express as pE



def dummy():

    df = pd.DataFrame({'a':[1,2,3,4,5], 'b':[10,5,2,4,5]})

    imz = plt.plot(df)

    plt.show()

def real():
    df = pd.read_json("jsonData/20230615 194837504100.json")
    dts = df.columns

    am  = df['amount']
    plt.ylabel('amount')
    plt.xlabel('people')
    plt.plot(am)

    plt.show()

    print(dts)








real()
#dummy()