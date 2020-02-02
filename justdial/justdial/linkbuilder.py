import csv

def get_all_city():
    city_names = []
    with open('justdial\cities.csv') as file:
        data = csv.reader(file)
        for city_name in data:
            city_names.append(city_name[0])
    
    return city_names


def get_all_category():
    category_names = []
    with open('justdial\category.csv') as file:
        data = csv.reader(file)
        for category_name in data:
            category_names.append(category_name[0])
    
    return category_names


def link_builder():
    build_links = []
    
    for nt in get_all_city():
        for mt in get_all_category():
            URL = 'https://www.justdial.com/'
            build_links.append(URL+nt+"/"+mt)

    return build_links
        