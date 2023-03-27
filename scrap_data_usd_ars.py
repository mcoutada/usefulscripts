import requests
from bs4 import BeautifulSoup
import pandas as pd
# from tabulate import tabulate

url = "https://www.cronista.com/MercadosOnline/dolar.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find_all("table")[0]
df = pd.read_html(str(table))[0]


# Convert all values in your dataframe to string
df = df.astype(str)

out_df = pd.DataFrame()

out_df[0] = df[0]
out_df.rename(columns={0: 'Dolar'}, inplace=True)


for j in range(len(df.columns)):
    for i in range(len(df)):
        curr_cell_val = df.iloc[i, j]
        if j in [1, 2]:
            if "$" in curr_cell_val:
                col_name, cell_value = curr_cell_val.split("$")
                out_df.at[i, col_name] = cell_value.replace(',', '.')

        # if "%" in curr_cell_val:
        #     col_name, cell_value = "Variacion", curr_cell_val
        #     out_df.at[i, col_name] = cell_value

        if "Actualizado: " in curr_cell_val:
            col_name, cell_value = (
                "Fecha Cotizacion",
                curr_cell_val.split("Actualizado: ")[1],
            )
            out_df.at[i, col_name] = cell_value

# set column 0 as row index
# out_df = out_df.set_index(0)

# print(df)
out_df['Punto Medio'] = (pd.to_numeric(out_df['Compra']) + pd.to_numeric(out_df['Venta'])) / 2

row = out_df[out_df['Dolar'].str.contains('BLUE')]
usd = 500
cot = row['Punto Medio'].values[0]
# row.to_string(index=False)
# print(tabulate(row, headers='keys', tablefmt='psql',showindex=False))
row_data = ''
for col in row.columns:
    row_data+=f'{col}: {row[col].values[0]}\n'

print(
    f'''
{url}

{row_data}

{usd} USD * {cot} ARS/USD = ARS$ {usd*cot}
''')
