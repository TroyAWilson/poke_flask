from os import environ
from flask import Flask, render_template, url_for, request
import requests
import json
import random

app = Flask(__name__)

def loadRandomPokemonBatch():
    batch = []
    used = []
    for p in range(24):
        rand = random.randint(0,897)
        while(rand in used):
            rand = random.randint(0,897)
        singleRandomMon = data[rand]
        batch.append(singleRandomMon)
        used.append(rand)
    return batch

@app.route('/')
def index():
    batch = loadRandomPokemonBatch()
    return render_template('index.html', batch=batch)

#gets to pokemon page by pokemon name
@app.route('/<name>')
def pokebyname(name = None):
    for i in data:
        if i['name'] == name:
            # sort the list of moves before rendering
            i['moves'] = sorted(i['moves'], key=lambda j:j['level_learned_at'])

            # The last pokemon has to manually be wrapped back around to the start
            if i['id'] == 898:
                next = {
                    'name': data[0]['name'],
                    'id' : data[0]['id']
                }
            else:
                 next = {
                    'name': data[i['id']]['name'],
                    'id': data[i['id']]['id']
                }
            prev = {
                'name':data[i['id']-2]['name'],
                'id':data[i['id']-2]['id']
            }

            return render_template('pokemon.html', Pokemon = i, nextMon = next, prevMon = prev)
    return render_template('error.html')

#get to pokemon page by pokedex number
@app.route('/pokemon/<num>')
def pokebynum(num = None):
    num = int(num)
    for i in data:
        if i['id'] == num:
            # sort the list of moves before rendering
            i['moves'] = sorted(i['moves'], key=lambda j:j['level_learned_at'])
            
            if num == 898:
                next = {
                    'name': data[0]['name'],
                    'id' : data[0]['id']
                }
            else:
                 next = {
                    'name': data[num]['name'],
                    'id' : data[num]['id']
                }

            prev = {
                'name':data[num-2]['name'],
                'id':data[num-2]['id']
            }

            return render_template('pokemon.html', Pokemon = i, nextMon = next, prevMon = prev)
    return render_template('error.html')


#function for search bar to get page of the new pokemon being serached
@app.route('/getNewPokemon', methods = ["GET", "POST"])
def getNewPokemon():
    if request.method == "POST":
        name = request.form.get("newName")     
        return pokebyname(name)
    return "Uh oh, something has gone wrong!"

@app.route('/getNewPokemonbyNumber', methods = ["GET", "POST"])
def getNewPokemonbyNumber(num = None):
    if request.method == "POST":
        num = request.form.get("newNumber")
        if num == None:
            num = request.form.get("imageNumber")
            if num == None:
                return render_template('Error.html')

        return pokebynum(num)
    return "Uh oh, something has gone wrong!"




def setUpEvolutionLines(ev_chain):
    evChain = {
            'smallestMon': None,
            'smallestMonId': None,
            
            'midMon': [],
            
            'bigMon': [],
        }

    if 'name' in ev_chain['chain']['species']:
        evChain['smallestMon'] = ev_chain['chain']['species']['name']
        smallurl = ev_chain['chain']['species']['url']
        getOne = requests.get(smallurl).json()
        evChain['smallestMonId'] = getOne['id']

        for i in ev_chain['chain']['evolves_to']:
            m = {
                'name':None,
                'id':None,
                'level_up_trigger':None,
                'level':None, 
                'item':None, 
                'happiness':None, 
                'location': None
                # Add time_of_day - triggered by level up
                # Add affection - triggered by level up
                # Add trade_species['name'] - triggered by trade
                # Add beauty - triggered by level up
                # Add Held Item -triggered by trade and maybe level up
                    #gligar requires holding an item and to level up at night
            }

            midurl = i['species']['url']
            getOne = requests.get(midurl).json()

            m['name'] = i['species']['name']
            m['id'] = getOne['id']

            if len(i['evolution_details']) > 0:
                m['level_up_trigger'] = i['evolution_details'][0]['trigger']['name']
                
                m['level'] = i['evolution_details'][0]['min_level']
                if m['level_up_trigger'] == 'use-item' and i['evolution_details'][0]['item'] != None:
                    m['item'] = i['evolution_details'][0]['item']['name']
                m['happiness'] = i['evolution_details'][0]['min_happiness']
                m['location'] = i['evolution_details'][0]['location']


            evChain['midMon'].append(m)

            for j in i['evolves_to']:
                b = {'name':None, 'id':None, 'level_up_trigger':None, 'level':None, 'item':None, 'happiness':None, 'location': None}
                bigurl = j['species']['url']
                getOne = requests.get(bigurl).json()

                b['name'] = j['species']['name']
                b['id'] = getOne['id']

                if len(j['evolution_details']) > 0:
                    b['level_up_trigger'] = j['evolution_details'][0]['trigger']['name']

                    b['level'] = j['evolution_details'][0]['min_level']
                    if b['level_up_trigger'] == 'use-item' and j['evolution_details'][0]['item'] != None:
                        b['item'] = j['evolution_details'][0]['item']['name']
                    b['happiness'] = j['evolution_details'][0]['min_happiness']
                    b['location'] = j['evolution_details'][0]['location']

                evChain['bigMon'].append(b)


    return evChain



