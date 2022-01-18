import requests
import json
from PIL import Image
from bs4 import BeautifulSoup


def format(p):
    p = p.replace('\n','')
    p = p.strip()
    p = p.replace(' ', '-')
    p = p.lower()

    return p

def format_list(l):
    n = []
    for p in l:
        p = p.replace('\n','')
        p = p.strip()
        p = p.replace(' ', '-')
        p = p.lower()
        n.append(p)
    return n



URL = "https://realpython.github.io/fake-jobs/"
brock = "https://bulbapedia.bulbagarden.net/wiki/Brock"
page = requests.get(URL)
b = requests.get(brock)

soup = BeautifulSoup(page.content, "html.parser")

brock_soup = BeautifulSoup(b.content, "html.parser")

results = soup.find(id="ResultsContainer")
brock_res = brock_soup.find_all("table", class_="expandable")

leaders_list = [
    'brock', 'misty', 'lt._Surge', 'erika', 'koga', 'sabrina', 'blaine', 'giovanni', #gen1
    'falkner','bugsy', 'whitney', 'morty', 'chuck', 'jasmine', 'pryce', 'clair', #gen2
    'roxanne', 'brawly', 'wattson', 'flannery', 'norman', 'winona', 'Tate_and_Liza', 'wallace', #gen3
    'roark', 'gardenia', 'maylene', 'Crasher_Wake', 'fantina', 'byron', 'candice', 'volkner', #gen4
    'chili', 'cilan', 'cress', 'lenora', 'burgh', 'elesa', 'clay', 'skyla', 'brycen', 'drayden', 'iris', #gen5
    'viola', 'grant', 'korrina', 'ramos', 'clemont', 'valerie', 'olympia', 'wulfric', #gen6
    'milo', 'nessa', 'kabu', 'bea', 'allister', 'opal', 'gordie', 'melony', 'piers', 'raihan' #gen8
    ]
versions = [
            'red', 'blue', 'green', 'yellow',
            'gold', 'silver', 'crystal',
            'ruby', 'saphire', 'emerald',
            'pearl', 'diamond', 'platinum'
            'firered','leafgreen',
            'heartgold', 'soulsilver', 
            'black', 'white', 
            'x', 'y',
            'omega', 'alpha',
            'sun', 'moon',
            'ultra',
            'sword', 'shield',
            'brilliant', 'shining'
            'Pikachu!'
            ]


