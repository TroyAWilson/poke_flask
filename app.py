from flask import Flask, render_template, url_for, request
import requests
import json
import random

app = Flask(__name__)

def couldNotFindPokemon():
    render_template()

def loadRandomPokemonBatch():
    batch = []
    numsUsed = []
    for p in range(24):
        rand = random.randint(1,898)
        while(rand in numsUsed):
            rand = random.randint(1,898)
        singleRandomMon = data[rand]
        batch.append(singleRandomMon)
        numsUsed.append(rand)
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
    print('collecting pokemon')

    for i in range(1,899):
        pokemonMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}').json()
        pokemonSpeciesMassInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{i}').json()

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
            'evolution_chain': pokemonSpeciesMassInfo['evolution_chain'],
            'flavor_text_entries': pokemonSpeciesMassInfo['flavor_text_entries'],
            'growth_rate': pokemonSpeciesMassInfo['growth_rate'],
            'habitat': pokemonSpeciesMassInfo['habitat'],
            'species': pokemonSpeciesMassInfo['genera'][7]['genus']
        }
        Pokemon.append(pokemon)

    with open('pokemon.json', 'w') as file: file.write(json.dumps(Pokemon))  


if __name__ == '__main__':
    f = open('pokemon.json')
    data = json.load(f)
    f.close() 
    app.run()