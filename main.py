
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp
from kivy.core.window import Window

class SkladApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('sklad.json')
        self.current_screen = "main"
        
    def build(self):
        # Устанавливаем черный фон приложения
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Темно-серый/черный
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.show_main_screen()
        return self.main_layout
    
    def clear_main_layout(self):
        self.main_layout.clear_widgets()
    
    def show_main_screen(self, instance=None):
        self.clear_main_layout()
        self.current_screen = "main"
        
        # Заголовок
        title = Label(
            text='СКЛАД', 
            size_hint=(1, 0.15), 
            font_size=dp(24),
            bold=True,
            color=(1, 1, 1, 1)  # Белый текст
        )
        self.main_layout.add_widget(title)
        
        # Кнопки главного меню
        btn_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=dp(15))
        
        add_btn = Button(
            text='ДОБАВИТЬ ТОВАР', 
            on_press=self.show_add_screen, 
            size_hint=(1, 0.3),
            background_color=(0.2, 0.5, 0.8, 1),  # Синий
            color=(1, 1, 1, 1),  # Белый текст
            font_size=dp(18)
        )
        btn_layout.add_widget(add_btn)
        
        search_btn = Button(
            text='ПОИСК ТОВАРА', 
            on_press=self.show_search_screen, 
            size_hint=(1, 0.3),
            background_color=(0.3, 0.6, 0.3, 1),  # Зеленый
            color=(1, 1, 1, 1),  # Белый текст
            font_size=dp(18)
        )
        btn_layout.add_widget(search_btn)
        
        show_btn = Button(
            text='ВЕСЬ СКЛАД', 
            on_press=self.show_all_screen, 
            size_hint=(1, 0.3),
            background_color=(0.8, 0.5, 0.2, 1),  # Оранжевый
            color=(1, 1, 1, 1),  # Белый текст
            font_size=dp(18)
        )
        btn_layout.add_widget(show_btn)
        
        self.main_layout.add_widget(btn_layout)
        
        # Статистика
        stats = self.get_stats()
        stats_label = Label(
            text=stats, 
            size_hint=(1, 0.2),
            font_size=dp(16),
            color=(0.8, 0.8, 0.8, 1)  # Светло-серый текст
        )
        self.main_layout.add_widget(stats_label)
    
    def show_add_screen(self, instance):
        self.clear_main_layout()
        self.current_screen = "add"
        
        # Заголовок
        title = Label(
            text='ДОБАВЛЕНИЕ ТОВАРА', 
            size_hint=(1, 0.1), 
            font_size=dp(20),
            bold=True,
            color=(1, 1, 1, 1)  # Белый текст
        )
        self.main_layout.add_widget(title)
        
        # Поля ввода
        input_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing=dp(8))
        
        # Общие настройки для всех полей ввода
        textinput_style = {
            'size_hint': (1, 0.2),
            'multiline': False,
            'padding': dp(15),
            'font_size': dp(16),
            'background_color': (0.2, 0.2, 0.2, 1),  # Темный фон
            'foreground_color': (1, 1, 1, 1),  # Белый текст
            'hint_text_color': (0.6, 0.6, 0.6, 1)  # Серый подсказка
        }
        
        self.firma_input = TextInput(
            hint_text='Фирма (например: Добрый)', 
            **textinput_style
        )
        input_layout.add_widget(self.firma_input)
        
        self.obiem_input = TextInput(
            hint_text='Объем (например: 0.25)', 
            **textinput_style,
            input_type='number',  # Только числа
            input_filter='float'  # Разрешаем десятичные числа
        )
        input_layout.add_widget(self.obiem_input)
        
        self.vkus_input = TextInput(
            hint_text='Вкус (например: апельсиновый)', 
            **textinput_style
        )
        input_layout.add_widget(self.vkus_input)
        
        self.kol_input = TextInput(
            hint_text='Количество', 
            **textinput_style
        )
        input_layout.add_widget(self.kol_input)
        
        self.main_layout.add_widget(input_layout)
        
        # Кнопки
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=dp(10))
        
        add_btn = Button(
            text='ДОБАВИТЬ', 
            on_press=self.add_sok,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=dp(16),
            color=(1, 1, 1, 1)  # Белый текст
        )
        btn_layout.add_widget(add_btn)
        
        back_btn = Button(
            text='НАЗАД', 
            on_press=lambda x: self.show_main_screen(),
            background_color=(0.6, 0.6, 0.6, 1),
            font_size=dp(16),
            color=(1, 1, 1, 1)  # Белый текст
        )
        btn_layout.add_widget(back_btn)
        
        self.main_layout.add_widget(btn_layout)
    
    def show_search_screen(self, instance):
        self.clear_main_layout()
        self.current_screen = "search"
        
        # Заголовок
        title = Label(
            text='ПОИСК ТОВАРА', 
            size_hint=(1, 0.1), 
            font_size=dp(20),
            bold=True,
            color=(1, 1, 1, 1)  # Белый текст
        )
        self.main_layout.add_widget(title)
        
        # Поля фильтрации
        filter_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.25), spacing=dp(8))
        
        # Получаем уникальные значения для фильтров
        firmas = self.get_unique_values('firma')
        obiems = self.get_unique_values('obiem')
        vkusy = self.get_unique_values('vkus')
        
        # Простой стиль для Spinner - контрастный
        spinner_style = {
            'size_hint': (1, 0.33),
            'font_size': dp(16),
            'background_color': (0.3, 0.3, 0.3, 1),  # Темно-серый фон самого Spinner
            'color': (1, 1, 1, 1),  # Белый текст Spinner
            'background_normal': '',  # Убираем стандартный фон
            'background_down': ''     # Убираем стандартный фон при нажатии
        }
        
        self.search_firma = Spinner(
            text='Любая фирма', 
            values=['Любая фирма'] + firmas, 
            **spinner_style
        )
        filter_layout.add_widget(self.search_firma)
        
        self.search_obiem = Spinner(
            text='Любой объем', 
            values=['Любой объем'] + obiems, 
            **spinner_style
        )
        filter_layout.add_widget(self.search_obiem)
        
        self.search_vkus = Spinner(
            text='Любой вкус', 
            values=['Любой вкус'] + vkusy, 
            **spinner_style
        )
        filter_layout.add_widget(self.search_vkus)
        
        self.main_layout.add_widget(filter_layout)
        
        # Кнопки поиска
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=dp(10))
        
        search_btn = Button(
            text='НАЙТИ', 
            on_press=self.search_sok,
            background_color=(0.3, 0.7, 0.3, 1),  # Зеленый
            font_size=dp(16),
            color=(1, 1, 1, 1)  # Белый текст
        )
        btn_layout.add_widget(search_btn)
        
        show_all_btn = Button(
            text='ВСЕ ТОВАРЫ', 
            on_press=self.show_all_products_in_search,
            background_color=(0.8, 0.5, 0.2, 1),  # Оранжевый
            font_size=dp(16),
            color=(1, 1, 1, 1)  # Белый текст
        )
        btn_layout.add_widget(show_all_btn)
        
        back_btn = Button(
            text='НАЗАД', 
            on_press=lambda x: self.show_main_screen(),
            background_color=(0.6, 0.6, 0.6, 1),  # Серый
            font_size=dp(16),
            color=(1, 1, 1, 1)  # Белый текст
        )
        btn_layout.add_widget(back_btn)
        
        self.main_layout.add_widget(btn_layout)
        
        # Область результатов
        scroll = ScrollView(size_hint=(1, 0.5))
        self.results_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(5))
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        self.main_layout.add_widget(scroll)
        
        self.show_all_products_in_search()
    
    def show_all_screen(self, instance=None):
        """Показывает весь склад"""
        self.clear_main_layout()
        self.current_screen = "all"
        
        title = Label(
            text='ВЕСЬ СКЛАД', 
            size_hint=(1, 0.1), 
            font_size=dp(20),
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)
        
        # Кнопки управления
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=dp(10))
        
        clear_btn = Button(
            text='ОЧИСТИТЬ СКЛАД', 
            on_press=self.confirm_clear,
            background_color=(0.8, 0.3, 0.3, 1),
            font_size=dp(16),
            color=(1, 1, 1, 1)
        )
        btn_layout.add_widget(clear_btn)
        
        back_btn = Button(
            text='НАЗАД', 
            on_press=lambda x: self.show_main_screen(),
            background_color=(0.6, 0.6, 0.6, 1),
            font_size=dp(16),
            color=(1, 1, 1, 1)
        )
        btn_layout.add_widget(back_btn)
        
        self.main_layout.add_widget(btn_layout)
        
        # Область результатов
        scroll = ScrollView(size_hint=(1, 0.75))
        self.all_results_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(5))
        self.all_results_layout.bind(minimum_height=self.all_results_layout.setter('height'))
        scroll.add_widget(self.all_results_layout)
        self.main_layout.add_widget(scroll)
        
        self.show_all_products()
    
    def add_sok(self, instance):
        # Получаем и форматируем данные
        firma = self.format_text(self.firma_input.text.strip())
        obiem_text = self.obiem_input.text.strip()
        vkus = self.format_text(self.vkus_input.text.strip())
        kol = self.kol_input.text.strip()
        
        if not all([firma, obiem_text, vkus, kol]):
            self.show_popup('ОШИБКА', 'Заполните все поля!')
            return
        
        # Проверяем что объем - число
        try:
            obiem = float(obiem_text.replace(',', '.'))  # Заменяем запятую на точку
            if obiem <= 0:
                self.show_popup('ОШИБКА', 'Объем должен быть больше 0!')
                return
        except ValueError:
            self.show_popup('ОШИБКА', 'Введите число в объеме!\nНапример: 0.25 или 1.5')
            return
        
        try:
            kol_int = int(kol)
            if kol_int <= 0:
                self.show_popup('ОШИБКА', 'Количество должно быть больше 0!')
                return
        except ValueError:
            self.show_popup('ОШИБКА', 'Введите число в количестве!')
            return
        
        # Создаем уникальный ключ
        key = f"{firma}|{obiem}|{vkus}"
        
        # Форматируем объем для отображения
        obiem_display = f"{obiem} л"
        
        # Используем ключ
        if key in self.store:
            current = self.store.get(key)
            new_kol = current['quantity'] + kol_int
            self.store.put(key, firma=firma, obiem=obiem_display, vkus=vkus, quantity=new_kol)
            message = f'ОБНОВЛЕНО: {firma} {obiem_display} {vkus}\nНОВОЕ КОЛИЧЕСТВО: {new_kol}'
        else:
            self.store.put(key, firma=firma, obiem=obiem_display, vkus=vkus, quantity=kol_int)
            message = f'ДОБАВЛЕНО: {firma} {obiem_display} {vkus}\nКОЛИЧЕСТВО: {kol_int}'
        
        self.show_popup('УСПЕХ', message)
        self.clear_inputs()
        self.show_main_screen()

    def format_text(self, text):
        """Форматирует текст: каждое слово с заглавной буквы, убирает лишние пробелы"""
        if not text:
            return text
        
        # Убираем пробелы в начале и конце
        text = text.strip()
        
        # Заменяем множественные пробелы на один
        text = ' '.join(text.split())
        
        # Каждое слово с заглавной буквы
        return ' '.join(word.capitalize() for word in text.split())
    
    def search_sok(self, instance=None):
        firma_filter = self.search_firma.text
        obiem_filter = self.search_obiem.text
        vkus_filter = self.search_vkus.text
        
        # Очищаем результаты
        self.results_layout.clear_widgets()
        
        found_count = 0
        for key in self.store.keys():
            item = self.store.get(key)
            
            # Применяем фильтры
            if firma_filter != 'Любая фирма' and item['firma'] != firma_filter:
                continue
            if obiem_filter != 'Любой объем' and item['obiem'] != obiem_filter:
                continue
            if vkus_filter != 'Любой вкус' and item['vkus'] != vkus_filter:
                continue
            
            found_count += 1
            card = self.create_product_card(key, item)
            self.results_layout.add_widget(card)
        
        if found_count == 0:
            no_results = Label(
                text='Товары не найдены', 
                size_hint_y=None, 
                height=dp(80),
                font_size=dp(18),
                color=(0.5, 0.5, 0.5, 1)
            )
            self.results_layout.add_widget(no_results)
        else:
            header = Label(
                text=f'Найдено товаров: {found_count}', 
                size_hint_y=None, 
                height=dp(40),
                font_size=dp(16),
                bold=True,
                color=(0.3, 0.3, 0.3, 1)
            )
            self.results_layout.add_widget(header)
    
    def show_all_products_in_search(self, instance=None):
        self.results_layout.clear_widgets()
        self.show_all_products_target(self.results_layout)
    
    def show_all_products(self):
        self.all_results_layout.clear_widgets()
        self.show_all_products_target(self.all_results_layout)
    
    def show_all_products_target(self, target_layout):
        keys = self.store.keys()
        if not keys:
            empty_label = Label(
                text='Склад пуст\n\nДобавьте первый товар!', 
                size_hint_y=None, 
                height=dp(120),
                font_size=dp(18),
                color=(0.5, 0.5, 0.5, 1)
            )
            target_layout.add_widget(empty_label)
            return
        
        # Заголовок
        header = Label(
            text=f'Всего товаров: {len(keys)}', 
            size_hint_y=None, 
            height=dp(40),
            font_size=dp(16),
            bold=True,
            color=(0.3, 0.3, 0.3, 1)
        )
        target_layout.add_widget(header)
        
        for key in sorted(keys):
            item = self.store.get(key)
            card = self.create_product_card(key, item)
            target_layout.add_widget(card)
    
    def confirm_delete_product(self, product_key):
        """Подтверждение удаления товара"""
        # Получаем информацию о товаре для сообщения
        item = self.store.get(product_key)
        product_info = f"{item['firma']} {item['obiem']} {item['vkus']}"
        
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(
            text=f'Удалить товар?\n\n{product_info}\nКоличество: {item["quantity"]} шт.',
            font_size=dp(16)
        ))
        
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=dp(10))
        
        # Создаем попап сначала
        popup = Popup(
            title='ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ', 
            content=content, 
            size_hint=(0.8, 0.5)
        )
        
        yes_btn = Button(
            text='ДА, УДАЛИТЬ', 
            on_press=lambda x: self.delete_product(product_key, popup),
            background_color=(0.9, 0.3, 0.3, 1)
        )
        btn_layout.add_widget(yes_btn)
        
        no_btn = Button(
            text='НЕТ, ОСТАВИТЬ', 
            on_press=popup.dismiss,  # Просто закрываем попап
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_layout.add_widget(no_btn)
        
        content.add_widget(btn_layout)
        popup.open()
    
    def refresh_current_screen(self):
        """Обновляет текущий экран"""
        if self.current_screen == "all":
            self.show_all_screen()
        elif self.current_screen == "search":
            self.show_search_screen()

    def delete_product(self, product_key, popup=None):
        """Удаление товара"""
        # Закрываем попап если он передан
        if popup:
            popup.dismiss()
        
        if product_key in self.store:
            item = self.store.get(product_key)
            product_info = f"{item['firma']} {item['obiem']} {item['vkus']}"
            
            self.store.delete(product_key)
            self.show_popup('✅ УДАЛЕНО', f'Товар удален:\n{product_info}')
            
            # Небольшая задержка перед обновлением, чтобы попап успел закрыться
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.refresh_current_screen(), 0.1)
        else:
            self.show_popup('❌ ОШИБКА', 'Товар не найден!')
    
    def create_product_card(self, key, item):
        # Основная карточка
        card = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=dp(100),
            spacing=dp(5),
            padding=dp(10),
        )

        # Добавляем фон через canvas с привязкой к размерам
        with card.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.2, 0.2, 0.2, 1)  # Темно-серый цвет
            card.rect = Rectangle(pos=card.pos, size=card.size)
        
        # Привязываем обновление фона при изменении размера/позиции
        card.bind(pos=self.update_card_rect, size=self.update_card_rect)
        
        # Верхняя строка - фирма и кнопка удаления
        top_row = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        
        firma_label = Label(
            text=item['firma'],
            font_size=dp(18),
            bold=True,
            color=(1, 1, 1, 1),  # Белый текст
            halign='left'
        )
        firma_label.bind(size=firma_label.setter('text_size'))
        top_row.add_widget(firma_label)
        
        # Кнопка удаления (крестик)
        delete_btn = Button(
            text='×',
            size_hint_x=0.07,       # Очень узкая
            size_hint_y=0.7,        # Не на всю высоту
            font_size=dp(22),       # Крупный крестик
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            padding=[dp(0), dp(0)], # Минимальные отступы
        )
        delete_btn.bind(on_press=lambda x, k=key: self.confirm_delete_product(k))
        top_row.add_widget(delete_btn)
        
        card.add_widget(top_row)
        
        # Нижняя строка - объем, вкус и количество
        bottom_row = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        
        details_label = Label(
            text=f"{item['obiem']} • {item['vkus']}",
            font_size=dp(22),
            color=(0.8, 0.8, 0.8, 1),  # Светло-серый
            halign='left'
        )
        details_label.bind(size=details_label.setter('text_size'))
        bottom_row.add_widget(details_label)
        
        qty_label = Label(
            text=f"{item['quantity']} шт.",
            font_size=dp(16),
            color=(0.4, 0.7, 1, 1),  # Голубой
            size_hint_x=0.3
        )
        bottom_row.add_widget(qty_label)
        
        card.add_widget(bottom_row)
        
        return card

    def update_card_rect(self, card, *args):
        """Обновляет фон карточки при изменении размера/позиции"""
        if hasattr(card, 'rect'):
            card.rect.pos = card.pos
            card.rect.size = card.size

    def confirm_clear(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(
            text='Вы уверены, что хотите\nочистить весь склад?\nЭто действие нельзя отменить!',
            font_size=dp(16)
        ))
        
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=dp(10))
        
        # Создаем попап сначала
        popup = Popup(
            title='ПОДТВЕРЖДЕНИЕ ОЧИСТКИ', 
            content=content, 
            size_hint=(0.8, 0.4)
        )
        
        yes_btn = Button(
            text='ДА, ОЧИСТИТЬ', 
            on_press=lambda x: self.clear_all(popup),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_layout.add_widget(yes_btn)
        
        no_btn = Button(
            text='НЕТ, ОТМЕНА', 
            on_press=popup.dismiss,  # Просто закрываем попап
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_layout.add_widget(no_btn)
        
        content.add_widget(btn_layout)
        popup.open()
    
    def clear_all(self, popup=None):
        """Очистка всего склада"""
        # Закрываем попап если он передан
        if popup:
            popup.dismiss()
        
        for key in list(self.store.keys()):
            self.store.delete(key)
        
        self.show_popup('✅ УСПЕХ', 'Склад очищен!')
        
        # Обновляем текущий экран
        if self.current_screen == "all":
            self.show_all_screen()
        else:
            self.show_main_screen()
    
    def clear_inputs(self):
        self.firma_input.text = ''
        self.obiem_input.text = ''
        self.vkus_input.text = ''
        self.kol_input.text = ''
    
    def get_stats(self):
        keys = self.store.keys()
        if not keys:
            return "Склад пуст"
        
        total_items = sum(self.store.get(key)['quantity'] for key in keys)
        return f"Всего позиций: {len(keys)}\nОбщее количество: {total_items} шт."
    
    def get_unique_values(self, field):
        values = set()
        for key in self.store.keys():
            item = self.store.get(key)
            values.add(item[field])
        return sorted(list(values))
    
    def show_popup(self, title, message):
        # Простой контейнер без фона
        content = BoxLayout(
            orientation='vertical', 
            padding=dp(15), 
            spacing=dp(15)
        )
        
        # Текст сообщения
        message_label = Label(
            text=message, 
            font_size=dp(16),
            color=(1, 1, 1, 1)  # Белый текст
        )
        content.add_widget(message_label)
        
        # Кнопка OK
        ok_btn = Button(
            text='OK', 
            size_hint=(1, 0.3),
            background_color=(0.2, 0.5, 0.8, 1),  # Синий
            color=(1, 1, 1, 1)  # Белый текст
        )
        
        # Создаем попап с темным фоном
        popup = Popup(
            title=title, 
            content=content, 
            size_hint=(0.8, 0.4),
            background_color=(0.1, 0.1, 0.1, 1)  # Темный фон попапа
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        content.add_widget(ok_btn)
        
        popup.open()

if __name__ == '__main__':
    SkladApp().run()