#library
import json
import sqlite3
import os


def insert_invoice(cursor, meta):
    version = meta.get('version')
    split = meta.get('split')
    image_id = meta.get('image_id')
    image_size = meta.get('image_size', {})
    width = image_size.get('width')
    height = image_size.get('height')

    cursor.execute('''
    INSERT INTO invoices (version, split, image_id, image_width, image_height)
    VALUES (?, ?, ?, ?, ?)
    ''', (version, split, image_id, width, height))

    return image_id

# Fonction pour insérer une ligne et retourner son ID
def insert_line(cursor, invoice_id, line):
    category = line.get('category')
    group_id = line.get('group_id')


    cursor.execute('''
    INSERT INTO lines (invoice_id, category, group_id)
    VALUES (?, ?, ?)
    ''', (invoice_id, category, group_id))

    return cursor.lastrowid

# Fonction pour insérer un mot
def insert_word(cursor, line_id, word):
    quad = word.get('quad', {})
    x1 = quad.get('x1')
    y1 = quad.get('y1')
    x2 = quad.get('x2')
    y2 = quad.get('y2')
    x3 = quad.get('x3')
    y3 = quad.get('y3')
    x4 = quad.get('x4')
    y4 = quad.get('y4')
    is_key = word.get('is_key')
    row_id = word.get('row_id')
    text = word.get('text')

    cursor.execute('''
    INSERT INTO words (
        line_id,row_id,text,is_key,x1, y1, x2, y2,
        x3, y3, x4, y4
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        line_id,row_id,text,is_key,x1, y1, x2, y2,
        x3, y3, x4, y4,
    ))


def create_database(name):
  # Connexion à la base de données
  conn = sqlite3.connect(name)
  cursor = conn.cursor()

  # Création de la table invoices
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS invoices (
      image_id INTEGER PRIMARY KEY,
      version TEXT,
      split TEXT,
      image_width INTEGER,
      image_height INTEGER
  )
  ''')

  # Création de la table lines
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS lines (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      invoice_id INTEGER,
      category TEXT,
      group_id INTEGER,
      FOREIGN KEY (invoice_id) REFERENCES invoices(image_id)
  )
  ''')

  # Création de la table words
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS words (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      line_id INTEGER,
      row_id INTEGER,
      text TEXT,
      is_key INTEGER,
      x1 INTEGER,
      y1 INTEGER,
      x2 INTEGER,
      y2 INTEGER,
      x3 INTEGER,
      y3 INTEGER,
      x4 INTEGER,
      y4 INTEGER,
      FOREIGN KEY (line_id) REFERENCES lines(id)
  )
  ''')


  # Sauvegarde des modifications et fermeture de la connexion
  conn.commit()
  conn.close()


def insert_data(json_folder,name):
  # Connexion à la base de données
  conn = sqlite3.connect(name)
  cursor = conn.cursor()
  # Parcours de tous les fichiers JSON dans le dossier
  for filename in os.listdir(json_folder):
      if filename.endswith('.json'):
          filepath = os.path.join(json_folder, filename)
          with open(filepath, 'r', encoding='utf-8') as f:
              data = json.load(f)

              # Insertion de la facture
              meta = data.get('meta', {})
              invoice_id = insert_invoice(cursor, meta)

              # Insertion des lignes
              valid_lines = data.get('valid_line', [])
              for line in valid_lines:
                  line_id = insert_line(cursor, invoice_id, line)

                  # Insertion des mots
                  words = line.get('words', [])
                  for word in words:
                      insert_word(cursor, line_id, word)
                      
  # Sauvegarde des modifications et fermeture de la connexion
  conn.commit()
  conn.close()