leaders = {
    #Gen1
    'brock':{
        'primary-typing':'rock',
        'versions':[] #here is where all of the information will be added leaders[leaders-name][versions] = all the stuff
    },
    'misty':{
        'primary-typing':'water',
        'versions':[]
    },
    'lt.-surge':{
        'primary-typing':'electric',
        'versions':[]
    },
    'erika':{
        'primary-typing':'grass',
        'versions':[]
    },
    'koga':{
        'primary-typing':'poison',
        'versions':[]
    },
    'sabrina':{
        'primary-typing':'psychic',
        'versions':[]
    },
    'blaine':{
        'primary-typing':'fire',
        'versions':[]
    },
    'giovanni':{
        'primary-typing':'ground',
        'versions':[]
    },
    #Gen2
    'falkner':{
        'primary-typing':'flying',
        'versions':[]
    },
    'bugsy':{
        'primary-typing':'bug',
        'versions':[]
    },
    'whitney':{
        'primary-typing':'normal',
        'versions':[]
    },
    'morty':{
        'primary-typing':'ghost',
        'versions':[]
    },
    'chuck':{
        'primary-typing':'fighting',
        'versions':[]
    },
    'jasmine':{
        'primary-typing':'steel',
        'versions':[]
    },
    'pryce':{
        'primary-typing':'ice',
        'versions':[]
    },
    'clair':{
        'primary-typing':'dragon',
        'versions':[]
    },
    #Gen3
    'roxanne':{
        'primary-typing':'rock',
        'versions':[]
    },
    'brawly':{
        'primary-typing':'fighting',
        'versions':[]
    },
    'wattson':{
        'primary-typing':'electric',
        'versions':[]
    },
    'flannery':{
        'primary-typing':'fire',
        'versions':[]
    },
    'norman':{
        'primary-typing':'normal',
        'versions':[]
    },
    'winona':{
        'primary-typing':'flying',
        'versions':[]
    },
    'tate-&-liza':{ # /Tate_and_Liza
        'primary-typing':'psychic',
        'versions':[]
    },
    'wallace':{
        'primary-typing':'water',
        'versions':[]
    },
    #Gen4
    'roark':{
        'primary-typing':'rock',
        'versions':[]
    },
    'gardenia':{
        'primary-typing':'grass',
        'versions':[]
    },
    'maylene':{
        'primary-typing':'fighting',
        'versions':[]
    },
    'wake':{ #Crasher_Wake
        'primary-typing':'water',
        'versions':[]
    },
    'fantina':{
        'primary-typing':'ghost',
        'versions':[]
    },
    'byron':{
        'primary-typing':'steel',
        'versions':[]
    },
    'candice':{
        'primary-typing':'ice',
        'versions':[]
    },
    'volkner':{
        'primary-typing':'electric',
        'versions':[]
    },
    #Gen5
    'chili':{
        'primary-typing':'fire',
        'versions':[]
    },
    'cilan':{
        'primary-typing':'grass',
        'versions':[]
    },
    'cress':{
        'primary-typing':'water',
        'versions':[]
    },
    'lenora':{
        'primary-typing':'normal',
        'versions':[]
    },
    'burgh':{
        'primary-typing':'bug',
        'versions':[]
    },
    'elesa':{
        'primary-typing':'electric',
        'versions':[]
    },
    'clay':{
        'primary-typing':'ground',
        'versions':[]
    },
    'skyla':{
        'primary-typing':'flying',
        'versions':[]
    },
    'brycen':{
        'primary-typing':'ice',
        'versions':[]
    },
    'drayden':{
        'primary-typing':'dragon',
        'versions':[]
    },
    'iris':{ #there's an issue with Drayden displaying and not Iris
        'primary-typing':'dragon',
        'versions':[]
    },
    #Gen6
    'viola':{ 
        'primary-typing':'bug',
        'versions':[]
    },
    'grant':{ 
        'primary-typing':'rock',
        'versions':[]
    },
    'korrina':{ 
        'primary-typing':'fighting',
        'versions':[]
    },
    'ramos':{ 
        'primary-typing':'grass',
        'versions':[]
    },
    'clemont':{ 
        'primary-typing':'electric',
        'versions':[]
    },
    'valerie':{ 
        'primary-typing':'fairy',
        'versions':[]
    },
    'olympia':{ 
        'primary-typing':'psychic',
        'versions':[]
    },
    'wulfric':{ 
        'primary-typing':'ice',
        'versions':[]
    },
    # no Gen7 leaders
    #Gen8
    'milo':{ 
        'primary-typing':'grass',
        'versions':[]
    },
    'nessa':{ 
        'primary-typing':'water',
        'versions':[]
    },
    'kabu':{ 
        'primary-typing':'fire',
        'versions':[]
    },
    'bea':{ 
        'primary-typing':'fighting',
        'versions':[]
    },
    'allister':{ 
        'primary-typing':'ghost',
        'versions':[]
    },
    'opal':{ 
        'primary-typing':'fairy',
        'versions':[]
    },
    'gordie':{ 
        'primary-typing':'rock',
        'versions':[]
    },
    'melony':{ 
        'primary-typing':'ice',
        'versions':[]
    },
    'piers':{ 
        'primary-typing':'dark',
        'versions':[]
    },
    'raihan':{ 
        'primary-typing':'dragon',
        'versions':[]
    },
}


