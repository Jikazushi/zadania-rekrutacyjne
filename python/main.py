# Z podanego zbioru danych wyselekcjonuj 5 o największej wartości na jednostkę, znając kategorię obiektu
# Dane znajdują się w folderze "dane" w pliku "zbiór_wejściowy.json" oraz "kategorie.json"
# Wynik przedstaw w czytelnej formie na standardowym wyjściu
import json

# 1ct = 0.2 grams
# 1oz = 31.1 grams
CARAT = 0.2
OUNCE = 0.0352739619

def get_mass(s):
    if(s[-1] == 't'):
        s = s[:-2].replace(',','.')
        s = round(float(s)*CARAT, 2)
    else:
        s = s[:-1].replace(',','.')
        s = round(float(s), 2)

    return s

def get_price(type, cls):
    with open('dane/kategorie.json', encoding='utf-8') as fh:
        catalogue = json.load(fh)

    for line in catalogue:
        if line['Typ'] == type and line['Czystość'] == cls:
            return line['Wartość za uncję (USD)']

def main():
    
    with open('dane/kategorie.json', encoding='utf-8') as fh:
        catalogue = json.load(fh)

    with open('dane/zbiór_wejściowy.json', encoding='utf-8') as fh:
        input = json.load(fh)

    top5 = [-1,-2,-3,-4,-5]
    output = [{}] * 5

    values = []
    for line in input:
            mass = get_mass(line['Masa'])
            price = get_price(line['Typ'], line['Czystość'])
            if price == None:
                continue

            #convert to price per gram
            price = price * OUNCE
            value = price * mass

            if value > min(top5):
                index = top5.index(min(top5))
                top5[index] = value
                output[index] = line

    i = 0
    for line in output:
        line.update({'Price': round(top5[i], 2)})
        i += 1

    newlist = sorted(output, key=lambda d: d['Price'])

    for line in newlist:
        print(line['Typ'], line['Masa'], line["Czystość"], line['Właściciel'], 'wartość:', line['Price'],'zł')
                     
if __name__ == '__main__':
    main()