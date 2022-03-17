
from get_content import get_data

products = {
    'VinoTinto':'https://www.vinoteca.com/vinos/tinto',
    'VinoBlanco':'https://www.vinoteca.com/vinos/blanco',
    'VinosRosado':'https://www.vinoteca.com/vinos/rosado',
    'Vinos':'https://www.vinoteca.com/vinos/jerez-oporto-vinos-de-postre',
    'Mezcal':'https://www.vinoteca.com/destilados/mezcal/',
    'Tequila':'https://www.vinoteca.com/destilados/tequila',
    'Whiskey':'https://www.vinoteca.com/destilados/whisky/',
    'Ron':'https://www.vinoteca.com/destilados/ron',
    'CremasYlicores':'https://www.vinoteca.com/destilados/licor',
    'Cognag':'https://www.vinoteca.com/destilados/cognac---brandy',
    'Ginebra':'https://www.vinoteca.com/destilados/ginebra',
    'Vodka':'https://www.vinoteca.com/destilados/vodka'
            }

count = 0

for type, url in products.items():
    if count == 0:
        get_data(type, url).to_csv('vinoteca_precios.csv', index=False)
    else:
        get_data(type, url).to_csv('vinoteca_precios.csv', mode='a', index=False, header=False)
    count += 1