for leader in leaders_list:
    leader_bulb_url = f"https://bulbapedia.bulbagarden.net/wiki/{leader}"
    l = requests.get(leader_bulb_url)
    leader_soup = BeautifulSoup(l.content, "html.parser")
    res = leader_soup.find_all("table", class_="expandable")

    for i in res:

        version = {
            'version-name':None,
            'leader-name':None,
            'location':None,
            'pokebucks':None,
            'pokemon-team':[]
        }

        imgLinksArray = []

        im = i.find("img")
        if im:
            imageLink = 'http:' + im['src']
            imgLinksArray.append(imageLink)

    #gym leader name
        name = i.find("big")
        if name != None:
            n = format(name.text)
            if n in leaders:
                version['leader-name'] = n

    #location name
        s = i.find_all("span")
        for j in s:
            if "Gym" in j.text or "Stadium" in j.text:
                if j.text.endswith("Gym") or j.text.endswith("Stadium"):
                    version['location'] = format(j.text)

    #names of the versions              
        sm = i.find_all("small")
        for j in sm:
            k = j.text.split(' ')

            for item in k:
                item = item.replace(',','')
                if item.lower() in versions:
                    #this will need to be fixed later to account for the multiworded titles
                    version['version-name'] = format(item)

    #number of pokebucks
        pokebucks = i.find_all("b")
        for j in pokebucks:
            if j != None:
                if j.text.isnumeric():
                    version['pokebucks'] = j.text



    # Moves and names of pokemon

        pokemon_names = []
        pokemon_levels = []
        pokemon_moves = [[]]
        pokemon_abilities = []
        pokemon_held_items = []

        pTeam = i.find_all("a")
        pm = []
        for j in pTeam:
            t = j.get('title')
            if t != None:
                if t.endswith("mon)"):
                    pokemon_moves.append(pm)
                    pm = []
                    t = t[:-10] #removes (pokemon) from the end of the string
                    pokemon_names.append(t)
                if t.endswith("move)"):
                    t = t[:-7]
                    if t != 'Struggle':
                        pm.append(t)
        pokemon_moves.append(pm)

        pokemon_moves = list(filter(None,pokemon_moves)) #removes empty lists from 2d list
            
    # levels of pokemon
        teamLevel = i.find_all("td")
        for j in teamLevel:
            if j.text != None:
                s = j.text.split()
                for x in s:
                    if x.startswith('Lv'):
                        pokemon_levels.append(x)

    #held items of pokemon
        heldItem = i.find_all(text="Held item:")
        for h in heldItem:
            if len(h.findNext('td').text) > 0:
                pokemon_held_items.append(h.findNext('td').text.replace('\n',''))
            else:
                pokemon_held_items.append('None')

    #abilities of pokemon
        ability = i.find_all(text="Ability:")
        for a in ability:
            pokemon_abilities.append(a.findNext('td').text)


    #put all the elements of the pokemon together
        for count in range(len(pokemon_names)):
            pokemon = {
                'name': format(pokemon_names[count]),
                # 'id': None,
                'level': None,
                'held_item': None,
                'ability': None,
                'moves': None
            }

            if pokemon_levels:
                pokemon['level'] = pokemon_levels[count]
            
            if pokemon_moves:
                pokemon['moves'] = format_list(pokemon_moves[count])

            if len(pokemon_abilities) == len(pokemon_names):
                pokemon['ability'] = format(pokemon_abilities[count])

            if len(pokemon_held_items) == len(pokemon_names):
                pokemon['held_item'] = format(pokemon_held_items[count])

            # pokemonApiInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon["name"]}')
            # if not pokemonApiInfo.ok:
            #     continue
            # else:
            #     pokemonApiInfo = pokemonApiInfo.json()
            #     pokemon['id'] = pokemonApiInfo['id']
            
            version['pokemon-team'].append(pokemon)

            print(version['pokemon-team'])

        if version['version-name']:
            if version['location'] != None:
                if version['leader-name'] in leaders:
                    for item in imgLinksArray:
                        name = version['leader-name']
                        vers = version['version-name']

                        img = Image.open(requests.get(item, stream = True).raw)
                        img.save(f'static/css/images/gymLeaderImages/{name}-{vers}.png')

                    leaders[version['leader-name']]['versions'].append(version)


# for key in leaders:
#     print(key,leaders[key])

with open('gymLeaders.json', 'w') as file: file.write(json.dumps(leaders))  