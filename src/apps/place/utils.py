from geopy.distance import distance as geo_distance
def nearby_filter(user_latitude, user_longitude, places):
    try:
        user_location = (float(user_latitude), float(user_longitude))
    except (TypeError, ValueError):
        return []

    nearby_place = []

    for place in places:
        try:
            place_location = (float(place.latitude), float(place.longitude))
            distance_km = round(geo_distance(user_location, place_location).km, 2)
            places_data = {
                'id': place.id,
                'name': place.name,
                'contact': place.contact,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'distance': distance_km,
            }
            nearby_place.append(places_data)
        except (TypeError, ValueError):
            continue

    return sorted(nearby_place, key=lambda x: x['distance'])

