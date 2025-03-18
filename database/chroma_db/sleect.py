
import sqlite3
from prettytable import PrettyTable

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('./database/chroma_db/chroma.sqlite3')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Executar um comando SQL para listar todas as tabelas
cursor.execute("SELECT * FROM embeddings WHERE type='table';")
tables = cursor.fetchall()

# Criar um objeto PrettyTable para exibir as tabelas de forma organizada
table = PrettyTable()
table.field_names = ["Tabelas"]

# Adicionar as tabelas ao PrettyTable
for row in tables:
    table.add_row(row)

# Mostrar a tabela
print(table)

# Fechar a conexão
conn.close()
