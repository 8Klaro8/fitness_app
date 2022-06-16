import requests
import json



class MyFireBase():
    wak = 'AIzaSyCmDTaaINrZtn6HmA-Kb9hTgnBCaZmEABM'   # web api key
    def sign_up(self, email, password):
        # Send email and password to firebase
        # Firebase will return localId, authToken, refreshToken
        signup_url = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={self.wak}'
        signup_data = {"email": email, "password": password, "returnSecureToken": True}
        print(email, password)
    def sign_in(self):
        pass