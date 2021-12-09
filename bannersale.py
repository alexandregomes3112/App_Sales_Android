from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class BannerSale(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        # with self.canvas:
        #     Color(rgb=(0,26,51))
        #     self.rec = Rectangle(size=self.size, pos=self.pos)
        # self.bind(pos=self.upd_rec, size=self.upd_rec)

        customer = kwargs['customer']
        photo_customer = kwargs['photo_customer']
        product = kwargs['product']
        photo_product = kwargs['photo_product']
        date = kwargs['date']
        unity = kwargs['unity']
        qty = float(kwargs['qty'])
        price = float(kwargs['price'])

        left = FloatLayout()
        left_image = Image(pos_hint={"right": 1, "top": 0.95}, size_hint=(1, 0.75),
                           source=f'icones/fotos_clientes/{photo_customer}')
        left_label = Label(text=customer, size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2})
        left.add_widget(left_image)
        left.add_widget(left_label)

        middle = FloatLayout()
        middle_image = Image(pos_hint={"right": 1, "top": 0.95}, size_hint=(1, 0.75),
                           source=f'icones/fotos_produtos/{photo_product}')
        middle_label = Label(text=product, size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2})
        middle.add_widget(middle_image)
        middle.add_widget(middle_label)

        right = FloatLayout()
        right_label_data = Label(text=f'Date: {date}', size_hint=(1, 0.3), pos_hint={"right": 1, "top": 0.9})
        right_label_price = Label(text=f'Price: R${price:,.2f}', size_hint=(1, 0.3), pos_hint={"right": 1, "top": 0.65})
        right_label_qty = Label(text=f'Qty: {qty} {unity}', size_hint=(1, 0.3), pos_hint={"right": 1, "top": 0.4})

        right.add_widget(right_label_data)
        right.add_widget(right_label_price)
        right.add_widget(right_label_qty)

        self.add_widget(left)
        self.add_widget(middle)
        self.add_widget(right)

    # def upd_rec(self, *args):
    #     self.rec.pos = self.pos
    #     self.rec.size = self.size