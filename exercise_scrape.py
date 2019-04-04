from bs4 import BeautifulSoup
import requests
import re
import json

def init(URList):
    url = "https://www.jefit.com/exercises/"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    table = soup.find("div", {"class": "card-body"})
    exercise_group = table.find_all("li")

    for exercises in exercise_group:
        link = exercises.find("a")
        URList.append(link['href'])
    for link in URList:
        print(link)

def extract_exercises(URList, link_add):
    page_re = re.compile("Page \d of (\d+)")
    exercise_type_re = re.compile("exercises=([a-z-A-Z]+)")
    exercise_json = {}
    exercise_json['excercises'] = []
    exercise_list = []
    URList.pop(11)
    for links in URList:
        body_type = exercise_type_re.search(links)
        btype = body_type.group(1)
        if body_type.group(1) == "Glutes" or body_type.group(1) == "Lower-Legs" or body_type.group(1) == "Upper-Legs":
            btype = "Legs"

        muscle_group = ()
        html = requests.get(links)
        soup = BeautifulSoup(html.content, "html.parser")
        page_gather = soup.find("div", {"class": "pageCell"})
        match = page_re.match(page_gather.text)
        page_number = int(match.group(1))
        i = 2
        while i < page_number:
            for exercises in soup.find_all("h4"):
                exercise_json['excercises'].append({"name": exercises.text, "type": btype})
                print(exercise_json)
                muscle_group += (exercise_json,)
            next_page = links + link_add + str(i)
            html = requests.get(next_page)
            soup = BeautifulSoup(html.content, "html.parser")
            i += 1
       # exercise_list.append(muscle_group)
    with open ('test.json', 'w') as exercise_file:
        json.dump(exercise_json, exercise_file)

if __name__ == '__main__':
    link_add = "&All=0&Bands=0&Bench=0&Dumbbell=0&EZBar=0&Kettlebell=0&MachineStrength=0&MachineCardio=0&Barbell=0&BodyOnly=0&ExerciseBall=0&FoamRoll=0&PullBar=0&WeightPlate=0&Other=0&Strength=0&Stretching=0&Powerlifting=0&OlympicWeightLifting=0&Beginner=0&Intermediate=0&Expert=0&page="
    URList = []
    init(URList)
    extract_exercises(URList, link_add)
