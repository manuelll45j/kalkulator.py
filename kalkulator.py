from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle

class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_color = self.background_color
        self.bind(on_press=self.on_press_effect)
        self.bind(on_release=self.on_release_effect)
        self.background_normal = ''
        self.background_down = ''
        self.shadow_offset = 4
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.3)  # bayangan
            RoundedRectangle(pos=(self.x + self.shadow_offset, self.y - self.shadow_offset),
                             size=self.size, radius=[20])
            r, g, b, a = self.background_color
            Color(r * 0.9, g * 0.9, b * 0.9, a)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            Color(r, g, b, a)
            RoundedRectangle(pos=(self.x, self.y + self.height * 0.3),
                             size=(self.width, self.height * 0.7), radius=[20])

    def on_press_effect(self, instance):
        self.background_color = (
            min(self.original_color[0] + 0.2, 1),
            min(self.original_color[1] + 0.2, 1),
            min(self.original_color[2] + 0.2, 1),
            1
        )
        self.shadow_offset = 1
        Animation.cancel_all(self)
        Animation(size=(self.width * 0.95, self.height * 0.95), d=0.05).start(self)
        self.update_canvas()

    def on_release_effect(self, instance):
        self.background_color = self.original_color
        self.shadow_offset = 4
        Animation.cancel_all(self)
        Animation(size=(self.width / 0.95, self.height / 0.95), d=0.05).start(self)
        self.update_canvas()

class MyApp(App):
    def build(self):
        self.dark_mode = True
        self.history = []

        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        root_widget = BoxLayout(orientation='vertical', padding=15, spacing=15)

        output_label = Label(
            text="",
            size_hint_y=0.75,
            font_size=50,
            color=(1, 1, 1, 1),
            bold=True
        )

        history_label = Label(
            text="Riwayat: ",
            size_hint_y=None,
            height=40,
            font_size=18,
            color=(0.7, 0.7, 0.7, 1)
        )

        button_symbols = (
            '1', '2', '3', '+',
            '4', '5', '6', '-',
            '7', '8', '9', '.',
            '0', '*', '/', '=',
        )

        button_grid = GridLayout(cols=4, size_hint_y=2, spacing=10)

        angka_color = (1, 0, 0, 1)
        operator_color = (0.7, 0, 0, 1)

        def create_button(symbol):
            if symbol.isdigit() or symbol == '.':
                bg_color = angka_color
            else:
                bg_color = operator_color
            return ModernButton(
                text=symbol,
                background_color=bg_color,
                color=(1, 1, 1, 1),
                font_size=32,
                size_hint=(1, 1)
            )

        buttons = {}
        for symbol in button_symbols:
            btn = create_button(symbol)
            button_grid.add_widget(btn)
            buttons[symbol] = btn

        clear_button = ModernButton(
            text='Clear',
            size_hint_y=None,
            height=80,
            background_color=operator_color,
            color=(1, 1, 1, 1),
            font_size=28,
            bold=True
        )

        backspace_button = ModernButton(
            text='⌫',
            size_hint_y=None,
            height=80,
            background_color=operator_color,
            color=(1, 1, 1, 1),
            font_size=28,
            bold=True
        )

        mode_button = ModernButton(
            text='Mode 🌙/☀',
            size_hint_y=None,
            height=80,
            background_color=operator_color,
            color=(1, 1, 1, 1),
            font_size=22,
            bold=True
        )

        def print_button_text(instance):
            if instance.text == '=':
                evaluate_result(instance)
            else:
                output_label.text += instance.text

        for btn in button_grid.children:
            btn.bind(on_press=print_button_text)

        def evaluate_result(instance):
            try:
                hasil = str(eval(output_label.text))
                self.history.append(output_label.text + " = " + hasil)
                history_label.text = "Riwayat: " + " | ".join(self.history[-3:])
                output_label.text = hasil
            except:
                output_label.text = "Error"

        def clear_label(instance):
            output_label.text = ""

        def backspace_label(instance):
            output_label.text = output_label.text[:-1]

        def toggle_mode(instance):
            self.dark_mode = not self.dark_mode
            if self.dark_mode:
                Window.clearcolor = (0.05, 0.05, 0.05, 1)
                output_label.color = (1, 1, 1, 1)
                history_label.color = (0.7, 0.7, 0.7, 1)
            else:
                Window.clearcolor = (1, 1, 1, 1)
                output_label.color = (0, 0, 0, 1)
                history_label.color = (0.3, 0.3, 0.3, 1)

        # Bind tombol bawah
        clear_button.bind(on_press=clear_label)
        backspace_button.bind(on_press=backspace_label)
        mode_button.bind(on_press=toggle_mode)

        # Keyboard support
        def on_key(window, key, scancode, codepoint, modifier):
            if codepoint in "0123456789+-*/.":
                output_label.text += codepoint
            elif codepoint == "\r":  # Enter
                evaluate_result(None)
            elif key == 8:  # Backspace
                backspace_label(None)

        Window.bind(on_text_input=lambda w, t: None)  # Dummy supaya Kivy nggak override
        Window.bind(on_key_down=on_key)

        root_widget.add_widget(output_label)
        root_widget.add_widget(history_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)
        root_widget.add_widget(backspace_button)
        root_widget.add_widget(mode_button)

        return root_widget

MyApp().run()