import json
import pandas as pd
import plotly.express as px
import numpy as np



# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    @staticmethod
    def make_plot_df(df):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        fig = px.line(df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        return fig 

    @staticmethod
    def read_my_csv(dateipfad):
        # Einlesen eines Dataframes
        ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
        ## header = None: es gibt keine Überschriften in der txt-Datei
        df = pd.read_csv(dateipfad, sep="\t", header=None)

        # Setzt die Columnnames im Dataframe
        df.columns = ["Messwerte in mV","Zeit in ms"]
        
        # Gibt den geladen Dataframe zurück
        return df

    @staticmethod
    def load_person_data():
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data
    

    @staticmethod
    def load_EKG_by_id(id, test_nr=0):
        personendata = EKGdata.load_person_data()

        for person in personendata:
            if person["id"] == id:
                #return person["ekg_tests"]
                return person["ekg_tests"][test_nr]["result_link"]
                

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        #self.df = self.df.iloc[:5000]  # Entferne die erste Zeile, da sie nur die Spaltennamen enthält


    def plot_time_series(self):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        return self.fig 

    def calc_avg_hr(self):
        df = self.df.copy()
        df_peaks = df.loc[df["is_peak"]]
        df_peaks.head()

        anzahl_peaks = df["is_peak"].sum()

        df_peaks["Time in ms"].iloc[0]
        df_peaks["Time in ms"].iloc[-1]

        dt_ms = df_peaks["Time in ms"].iloc[-1] - df_peaks["Time in ms"].iloc[0]
        dt_mins = dt_ms / 60000
        avg_hr = anzahl_peaks / dt_mins
        return avg_hr


if __name__ == "__main__":
    #print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    #print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    #print(ekg.df.head()) 

    #print(EKGdata.load_EKG_by_id(2))
    #print(EKGdata.load_person_data())
    #print(EKGdata.read_my_csv(EKGdata.load_EKG_by_id(2)))

    Leistungstest_df = EKGdata.read_my_csv(EKGdata.load_EKG_by_id(2))
    plot = EKGdata.make_plot_df(Leistungstest_df)
    #plot.show()

