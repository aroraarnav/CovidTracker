import requests
import json
import os
from tkinter import *
# BY ARNAV ARORA

API_KEY = "" # Key here
PROJECT_TOKEN = "" # Token here

root = Tk()

class Data:
    def __init__ (self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()

    def get_data (self):
        response = requests.get (f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
        self.data = json.loads(response.text)

    def get_total_cases (self):
        data = self.data["total"]
        for content in data:
            if content["name"] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths (self):
        data = self.data["total"]
        for content in data:
            if content["name"] == "Deaths:":
                return content['value']
        
        return "0"

    def get_country_data (self, country):
        data = self.data["country"]
        for content in data:
            if content["name"].lower() == country.lower():
                return content
            
        return "No such country was found.\nPlease check your spelling."

data = Data(API_KEY, PROJECT_TOKEN)

def speak(text):
    os.system("/usr/bin/say " + text)

def getInfo(country):
    if country.strip() == "":
        label['text'] = "Please enter a country to continue."

    elif country.lower() == "world":
        worldDeaths = str(data.get_total_deaths())
        worldCases = str(data.get_total_cases())
        label['text'] = "Showing Global Stats\nTotal number of cases: " + worldCases + "\nTotal number of deaths: " + worldDeaths
        speak ("The total number of cases in the world is " + worldCases + ". There have been " + worldDeaths + " deaths in total.")

    else:
        countryData = data.get_country_data(country)

        if countryData == "No such country was found.\nPlease check your spelling.":
            label['text'] = countryData
            speak("No such country was found. Please check your spelling and try again.")   
        else:
            print (countryData)
            name = (countryData['name'])
            totalCases = (countryData['total_cases'])
            totalDeaths = (countryData['total_deaths'])
            label['text'] = "Name of country: " + name + "\nTotal number of cases: " + str(totalCases) + "\nTotal number of deaths: " + str(totalDeaths) 
            speak("The total number of cases in " + name + " as of now is " + str(totalCases) + ". There have been " + str(totalDeaths) + " deaths in total.")

canvas = Canvas(root, height = 500, width = 600)
canvas.pack()

backgroundImage = PhotoImage(file = "") # Your Path Here
backgroundLabel = Label(root, image = backgroundImage)
backgroundLabel.place (relwidth = 1, relheight = 1)

upperFrame = Frame(root, bg = 'lightgreen', bd = 10)
upperFrame.place(relwidth = 0.75, relheight = 0.1, relx = 0.5, rely = 0.1, anchor = 'n')

lower_frame = Frame(root, bg = 'lightgreen', bd = 20)
lower_frame.place(relx = 0.5, rely = 0.25, relwidth = 0.75, relheight = 0.6, anchor = "n")

lowest_frame = Frame(root, bg = "lightblue", bd = 10)
lowest_frame.place(relwidth = 1, relheight = 0.1, relx = 0.5, rely = 0.9, anchor = "n")

covidLabel = Label(lowest_frame, text = "COVID-19 TRACKER", font = ('Courier', 24), bg = "lightblue", fg = "gray")
covidLabel.place(relx = 0.5, rely = 0, anchor = 'n')

creditLabel = Label(root, text = "By Arnav Arora", font = ('Courier', 18), bg = 'lightgreen', fg = 'gray')
creditLabel.place(relx = 0.8, rely = 0.8, anchor = "n", relwidth = 1.35)

button = Button(upperFrame, text= "Get Information", highlightbackground= 'lightgray', font = ('Courier', 14), command = lambda: getInfo(entry.get()))
button.place(relx = 0.7, relwidth = 0.3, relheight = 1)

label = Label(lower_frame, text = "When you enter a country above,\nCOVID-19 stats relating to the same\nwill be shown here.\n\nIf you want world stats,\nplease type 'world' above." , bg = 'lightgreen', font = ('Courier', 18), anchor = 'nw', justify = 'left')
label.place (relwidth = 1, relheight = 1)

entry = Entry(upperFrame, font = ('Courier', 18))
entry.place(relwidth = 0.65, relheight = 1)

root.after(0, speak("Welcome to the Corona Virus Tracker."))
mainloop()