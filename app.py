from flask import Flask, render_template, url_for, request
import requests
import json
import random

app = Flask(__name__)

def loadRandomPokemonBatch():
    batch = []
    for p in range(24):
        rand = random.randint(1,898)
        singleRandomMon = data[rand]
        batch.append(singleRandomMon)
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
            return render_template('pokemon.html', Pokemon = i)

    return render_template('error.html')

#get to pokemon page by pokedex number
@app.route('/pokemon/<num>')
def pokebynum(num = None):
    num = int(num)
    for i in data:
        if i['id'] == num:
            print(i['evolution_chain'])
            return render_template('pokemon.html', Pokemon = i)
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


def grabEmAll():
    Pokemon=[]
    evChainList = []
    print('collecting pokemon')

    for i in range(1,899):
        pokemonMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}').json()
        pokemonSpeciesMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{i}').json()
        ev_chain = requests.get(pokemonSpeciesMassInfo['evolution_chain']['url']).json()

        evChain = {
            'smallestMon': None,
            'smallestMonId': None,
            'midMon': None,
            'midMonId': None,
            'bigMon': None,
            'bigMonId': None,
            'altMon': None,
            'altMonId': None

        }

        if 'name' in ev_chain['chain']['species']:
            evChain['smallestMon'] = ev_chain['chain']['species']['name']
            smallurl = ev_chain['chain']['species']['url']
            getOne = requests.get(smallurl).json()
            evChain['smallestMonId'] = getOne['id']

        if len(ev_chain['chain']['evolves_to']) > 0:
            evChain['midMon'] = ev_chain['chain']['evolves_to'][0]['species']['name']
            midurl = ev_chain['chain']['evolves_to'][0]['species']['url']
            getOne = requests.get(midurl).json()
            evChain['midMonId'] = getOne['id']
        
            if len(ev_chain['chain']['evolves_to'][0]['evolves_to']) > 0:
                evChain['bigMon'] = ev_chain['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
                bigurl = ev_chain['chain']['evolves_to'][0]['evolves_to'][0]['species']['url']
                getOne = requests.get(bigurl).json()
                evChain['bigMonId'] = getOne['id']
        
                if len(ev_chain['chain']['evolves_to'][0]['evolves_to']) > 1:
                    evChain['altMon'] = ev_chain['chain']['evolves_to'][0]['evolves_to'][1]['species']['name']
                    alturl = ev_chain['chain']['evolves_to'][0]['evolves_to'][1]['species']['url']
                    getOne = requests.get(alturl).json()
                    evChain['altMonId'] = getOne['id']

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
            # 'evolution_chain': ev_chain,
            'flavor_text_entries': pokemonSpeciesMassInfo['flavor_text_entries'],
            'growth_rate': pokemonSpeciesMassInfo['growth_rate'],
            'habitat': pokemonSpeciesMassInfo['habitat'],
            'species': pokemonSpeciesMassInfo['genera'][7]['genus']
        }
        Pokemon.append(pokemon)

    with open('pokemon.json', 'w') as file: file.write(json.dumps(Pokemon))  


if __name__ == '__main__':
    # grabEmAll()
    f = open('pokemon.json')
    data = json.load(f)
    f.close() 
    app.run()