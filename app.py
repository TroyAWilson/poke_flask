from os import environ
from flask import Flask, render_template, url_for, request
from flask.wrappers import Response
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

@app.route('/move/<name>')
def moveByName(name = None):
    return render_template('move.html', move = movesData[name], pokemon = data, data = data)

@app.route('/item/<name>')
def itemByName(name = None):
    return render_template('item.html', item = itemsData[name], pokemon = data, data = data)

@app.route('/type/<name>')
def typeByName(name = None):
    return render_template('type.html', type = typesData[name], move = movesData, pokemon = data)

@app.route('/')
def index():
    batch = loadRandomPokemonBatch()
    return render_template('index.html', batch=batch, data = data)

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

            return render_template('pokemon.html', Pokemon = i, nextMon = next, prevMon = prev, data = data)
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

            return render_template('pokemon.html', Pokemon = i, nextMon = next, prevMon = prev, data = data)
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
                'location': None,
                
                'time_of_day': None,
                'affection': None,
                'trade_species': None,
                'beauty': None,
                'held_item': None
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

                m['time_of_day'] = i['evolution_details'][0]['time_of_day']
                m['affection'] = i['evolution_details'][0]['min_affection']
                if i['evolution_details'][0]['held_item'] != None:
                    m['held_item'] = i['evolution_details'][0]['held_item']['name']
                m['trade_species'] = i['evolution_details'][0]['trade_species']
                m['beauty'] = i['evolution_details'][0]['min_beauty']

            evChain['midMon'].append(m)

            for j in i['evolves_to']:
                b = {
                    'name':None,
                    'id':None,
                    'level_up_trigger':None,
                    'level':None, 
                    'item':None, 
                    'happiness':None, 
                    'location': None,
                    
                    'time_of_day': None,
                    'affection': None,
                    'trade_species': None,
                    'beauty': None,
                    'held_item': None
                }                
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

                    b['time_of_day'] = j['evolution_details'][0]['time_of_day']
                    b['affection'] = j['evolution_details'][0]['min_affection']
                    if j['evolution_details'][0]['held_item'] != None:
                        b['held_item'] = j['evolution_details'][0]['held_item']['name']
                    b['trade_species'] = j['evolution_details'][0]['trade_species']
                    b['beauty'] = j['evolution_details'][0]['min_beauty']

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
    t = open('types.json')
    tData = json.load(t)
    t.close() 
    print('collecting pokemon')

    for i in range(1,899):
        pokemonMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}').json()
        pokemonSpeciesMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{i}').json()
        print(f"Pokemon ID: {pokemonMassInfo['id']}")
        ev_chain = requests.get(pokemonSpeciesMassInfo['evolution_chain']['url']).json()
        pMoves= packageMoves(pokemonMassInfo)
        evChain = setUpEvolutionLines(ev_chain)

        pokemon = {
            'name': pokemonMassInfo['species']['name'],
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

            'moves': pMoves,
            'weaknessChart':None
        }

        weaknessChart = {
            'normal':0,
            'fire':0,
            'water':0,
            'electric':0,
            'grass':0,
            'ice':0,
            'fighting':0,
            'poison':0,
            'ground':0,
            'flying':0,
            'psychic':0,
            'bug':0,
            'rock':0,
            'ghost':0,
            'dragon':0,
            'dark':0,
            'steel':0,
            'fairy':0,
        }

        ddf = []
        hdf = []
        for j in pokemon['types']:
            ddf.append(tData[j['type']['name']]['double_damage_from'])
            hdf.append(tData[j['type']['name']]['half_damage_from'])

        for j in ddf:
            for k in j:
                weaknessChart[k] += 2
        
        for j in hdf:
            for k in j:
                weaknessChart[k] -= 2

        pokemon['weaknessChart'] = weaknessChart

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
            'type': r['type']['name'],
            'flavor_text':r['flavor_text_entries'][7]['flavor_text'].replace('\n',' '),
            'learned_by': None, #set this up, should be an array of pokemon names, then can search the local pokemon data to get the ID number
            'tm': None, #if 'machines' is empty leave this empty otherwise [machines][length of thing][machine][url] gives you a url follow url and go [item][name]
        }

        learned = []

        for item in r['learned_by_pokemon']:
            learned.append(item['name'])

        moves[r['name']]['learned_by'] = learned

        if len(r['machines']) > 0:
            tmURL = r['machines'][len(r['machines'])-1]['machine']['url']
            tmInfo = requests.get(tmURL).json()
            moves[r['name']]['tm'] = tmInfo['item']['name']

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

