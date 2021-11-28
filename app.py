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
    pokemonInfo = pokemonInfo.json()

    return render_template('pokemon.html', PokedexNum = pokemonInfo['id'], PokeInfo = pokemonInfo)

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