# Paket für Bearbeitung von Tabellen
import pandas as pd
import streamlit as st


# Paket
## zuvor !pip install plotly
## ggf. auch !pip install nbformat
import plotly.express as px


def read_my_csv():
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep="\t", header=None)

    # Setzt die Columnnames im Dataframe
    df.columns = ["Messwerte in mV","Zeit in ms"]
    
    # Gibt den geladen Dataframe zurück
    return df

def read_my_activity():
    
    df = pd.read_csv("data/activities/activity.csv")

    #df["time_seconds"] = np.arange(1805)

    return df # dataframe with the activity


def make_power_hr_plot(df, hr_max):
    #select Hr column
    Herzrate = df["HeartRate"]

    #select power column
    powercolumn = df["PowerOriginal"]

    #plot both
    fig = px.line(df, y=Herzrate,
                  labels={"HeartRate": "Herzfrequenz | B/min", "index": "Zeit | s"})
    fig.update_traces(line=dict(color="black"))
    
    fig.add_hrect(y0=hr_max*0.5, y1=hr_max*0.6, fillcolor="green", opacity=0.04, layer="below")
    fig.add_hrect(y0=hr_max*0.6, y1=hr_max*0.7, fillcolor="green", opacity=0.12, layer="below")
    fig.add_hrect(y0=hr_max*0.7, y1=hr_max*0.8, fillcolor="green", opacity=0.24, layer="below")
    fig.add_hrect(y0=hr_max*0.8, y1=hr_max*0.9, fillcolor="green", opacity=0.32, layer="below")
    fig.add_hrect(y0=hr_max*0.9, y1=hr_max, fillcolor="green", opacity=0.4, layer="below")

    fig.add_annotation(x=1950,
                       y=hr_max*0.5+5,
                       text="Zone 1",
                       showarrow=False,
                       font=dict(color="black"))
    fig.add_annotation(x=1950,
                       y=hr_max*0.6+5,
                       text="Zone 2",
                       showarrow=False,
                       font=dict(color="black"))
    fig.add_annotation(x=1950,
                       y=hr_max*0.7+5,
                       text="Zone 3",
                       showarrow=False,
                       font=dict(color="black"))
    fig.add_annotation(x=1950,
                       y=hr_max*0.8+5,
                       text="Zone 4",
                       showarrow=False,
                       font=dict(color="black"))
    fig.add_annotation(x=1950,
                       y=hr_max*0.9+5,
                       text="Zone 5",
                       showarrow=False,
                       font=dict(color="black"))

    return fig

def add_hr_zones(df, hr_max):
    zone_dict = {"zone1": hr_max*0.6,
                 "zone2": hr_max*0.7,
                 "zone3": hr_max*0.8,
                 "zone4": hr_max*0.9,
                 "zone5": hr_max}

    z1_mask = ((df["HeartRate"]< zone_dict["zone1"])&(df["HeartRate"]>hr_max*0.4)) 
    z1 = z1_mask.sum() 

    z2_mask = ((df["HeartRate"]> zone_dict["zone1"]) & (df["HeartRate"]< zone_dict["zone2"]))  
    z2 = z2_mask.sum() 
    
    z3_mask = ((df["HeartRate"]> zone_dict["zone2"]) & (df["HeartRate"]< zone_dict["zone3"]))  
    z3 = z3_mask.sum() 

    z4_mask = ((df["HeartRate"]> zone_dict["zone3"]) & (df["HeartRate"]< zone_dict["zone4"]))  
    z4 = z4_mask.sum()

    z5_mask = (df["HeartRate"]> zone_dict["zone4"])
    z5 = z5_mask.sum()

    df2 = pd.DataFrame({
        "Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
        "Werte / s": [z1,z2,z3,z4,z5]
    })
    return df2



def make_plot(df):

    # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
    fig = px.line(df.head(2000), x= "Zeit in ms", y="Messwerte in mV")
    return fig

if __name__ == "__main__":
    activity_df = read_my_activity()

    #print(activity_df.head())

    my_fig = make_power_hr_plot(activity_df, 200)

    #my_fig.show()
    
    df_zones = add_hr_zones(activity_df,200)
    print(df_zones)

    st.title("Running analysis")
    st.markdown("#### Table of Measurements in Different Zones")
    
    st.table(df_zones)

    st.markdown("#### Describing Values")

    df = read_my_activity()
    st.write("The maximum heartrate is:", df["HeartRate"].max(), "B/min")
    st.write("The mean heartrate is:", df["HeartRate"].mean(), "B/min", 
             "/ or about ~", int(df["HeartRate"].mean()),"B/min")

    
    st.markdown("#### Heartrate over Time / Zone's")
    st.plotly_chart(my_fig)
   
    
    


