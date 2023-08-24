

def normalize_countries(countries, new_min, new_max):
    sizes = [countries[key]["size"] for key in countries.keys()]
    min_value = min(sizes)
    max_value = max(sizes)

    for key in countries.keys():
        new_size = int((countries[key]["size"] - min_value) / (max_value - min_value) * (new_max - new_min) + new_min + 0.5)
        countries[key]["size"] = new_size

    return countries
