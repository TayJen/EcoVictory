import csv

def read_data(filepath):
    
    food_supplements = {}

    with open(filepath, encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter = ";")
        # Считывание данных из CSV файла
        vari = 0
        for row in file_reader:
            print(row)
            vari += 1
            if vari == 1:
                continue
            
            key = str(row[1].lower()).replace('е', 'e')
            food_supplements[key] ={}
            food_supplements[key]["id"] = row[0]
            food_supplements[key]["name"] = row[1]
            food_supplements[key]["extend_name"] = row[2]
            food_supplements[key]["link"] = row[3]
            food_supplements[key]["danger"] = row[4]
            food_supplements[key]["danger_2"] = row[5]
            food_supplements[key]["full_name"] = row[6]
            food_supplements[key]["type_2"] = row[7]
            food_supplements[key]["used_in"] = row[8]
            food_supplements[key]["health_impact"] = row[9]

    return food_supplements

if __name__ == "__main__":
    filepath = 'data/version_2.csv'
    print(read_data(filepath))