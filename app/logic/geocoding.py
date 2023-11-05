from ..models.localization import AddressBase
import httpx

# https://medium.com/@benshearlaw/how-to-use-httpx-request-client-with-fastapi-16255a9984a4

class Geocoder:
    def get_lat_lon(address: AddressBase) -> tuple[float, float]:
        """ Returns tuple consisting of latitude and longitude based on given address"""
        req_url = f"https://geocode.maps.co/search?country={address.country}&street={address.street_number,address.street}&city={address.city}&postalcode={address.postal_code}"
        response = httpx.get(req_url)
        if response.status_code == 200:
            if response.json():
                lat = float(response.json()[0]['lat'])
                lon = float(response.json()[0]['lon'])
                response =  {'lat': lat, 'lon':lon}
            else:
                response = {'status_code': response.status_code, 'response': 'Address not found.'}
            
        else:
            response = {"status_code": response.status_code, "response": response.text}

        return response
    
    def get_address(lat: float, lon: float) -> AddressBase:
        """Returns address based on lattitude and longitude"""

        req_url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}"
        response = httpx.get(req_url)

        if response.status_code == 200:
            address_json = response.json()['address']
            country = address_json['country']
            city = address_json['city']
            street = address_json['road']
            street = address_json['road']
            postal_code = address_json['postcode']
            street_number = address_json['house_number']

            address = AddressBase(country=country,
                                city=city,
                                street=street,
                                postal_code=postal_code,
                                street_number=street_number,
                                latitude= lat,
                                longitude= lon
                                )
            return address
        
        else:
            return {"status_code": response.status_code, "body": response.text}
