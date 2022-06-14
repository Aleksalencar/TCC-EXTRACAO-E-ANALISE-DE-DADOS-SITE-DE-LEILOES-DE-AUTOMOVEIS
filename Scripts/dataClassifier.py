import csv
from tkinter import N
import requests


def get_brands_id(brand):
    response = requests.get('https://api.fipe.cenarioconsulta.com.br/marcas/1')
    
    brand = brand.lower()
    for response_brand in response.json()['body']:
        if "Citroën" in   response_brand['Marca']:
            response_brand['Marca'] = "citroen"
        
        response_brand_str = response_brand['Marca'].lower()
        if brand in response_brand_str:
            print(response_brand['IdMarca'], response_brand['Marca'])
            return response_brand['IdMarca']
    return None

def get_car_id(id, nome):
    nome = nome.lower().strip()
    print(nome)
    response = requests.get(f'https://api.fipe.cenarioconsulta.com.br/modelos/{id}')
    
    for cont, model in enumerate(response.json()['body']):
        modelo = model['Modelo'].lower().strip()
        if cont == 191:
            pass
        if modelo.startswith(nome):
            print(model)
            pass
    pass
    



file = open("Base_Limpa.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
rows = []

for row in csvreader:
    data = {}
    for field_i in range(len(row)):
        data[header[field_i]] = row[field_i]
    pass
    marca = data["marca"]
    nome = data["nome"].replace(data["marca"], "").strip()
    brand_id = get_brands_id(data["marca"])
    if not brand_id:
        continue
    car_id = get_car_id(brand_id, nome)

    

print(rows)
file.close()