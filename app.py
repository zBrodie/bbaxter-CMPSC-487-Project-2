from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database initialization
def init_db():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, image TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'id')  # Default sort by ID
    search_query = request.args.get('search', '')  # Get search query from URL parameters
    conn = sqlite3.connect('items.db')
    c = conn.cursor()

    if search_query:
        # If search query is provided, filter items by ID, name, or description containing the search query
        c.execute('SELECT * FROM items WHERE id LIKE ? OR name LIKE ? OR description LIKE ? ORDER BY {}'.format(sort_by),
                  ('%{}%'.format(search_query), '%{}%'.format(search_query), '%{}%'.format(search_query)))
    else:
        # If no search query, retrieve all items and sort them based on the selected attribute
        c.execute('SELECT * FROM items ORDER BY {}'.format(sort_by))

    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items, search_query=search_query)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    description = request.form['description']
    image = request.form['image']
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (name, description, image) VALUES (?, ?, ?)', (name, description, image))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.form['image']
        c.execute('UPDATE items SET name=?, description=?, image=? WHERE id=?', (name, description, image, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute('SELECT * FROM items WHERE id=?', (item_id,))
        item = c.fetchone()
        conn.close()
        return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete(item_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
