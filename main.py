from kivy.app import App
from kivy.lang import Builder
from screens import *
from buttons import *
import requests
from bannersale import BannerSale
import os
from functools import partial
from myfirebase import MyFirebase
from bannersalesman import BannerSalesman
from datetime import date


GUI = Builder.load_file("main.kv")


class MainApp(App):
    customer = None
    product = None
    unt = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        # load User Profile Photos
        files = os.listdir('icones/fotos_perfil')
        pg_photoprofile = self.root.ids['photoprofilepage']
        lst_photos = pg_photoprofile.ids['lst_photos_profile']
        for photo in files:
            img = ImageButton(source=f'icones/fotos_perfil/{photo}', on_release=partial(self.change_photo_profile, photo))
            lst_photos.add_widget(img)
        # load user info
        self.load_user_info()

        # load customer photo
        files = os.listdir('icones/fotos_clientes')
        pg_addsalespage = self.root.ids['addsalespage']
        lst_customers = pg_addsalespage.ids['sales_list']
        for photo_cstm in files:
            img = ImageButton(source=f'icones/fotos_clientes/{photo_cstm}',
                              on_release=partial(self.select_customer, photo_cstm))
            label = LabelButton(text=photo_cstm.replace('.png', '').capitalize(),
                                on_release=partial(self.select_customer, photo_cstm))
            lst_customers.add_widget(img)
            lst_customers.add_widget(label)
        # load product photo
        files = os.listdir('icones/fotos_produtos')
        pg_addsalespage = self.root.ids['addsalespage']
        lst_products = pg_addsalespage.ids['product_list']
        for photo_prod in files:
            img = ImageButton(source=f'icones/fotos_produtos/{photo_prod}',
                              on_release=partial(self.select_product, photo_prod))
            label = LabelButton(text=photo_prod.replace('.png', '').capitalize(),
                                on_release=partial(self.select_product, photo_prod))
            lst_products.add_widget(img)
            lst_products.add_widget(label)

        # label date
        pg_addsalespage = self.root.ids['addsalespage']
        label_date = pg_addsalespage.ids['label_date']
        label_date.text = f'Date: {date.today().strftime("%d/%m/%Y")}'

        # load user infos
        self.load_user_info()

    def load_user_info(self):
        try:
            with open('refreshtoken.txt', 'r') as file:
                refresh_token = file.read()
            local_id, id_token = self.firebase.change_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            # get user info
            req = requests.get(f'https://teste-d03a5.firebaseio.com/{self.local_id}.json?auth={self.id_token}')
            req_dic = req.json()

            # fill user photo
            avatar = req_dic['avatar']
            self.avatar = avatar
            photo_profile = self.root.ids['photo_profile']
            photo_profile.source = f'icones/fotos_perfil/{avatar}'

            # fill unique ID
            id_salesman = req_dic['id_vendedor']
            self.id_salesman = id_salesman
            pg_adjust = self.root.ids['adjustpage']
            pg_adjust.ids['id_salesman'].text = f'Your Unique ID: {id_salesman}'

            # fill team
            self.team = req_dic["equipe"]

            # fill total amount
            total_revenue = req_dic['total_vendas']
            self.totalrevenue = total_revenue
            homepage = self.root.ids['homepage']
            homepage.ids['label_total_revenue'].text = f'[color=#000000]Total Revenue:[/color] [b]R${total_revenue}[/b]'

            # fill sales list
            try:
                sales = req_dic['vendas']
                self.sales = sales
                pg_homepage = self.root.ids['homepage']
                sales_list = pg_homepage.ids['sales_list']
                for id_sale in sales:
                    sale = sales[id_sale]
                    banner = BannerSale(customer=sale['cliente'], photo_customer=sale['foto_cliente'],
                                        product=sale['produto'], photo_product=sale['foto_produto'],
                                        date=sale['data'], price=sale['preco'],
                                        unity=sale['unidade'], qty=sale['qtde'])

                    sales_list.add_widget(banner)

            except:
                pass

            # fill salesman team
            team = req_dic['equipe']
            lst_team = team.split(",")
            pg_listsalespage = self.root.ids['listsalespage']
            lst_salesman = pg_listsalespage.ids['list_salesman']

            for id_salesman_team in lst_team:
                if id_salesman_team != '':
                    banner_salesman = BannerSalesman(id_vendedor=id_salesman_team)
                    lst_salesman.add_widget(banner_salesman)

            self.change_screen('homepage')

        except:
            pass

    def change_screen(self, id_screen):
        scrn_mngr = self.root.ids['screen_manager']
        scrn_mngr.current = id_screen

    def change_photo_profile(self, photo, *args):
        photo_profile = self.root.ids['photo_profile']
        photo_profile.source = f'icones/fotos_perfil/{photo}'

        info = f'{{"avatar": "{photo}"}}'
        req = requests.patch(f'https://teste-d03a5.firebaseio.com/{self.local_id}.json?auth={self.id_token}',
                             data=info)
        self.change_screen('adjustpage')

    def add_salesman(self, id_salesman_added):
        link = f'https://teste-d03a5.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_salesman_added}"'
        req = requests.get(link)
        req_dic = req.json()

        pg_addsalesman = self.root.ids["addsalesmanpage"]
        msg_txt = pg_addsalesman.ids["msg_other_salesman"]

        if req_dic == {}:
            msg_txt.text = "User Not Found"
        else:
            team = self.team.split(",")
            if id_salesman_added in team:
                msg_txt.text = "Seller is already part of the team"
            else:
                self.team = self.team + f',{id_salesman_added}'
                info = f'{{"equipe": "{self.team}"}}'
                requests.patch(f'https://teste-d03a5.firebaseio.com/{self.local_id}.json?auth={self.id_token}',
                               data=info)
                msg_txt.text = "Seller Added Successfully"
                # add new banner salesman list
                pg_listsalespage = self.root.ids['listsalespage']
                lst_salesman = pg_listsalespage.ids['list_salesman']
                banner_salesman = BannerSalesman(id_vendedor=id_salesman_added)
                lst_salesman.add_widget(banner_salesman)

    def select_customer(self, photo, *args):
        self.customer = photo.replace('.png', '')
        pg_addsalespage = self.root.ids['addsalespage']
        lst_customers = pg_addsalespage.ids['sales_list']

        for item in list(lst_customers.children):
            item.color = (1, 1, 1, 1)
            try:
                text = item.text
                text = text.lower() + '.png'
                if photo == text:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def select_product(self, photo, *args):
        self.product = photo.replace('.png', '')
        pg_addsalespage = self.root.ids['addsalespage']
        lst_products = pg_addsalespage.ids['product_list']

        # color all itens in white
        for item in list(lst_products.children):
            item.color = (1, 1, 1, 1)
            try:
                text = item.text
                text = text.lower() + '.png'
                # color selected
                if photo == text:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def select_und(self, id_label, *args):
        self.unt = id_label.replace('un_', '')
        pg_addsales = self.root.ids['addsalespage']
        pg_addsales.ids['un_kg'].color = (1, 1, 1, 1)
        pg_addsales.ids['un_un'].color = (1, 1, 1, 1)
        pg_addsales.ids['un_lt'].color = (1, 1, 1, 1)

        # color blue for item selected
        pg_addsales.ids[id_label].color = (0, 207/255, 219/255, 1)

    def add_sale(self):
        customer = self.customer
        product = self.product
        unt = self.unt
        pg_addsales = self.root.ids['addsalespage']
        data = pg_addsales.ids['label_date'].text.replace('Date: ', '')
        preco = pg_addsales.ids['total_price'].text
        qtde = pg_addsales.ids['qty'].text

        if not customer:
            pg_addsales.ids['label_select_customer'].color = (1, 0, 0, 1)
        if not product:
            pg_addsales.ids['label_select_product'].color = (1, 0, 0, 1)
        if not unt:
            pg_addsales.ids['un_kg'].color = (1, 0, 0, 1)
            pg_addsales.ids['un_un'].color = (1, 0, 0, 1)
            pg_addsales.ids['un_lt'].color = (1, 0, 0, 1)
        if not preco:
            pg_addsales.ids['label_price'].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pg_addsales.ids['label_price'].color = (1, 0, 0, 1)
        if not qtde:
            pg_addsales.ids['label_qty'].color = (1, 0, 0, 1)
        else:
            try:
                qtde = float(qtde)
            except:
                pg_addsales.ids['label_qty'].color = (1, 0, 0, 1)
        if customer and product and unt and preco and qtde and (type(preco) == float) and (type(qtde) == float):
            photo_prod = product + '.png'
            photo_cstmr = customer + '.png'

            info = f'{{"cliente": "{customer}", "produto": "{product}", "foto_cliente": "{photo_cstmr}", ' \
                   f'"foto_produto": "{photo_prod}", "data": "{data}", "unidade": "{unt}", ' \
                   f'"preco": "{preco}", "qtde": "{qtde}"}}'
            requests.post(f'https://teste-d03a5.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}', data=info)

            banner = BannerSale(customer=customer, product=product, photo_customer=photo_cstmr, photo_product=photo_prod,
                                date=data, unity=unt, qty=qtde, price=preco)
            pg_homepage = self.root.ids['homepage']
            sales_list = pg_homepage.ids['sales_list']
            sales_list.add_widget(banner)

            req = requests.get(f'https://teste-d03a5.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}')
            total_sale = float(req.json())
            total_sale += preco
            info = f'{{"total_vendas": "{total_sale}"}}'
            requests.patch(f'https://teste-d03a5.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data=info)
            homepage = self.root.ids['homepage']
            homepage.ids['label_total_revenue'].text = f'[color=#000000]Total Revenue:[/color] [b]R${total_sale}[/b]'
            self.change_screen('homepage')

        self.customer = None
        self.product = None
        self.unt = None

    def load_all_sales(self):
        # load company data
        pg_totalrevenue = self.root.ids['totalrevenuepage']
        sales_list = pg_totalrevenue.ids['sales_list']

        for item in list(sales_list.children):
            sales_list.remove_widget(item)

        req = requests.get(f'https://teste-d03a5.firebaseio.com/.json?orderBy="id_vendedor"')
        req_dic = req.json()

        # fill company photo
        photo_profile = self.root.ids['photo_profile']
        photo_profile.source = 'icones/fotos_perfil/seal.png'

        total_revenue = 0
        for local_id_user in req_dic:
            try:
                vendas = req_dic[local_id_user]['vendas']
                for id_venda in vendas:
                    sale = vendas[id_venda]
                    total_revenue += float(sale['preco'])
                    banner = BannerSale(customer=sale['cliente'], photo_customer=sale['foto_cliente'],
                                        product=sale['produto'], photo_product=sale['foto_produto'],
                                        date=sale['data'], price=sale['preco'],
                                        unity=sale['unidade'], qty=sale['qtde'])
                    sales_list.add_widget(banner)
            except:
                pass

        # fill total amount
        pg_totalrevenue.ids['label_total_revenue'].text = f'[color=#000000]Total Revenue:[/color] [b]R${total_revenue}[/b]'

        self.change_screen('totalrevenuepage')

    def exit_all_sales(self, id_screen):
        photo_profile = self.root.ids['photo_profile']
        photo_profile.source = f'icones/fotos_perfil/{self.avatar}'

        self.change_screen(id_screen)

    def load_othersalesman(self, dic_info_salesman, *args):
        try:
            vendas = dic_info_salesman['vendas']
            pg_salesothersalesman = self.root.ids['salesothersalesman']
            sales_list = pg_salesothersalesman.ids['sales_list_other']

            # clear old sales
            for item in list(sales_list.children):
                sales_list.remove_widget(item)

            for id_venda in vendas:
                sale = vendas[id_venda]
                banner = BannerSale(customer=sale['cliente'], photo_customer=sale['foto_cliente'],
                                    product=sale['produto'], photo_product=sale['foto_produto'],
                                    date=sale['data'], price=sale['preco'],
                                    unity=sale['unidade'], qty=sale['qtde'])
                sales_list.add_widget(banner)
        except:
            pass

        # fill total revenue
        total_revenue = dic_info_salesman['total_vendas']
        pg_salesothersalesman.ids['label_total_revenue'].text = f'[color=#000000]Total Revenue:[/color] [b]R${total_revenue}[/b]'

        # load picture profile
        photo_profile = self.root.ids['photo_profile']
        avatar = dic_info_salesman['avatar']
        photo_profile.source = f'icones/fotos_perfil/{avatar}'

        self.change_screen('salesothersalesman')


MainApp().run()
