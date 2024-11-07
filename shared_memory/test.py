from manager import load_data, load_data_and_retrieve,saveFile,retrieveData
import pandas as pd
from io import BytesIO
import time
import matplotlib.pyplot as plt
if __name__=="__main__":
    st=[]
    data = {
        "context": {
            "type": "local",
            # "path": "/home/julio/objects/one/f.txt"
            #"path": "/home/alejandro/documentos/clase/curso.rar"
            "path": "/home/alejandro/documentos/clase/memoria_compartida/data.csv"
            
            # "path": "/home/julio/objects/TESIS.pdf"
        }
    }
    
    response=load_data(data)
    #print(response)
    start_in_memory=time.time()
    r=retrieveData(response["metadata"]["resources"][0]["shm"])
    df = pd.read_csv(BytesIO(r))
    end_in_memory=time.time()
    st_in_memory=end_in_memory-start_in_memory
    st.append(st_in_memory)
    print(df)
    
    start_time_in_hd=time.time()
    df2=pd.read_csv("/home/alejandro/documentos/clase/memoria_compartida/data.csv")
    end_time_in_hd=time.time()
    
    st_in_hd=end_time_in_hd-start_time_in_hd
    st.append(st_in_hd)
    print(df2)
    plt.figure(figsize=(12,8))
    plt.bar(["in memroy","hard disk"],st,)
    plt.xlabel("type")
    plt.ylabel("service time (seg)")
    plt.title("services time")
    
    for i, value in enumerate(st):
        plt.text(i, value + 0.01, f"{value:.2f}", ha='center', va='bottom')
    plt.show()
