
from get_content import get_data

products = {
    'Vinos': 'https://www.vinoteca.com/vinos',
    'Mezcal': 'https://www.vinoteca.com/destilados/mezcal/',
    'Tequila': 'https://www.vinoteca.com/destilados/tequila',
    'Whiskey': 'https://www.vinoteca.com/destilados/whisky/',
    'Ron': 'https://www.vinoteca.com/destilados/ron',
    'CremasYlicores': 'https://www.vinoteca.com/licor?_q=licor&map=ft',
    'Cognag': 'https://www.vinoteca.com/cognac?_q=cognac&map=ft',
    'Ginebra': 'https://www.vinoteca.com/destilados/ginebra',
    'Vodka': 'https://www.vinoteca.com/destilados/vodka'
}

# products = {
#     'Vinos': 'https://www.vinoteca.com/vinos'
# }

count = 0

for type, url in products.items():
    if count == 0:
        get_data(type, url).to_csv('vinoteca_precios.csv', index=False)
    else:
        get_data(type, url).to_csv('vinoteca_precios.csv', mode='a', index=False, header=False)
    count += 1

