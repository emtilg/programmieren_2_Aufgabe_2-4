import json
import plotly.express as px
import find_peaks
import pandas as pd
import plotly.graph_objects as go


# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    @staticmethod
    def ekg_dict_choose(person, ekg_test=0):
        file = open("data/person_db.json")
        person_data = json.load(file)
        ekg_dict = person_data[person]["ekg_tests"][ekg_test]

        return ekg_dict

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df_1 = find_peaks.add_peaks_true_false(self.data)  #df mit den peaks für avg_hr berechnung
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])  #df ohne peaks für graph
        #self.df = self.df.iloc[:5000]  # Entferne die erste Zeile, da sie nur die Spaltennamen enthält

    def printen(self):
        print(self.df)


    def plot_time_series(self):

        #Plot des EKGs mit Peaks gefärbt

        fig = go.Figure()

        df_plot = self.df_1[:2000]

        fig.add_trace(
            go.Scatter(
                x=df_plot["Time in ms"],
                y=df_plot["EKG in mV"],
                mode="lines",
                name="EKG"
            )
        )

        peak_df = df_plot[df_plot["is_peak"]]
        
        fig.add_trace(
            go.Scatter(
                x=peak_df["Time in ms"],
                y=peak_df["EKG in mV"],
                mode="markers",
                marker=dict(
                    color = "red",
                    size = 8
                ),
                name ="Peaks"
            )
        )
        #fig.show()
        return fig
        '''
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        return self.fig 
        '''
    
    def calc_avg_hr(self):
        df = self.df_1.copy()
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
    
    '''  #This operations are now covered in the 'ekg_dict_choose 'funktion
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    '''
    #print(EKGdata.ekg_dict_choose(0))
    
    objekt = EKGdata(EKGdata.ekg_dict_choose(0,0))
    #objekt.printen()
    print(objekt.calc_avg_hr())
    #objekt.plot_time_series()