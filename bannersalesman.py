from buttons import ImageButton, LabelButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import requests
from kivy.app import App
from functools import partial


class BannerSalesman(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()

        # with self.canvas:
        #     Color(rgb=(0,26,51))
        #     self.rec = Rectangle(size=self.size, pos=self.pos)
        # self.bind(pos=self.upd_rec, size=self.upd_rec)

        id_vendedor = kwargs['id_vendedor']
        link = f'https://teste-d03a5.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"'
        req = requests.get(link)
        req_dic_banner = req.json()
        value = list(req_dic_banner.values())[0]
        avatar = value['avatar']
        total_sales = value['total_vendas']

        my_app = App.get_running_app()

        img = ImageButton(source=f"icones/fotos_perfil/{avatar}",
                          pos_hint={"right": 0.4, "top": 0.9}, size_hint=(0.3, 0.8),
                          on_release=partial(my_app.load_othersalesman, value))
        label_id = LabelButton(text=f"ID Salesman: {id_vendedor}",
                               pos_hint={"right": 0.9, "top": 0.9}, size_hint=(0.5, 0.5),
                               on_release=partial(my_app.load_othersalesman, value))
        label_total = LabelButton(text=f"Total Sales: R${total_sales}",
                                  pos_hint={"right": 0.9, "top": 0.6}, size_hint=(0.5, 0.5),
                                  on_release=partial(my_app.load_othersalesman, value))

        self.add_widget(img)
        self.add_widget(label_id)
        self.add_widget(label_total)

    # def upd_rec(self, *args):
    #     self.rec.pos = self.pos
    #     self.rec.size = self.size