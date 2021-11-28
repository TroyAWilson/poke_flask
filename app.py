from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<name>')
def pokebyname(name = None):
    pokemonInfo = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokemonInfo = pokemonInfo.json()

    # for key in pokemonInfo['stats']:
    #     print(key['stat']['name'])
    #     print(key['base_stat'])


    return render_template('pokemon.html', PokedexNum = pokemonInfo['id'], PokeInfo = pokemonInfo, name = name)

#get to pokemon page by pokedex number
@app.route('/<num>')
def pokebynum(num = None):
    return render_template('pokemon.html', PokedexNum = num)

