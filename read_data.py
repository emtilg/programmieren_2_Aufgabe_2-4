import json

def load_person_data():
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data

def get_person_list(person_data):
    list_of_names=[]

    for e in person_data:
        list_of_names.append(e["lastname"] + "," + " " + e["firstname"])
   
    return list_of_names

print(get_person_list(load_person_data()))

#print(load_person_data())

def find_person_data_by_name(suchstring):

    if suchstring == "None":
        return {}

    #suchstring = "Huber, Julian"
    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]
    #print(nachname)

    data = load_person_data()

    for e in data:
        #print(e)
        if nachname == e["lastname"] and vorname == e["firstname"]:
            return e

    return {}

print(find_person_data_by_name("Heyer, Yannic"))


eintrag = find_person_data_by_name("Huber, Julian")
Picturepath = eintrag["picture_path"]
print(Picturepath)