from flask import Flask, render_template, url_for, request
import requests
import random

app = Flask(__name__)


def couldNotFindPokemon():
    render_template()

def loadPokemonBatch(pokeInfo):
    
    batch = []

    for p in pokeInfo['results']:
        singleMon = requests.get(p['url'])
        singleMon = singleMon.json()
        mon = {
            'name': singleMon['forms'][0]['name'],
            'id': singleMon['id']
        }
        batch.append(mon)

    return batch


def loadRandomPokemonBatch():
    batch = []

    for p in range(12):
        rand = random.randint(1,898)
        singleRandomMon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{rand}')
        singleRandomMon = singleRandomMon.json()
    
        mon = {
            'name': singleRandomMon['forms'][0]['name'],
            'id': singleRandomMon['id']
        }
        batch.append(mon)
    return batch


@app.route('/')
def index():
    batch = loadRandomPokemonBatch()
    return render_template('index.html', batch=batch)

#gets to pokemon page by pokemon name
@app.route('/<name>')
def pokebyname(name = None):
    pokemonInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokedexEntry = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}')
    
    if pokemonInfo.status_code != 200:
        return render_template('error.html')
    
    pokemonInfo = pokemonInfo.json()
    pokedexEntry = pokedexEntry.json()

    return render_template('pokemon.html', PokedexNum = pokemonInfo['id'], PokeInfo = pokemonInfo, Pokedex=pokedexEntry)

#get to pokemon page by pokedex number
@app.route('/<num>')
def pokebynum(num = None):
    pokemonInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}')
    pokedexEntry = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{num}')
    pokemonInfo = pokemonInfo.json()
    pokedexEntry = pokedexEntry.json()

    return render_template('pokemon.html', PokedexNum = num, PokeInfo = pokemonInfo, Pokedex=pokedexEntry)

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

if __name__ == '__main__':
    app.run()