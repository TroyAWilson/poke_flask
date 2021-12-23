from flask import Flask, render_template, url_for, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#gets to pokemon page by pokemon name
@app.route('/<name>')
def pokebyname(name = None):
    pokemonInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokedexEntry = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}')
    pokemonInfo = pokemonInfo.json()
    pokedexEntry = pokedexEntry.json()

    # evolution_chain = requests.get(pokedexEntry['evolution_chain']['url'])
    # evolution_chain = evolution_chain.json()

    print(pokedexEntry['egg_groups'][0]['name'])   

    return render_template('pokemon.html', PokedexNum = pokemonInfo['id'], PokeInfo = pokemonInfo, Pokedex=pokedexEntry)

#get to pokemon page by pokedex number
@app.route('/<num>')
def pokebynum(num = None):
    return render_template('pokemon.html', PokedexNum = num)

#function for search bar to get page of the new pokemon being serached
@app.route('/getNewPokemon', methods = ["GET", "POST"])
def getNewPokemon():
    if request.method == "POST":
        name = request.form.get("newName")     
        return pokebyname(name)
    return "Uh oh, something has gone wrong!"

if __name__ == '__main__':
    app.run()