def gatherItems():
    items = {}
    for i in range(1,1330):
        print(i)
        item = requests.get(f'https://pokeapi.co/api/v2/item/{i}')
        if not item.ok:
            continue
        else:
            item = item.json()

        items[item['name']] = {
            'name': None,
            'cost': item['cost'],
            'sprite': item['sprites']['default'],
            'effect': None,
            'attributes': None,
            'flavor_text': None
        }

        if len(item['effect_entries']) > 0:
            items[item['name']]['effect'] = item['effect_entries'][0]['effect'].replace('\n',' ')


        manyFlavorText = []
        manyAttributes = []

        for j in item['names']:
            if j['language']['name'] == 'en':
                items[item['name']]['name'] = j['name']

        for j in item['flavor_text_entries']:
            if j['language']['name'] == 'en':
                flavor = {
                    'text':j['text'].replace('\n', ' '),
                    'version':j['version_group']['name'].replace('-',' ')
                }
                manyFlavorText.append(flavor)
        items[item['name']]['flavor_text'] = manyFlavorText

        for j in item['attributes']:
            manyAttributes.append(j['name'])

        # print(items)

    with open('items.json', 'w') as file: file.write(json.dumps(items))  


def gatherTypes():
    print('gathering types')

    #What do I need?
    # 1 - 18
    # double damage from
    # double damage to
    # half damage from
    # half damage to
    # pokemon names of that type [pokemon][#][pokemon][name]
    types = {}
    for i in range(1,19):
        print(i)
        type = requests.get(f'https://pokeapi.co/api/v2/type/{i}')
        #error checking
        if not type.ok:
            continue
        else:
            type = type.json()

        types[type['name']] = {
            'name': type['name'],
            'double_damage_from': None,#array
            'double_damage_to': None, #array
            'half_damage_from': None,#array
            'half_damage_to': None, #array
            'pokemon_of_type':None, #array of names
            'moves_of_type': None,
        }

        ddf = []
        for j in type['damage_relations']['double_damage_from']:
            ddf.append(j['name'])
        types[type['name']]['double_damage_from'] = ddf


        ddt = []
        for j in type['damage_relations']['double_damage_to']:
            ddt.append(j['name'])
        types[type['name']]['double_damage_to'] = ddt


        hdf = []
        for j in type['damage_relations']['half_damage_from']:
            hdf.append(j['name'])
        types[type['name']]['half_damage_from'] = hdf


        hdt = []
        for j in type['damage_relations']['half_damage_to']:
            hdt.append(j['name'])
        types[type['name']]['half_damage_to'] = hdt


        mon = []
        for j in type['pokemon']:
            mon.append(j['pokemon']['name'])
        types[type['name']]['pokemon_of_type'] = mon

        moves = []
        for j in type['moves']:
            moves.append(j['name'])
        types[type['name']]['moves_of_type'] = moves

    with open('types.json', 'w') as file: file.write(json.dumps(types))  




if __name__ == '__main__':
    print('starting PokeInfo')
    # grabEmAll()

    # gatherTypes()

    f = open('pokemon.json')
    print('loading json file')
    data = json.load(f)
    f.close() 
    
    g = open('moves.json')
    movesData = json.load(g)
    g.close()

    i = open('items.json')
    itemsData = json.load(i)
    i.close() 

    t = open('types.json')
    typesData = json.load(t)
    t.close() 

    app.run(host="0.0.0.0")