from shapely.geometry import Point, Polygon
from alem.zone import *

def create_zone(name,coordinates):
    coords = coord_parse(coordinates)
    return Zone(Polygon(coords),name)

def get_zones_by_coordintes(lat,lng):
    # p1 = Point(49.894835,73.202145)
    point = Point(lat,lng)
    all_zones = create_zones()

    for zone in all_zones:
        if point.within(zone.polygon):
           return zone.name
    return None




def calculate_price(from_zone,to_zone):
        # print('calculate_price',from_zone,' ', to_zone)

        if from_zone == None:
           return None 
        if to_zone == None:
           return None 

        # print(from_zone,'  ',to_zone)



        price = None
        
        try:
            price = price_dict[from_zone+" "+to_zone]
            # price = price + '₸ ('+from_zone +' → '+to_zone+')'
            return price
        except:
            price = None

        try:
            price = price_dict[to_zone+" "+from_zone]
            # price = price + '₸ ('+from_zone +' → '+to_zone+')'
            return price
        except:
            price = None


        return price


def get_price_by_route_alem(routes):

    result = None

    if len(routes) == 2:
        result = [] 
        from_zone = get_zones_by_coordintes(routes[0][1], routes[0][0],)    
        to_zone =  get_zones_by_coordintes(routes[1][1], routes[1][0])   
        price = calculate_price(from_zone,to_zone)
        result.append({
                            "price":price,
                            "tariff_name":"Эконом"
                            })

    return result

   