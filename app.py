from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
DATA_FILE = 'notes.json'

def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(DATA_FILE, 'w') as f:
        json.dump(notes, f)

@app.route('/')
def index():
    notes = load_notes()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        notes = load_notes()
        notes.append({'title': request.form['title'], 'content': request.form['content']})
        save_notes(notes)
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_note(index):
    notes = load_notes()
    if request.method == 'POST':
        notes[index]['title'] = request.form['title']
        notes[index]['content'] = request.form['content']
        save_notes(notes)
        return redirect('/')
    return render_template('edit.html', note=notes[index], index=index)

@app.route('/delete/<int:index>')
def delete_note(index):
    notes = load_notes()
    notes.pop(index)
    save_notes(notes)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
