import requests
from kivy.app import App


class MyFirebase():
    API_KEY = 'AIzaSyD2ehQIGrTQxgOHfuFFs4oiCLBu_EQRpXM'

    def create_account(self, email, password):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
        info = {"email": email,
                "password": password,
                "returnSecureToken": True}
        req = requests.post(link, data=info)
        req_dic = req.json()

        if req.ok:
            # requisicao_dic["idToken"] -> autenticação
            # requisicao_dic["refreshToken"] -> token que mantém o usuário logado
            # requisicao_dic["localId"] -> id_usuario
            refresh_token = req_dic['refreshToken']
            local_id = req_dic['localId']
            id_token = req_dic['idToken']

            my_app = App.get_running_app()
            my_app.local_id = local_id
            my_app.id_token = id_token

            with open('refreshtoken.txt', 'w') as file:
                file.write(refresh_token)

            req_id = requests.get(f'https://teste-d03a5.firebaseio.com/prox_id_vendedor.json?auth={id_token}')
            id_salesman = req_id.json()

            link = f'https://teste-d03a5.firebaseio.com/{local_id}.json?auth={id_token}'
            info_user = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_salesman}"}}'
            req_user = requests.patch(link, data=info_user)

            #  upd next id_salesman
            next_id_salesman = int(id_salesman) + 1
            inf_id_salesman = f'{{"prox_id_vendedor": "{next_id_salesman}"}}'
            requests.patch(f'https://teste-d03a5.firebaseio.com/.json?auth={id_token}', data=inf_id_salesman)

            my_app.load_user_info()
            my_app.change_screen('homepage')

        else:
            msg_error = req_dic['error']['message']
            my_app = App.get_running_app()
            pag_login = my_app.root.ids['loginpage']
            pag_login.ids['msg_login'].text = msg_error
            pag_login.ids['msg_login'].color = (1,0,0,1)

    def login(self, email, password):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}'
        info = {"email": email,
                "password": password,
                "returnSecureToken": True}
        req = requests.post(link, data=info)
        req_dic = req.json()
        if req.ok:
            refresh_token = req_dic['refreshToken']
            local_id = req_dic['localId']
            id_token = req_dic['idToken']

            my_app = App.get_running_app()
            my_app.local_id = local_id
            my_app.id_token = id_token

            with open('refreshtoken.txt', 'w') as file:
                file.write(refresh_token)

            my_app.load_user_info()
            my_app.change_screen('homepage')

        else:
            msg_error = req_dic['error']['message']
            my_app = App.get_running_app()
            pag_login = my_app.root.ids['loginpage']
            pag_login.ids['msg_login'].text = msg_error
            pag_login.ids['msg_login'].color = (1,0,0,1)

    def change_token(self, refresh_token):
        link = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'
        info = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        req = requests.post(link, data=info)
        req_dic = req.json()
        local_id = req_dic['user_id']
        id_token = req_dic['id_token']
        return local_id, id_token