def testEmAll():
    Pokemon=[]
    print('collecting pokemon')

    for i in range(90,899):
        pokemonMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}').json()
        pokemonSpeciesMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{i}').json()
        print(f"Pokemon ID: {pokemonMassInfo['id']}")
        ev_chain = requests.get(pokemonSpeciesMassInfo['evolution_chain']['url']).json()

        evChain = setUpEvolutionLines(ev_chain)

        print(evChain)




# You need to fix the evolution line on the pokemon html page

def grabEmAll():
    Pokemon=[]
    print('collecting pokemon')

    for i in range(1,899):
        pokemonMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}').json()
        pokemonSpeciesMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{i}').json()
        print(f"Pokemon ID: {pokemonMassInfo['id']}")
        ev_chain = requests.get(pokemonSpeciesMassInfo['evolution_chain']['url']).json()
        pMoves= packageMoves(pokemonMassInfo)
        evChain = setUpEvolutionLines(ev_chain)

        pokemon = {
            'name': pokemonMassInfo['name'],
            'id':  pokemonMassInfo['id'],
            'abilities':  pokemonMassInfo['abilities'],
            'base_experience': pokemonMassInfo['base_experience'],
            'forms':  pokemonMassInfo['forms'],
            'height':  pokemonMassInfo['height'],
            'weight':  pokemonMassInfo['weight'],
            'sprites':  pokemonMassInfo['sprites'],
            'stats':  pokemonMassInfo['stats'],
            'types':  pokemonMassInfo['types'],
            
            'catch_rate': pokemonSpeciesMassInfo['capture_rate'],
            'base_happiness': pokemonSpeciesMassInfo['base_happiness'],
            'egg_groups': pokemonSpeciesMassInfo['egg_groups'],
            'evolution_chain': evChain,
            'flavor_text_entries': pokemonSpeciesMassInfo['flavor_text_entries'],
            'growth_rate': pokemonSpeciesMassInfo['growth_rate'],
            'habitat': pokemonSpeciesMassInfo['habitat'],
            'species': pokemonSpeciesMassInfo['genera'][7]['genus'],

            'moves': pMoves
        }

        Pokemon.append(pokemon)

    with open('pokemon.json', 'w') as file: file.write(json.dumps(Pokemon))  






def gatherMoves():
    moves = {}
    for i in range(1,826):
        print(i)
        r = requests.get(f'https://pokeapi.co/api/v2/move/{i}').json()
        
        moves[r['name']] = {
            'name': r['name'],
            'accuracy': r['accuracy'],
            'damage_class': r['damage_class']['name'],
            'power': r['power'],
            'pp': r['pp'],
            'type': r['type']['name']
        }
    
    with open('moves.json', 'w') as file: file.write(json.dumps(moves))  



def packageMoves(pokemon):
    m = open('moves.json')
    movesData = json.load(m)
    m.close()

    pMoves = []

    for i in pokemon['moves']:
        pMove = {
            'name': None,
            'level_learned_at': None,
            'move_learn_method': None,
            'damage_class': None,
            'power':None,
            'pp': None,
            'type': None,
            'accuracy':None
        }

        pMove['name'] = i['move']['name']
        pMove['level_learned_at'] = i['version_group_details'][len(i['version_group_details'])-1]['level_learned_at']
        pMove['move_learn_method'] = i['version_group_details'][len(i['version_group_details'])-1]['move_learn_method']['name']
        pMove['damage_class'] = movesData[pMove['name']]['damage_class']
        pMove['power'] = movesData[pMove['name']]['power']
        pMove['pp'] = movesData[pMove['name']]['pp']
        pMove['type'] = movesData[pMove['name']]['type']
        pMove['accuracy'] = movesData[pMove['name']]['accuracy']

        pMoves.append(pMove)

    return pMoves


def test():
    p = requests.get(f'https://pokeapi.co/api/v2/pokemon/25').json()

    y = packageMoves(p)

    print(y)



if __name__ == '__main__':
    print('starting PokeInfo')
    # grabEmAll()
    # testEmAll()

    # test()

    f = open('pokemon.json')
    print('loading json file')
    data = json.load(f)
    f.close() 
    
    app.run()