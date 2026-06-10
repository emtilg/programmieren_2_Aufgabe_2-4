import pandas as pd
import numpy as np
import plotly.express as px

def read_data():
    df = pd.read_csv("data/activities/activity.csv")
    return df

def add_time(df):
    df["Time"] = np.arange(len(df))
    return df

def find_best_effort(df,window_size,resolution=1):
    best_effort = df["PowerOriginal"].rolling(window_size*resolution).mean().max()
    return best_effort

def create_pc(window_list):
    avg_power = []
    
    for window_size in window_list:
        avg_power.append(find_best_effort(df,window_size))
    
    df_pc = pd.DataFrame({"Time": window_list,
                          "Avg_Power": avg_power})
    return df_pc


def fig(window_list,power):
    return px.line(x= window_list,
                   y= power)

if __name__ == "__main__":
    #window_list = [10,20,30,60,300,600,1200,1800,3600,7200]
    window_list = [10,20,30,40,60,80,100,130,160,190,240,270,300,400,500,600,800,1000,1100,1200,1300,1400,1500,1700,1800]
    df = read_data()
    df_time = add_time(df)
    df_pc = create_pc(window_list)
    figure = fig(df_pc["Time"], df_pc["Avg_Power"])
    figure.show()