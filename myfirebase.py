import requests
import json
from kivy.app import App
import os
from dotenv import load_dotenv
load_dotenv()



class MyFireBase():
    wak = os.environ.get('wak')   # web api key
    def sign_up(self, email, password):
        app = App.get_running_app()
        # Send email and password to firebase
        # Firebase will return localId, authToken, refreshToken
        signup_url = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={self.wak}'
        signup_data = {"email": email, "password": password, "returnSecureToken": True}
        signup_request = requests.post(url=signup_url, data=signup_data)

        if signup_request.ok == True:
            # Get localId, refreshToken, idToken
            # TODO - Solve the next problem:
            #  {'error': 'Invalid path: Path specified exceeds the maximum length that can be written (768 bytes).'}
            idToken = json.loads(signup_request.content.decode())['idToken']
            refresh_token = json.loads(signup_request.content.decode())['refreshToken']
            localId = json.loads(signup_request.content.decode())['localId']

            # Save refresh token to a txt file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # Save localId, idToken to app
            app.local_id = localId
            app.id_token = idToken


            # Create new key in database with localId
            # Get friend ID
            # Default avatar
            # Friends list
            # Empty workouts are
            my_data = '{"avatar": "avatar_pic_girl.png", "friends": "", "workouts": ""}'
            my_patch = requests.patch(
                'https://friendly-fitness-9b323-default-rtdb.firebaseio.com/' + localId + '.json?auth=' + idToken,
            data=my_data)
            print(my_patch.ok)
            print(json.loads(my_patch.content.decode()))

        print(signup_request.ok)
        print(signup_request.text)

        if signup_request.ok == False:
            error_data = json.loads(signup_request.content.decode())
            app.root.ids['login_screen'].ids['login_message'].text = error_data['error']['message']
            # print(error_data['error']['message'])
    def sign_in(self):
        pass

    def exchange_refresh_token(self, refresh_token):
        refresh_url = 'https://securetoken.googleapis.com/v1/token?key=' + self.wak
        refresh_playload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(url=refresh_url, data=refresh_playload)
        print("Was the request ok?: " + f"{refresh_req.ok}")
        print(refresh_req.json())

        local_id = refresh_req.json()['user_id']
        id_token = refresh_req.json()['id_token']




        return local_id, id_token