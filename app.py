import random

from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request

from Source.Source import s
app = Flask(__name__)
s = s.replace('­', '')
s = s.replace(',', '')

Dict = s.split()
Words = []
Colors = []
ran = []
string = ''
for i in range(25):
    Colors.append(['olive', 'gray', 0])
    ran.append(i)
    a = random.choice(Dict)
    Words.append(a)
    Dict.pop(Dict.index(a))
for i in range(9):
    a = random.choice(ran)
    Colors[a][1] = 'red'
    ran.pop(ran.index(a))
for i in range(8):
    a = random.choice(ran)
    Colors[a][1] = 'navy'
    ran.pop(ran.index(a))
a = random.choice(ran)
Colors[a][1] = 'black'
print(Colors)
q = ['2313']


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/captain')
def captain():
    return render_template('Captain.html', Words=Words, Colors=Colors)


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', Words=Words, Colors=Colors, str=string)


@app.route('/execute_cell/<cell_id>', methods=['POST'])
def execute(cell_id=None):
    cell_id = int(cell_id)
    if (Colors[cell_id][2] == 0):
        Colors[cell_id][2] += 1
    return redirect(url_for('main'))


app.run(debug=True)
