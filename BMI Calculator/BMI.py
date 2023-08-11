import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, c_int, sizeof
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        # window setup
        super().__init__(fg_color=GREEN)

        # window title and icon
        self.title('BMI Calculator')
        self.iconbitmap('python_dark.ico')
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()

        # layout
        self.columnconfigure(0, weight = 1)
        self.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')

        # data
        self.metric_bool = ctk.BooleanVar(value = True)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value = 65)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()

        # tracing
        self.height_int.trace('w', self.update_bmi)
        self.weight_float.trace('w', self.update_bmi)
        self.metric_bool.trace('w', self.change_units)

        # widgets
        ResutlText(self, self.bmi_string)
        self.weight_input = WeightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)

        # run app
        self.mainloop()
    
    def change_units(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()

    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2, 2)
        self.bmi_string.set(bmi_result)
    
    def change_title_bar_color(self):
        # change the color of the title bar
        try:
            # Get the window handle
            HWND = windll.user32.GetParent(self.winfo_id())
            # Set the color attribute
            DWM_ATTRIBUTE = 35  # DWMWA_NCRENDERING_POLICY
            color = TITLE_HEX_COLOR  # DWMNCRP_USEWINDOWSTYLE
            windll.dwmapi.DwmSetWindowAttribute(
                    HWND,
                    DWM_ATTRIBUTE,
                    byref(c_int(color)),
                    sizeof(c_int)
            )
        except Exception as e:
            print('Exception in changing title bar color:', str(e))

class ResutlText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string : ctk.StringVar):
        font = ctk.CTkFont(family=FONT, size= MAIN_TEXT_SIZE, weight= 'bold')
        super().__init__(master=parent, text=22.5, font=font, text_color=WHITE, textvariable = bmi_string)
        self.grid(row = 0, column = 0, rowspan = 2, sticky = 'nsew')

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float : ctk.DoubleVar, metric_bool : ctk.BooleanVar):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column = 0, row = 2, sticky = 'nsew', padx = 10, pady = 10)
        self.weight_float = weight_float
        self.metric_bool = metric_bool

        # layout
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')

        # text
        self.label_text = ctk.StringVar(value=f'{weight_float.get()} kg')
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, text_color=BLACK, font=font, textvariable = self.label_text)
        label.grid(row = 0, column = 2)

        # buttons
        minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'large')), text = '-', font=font, text_color= BLACK, fg_color=LIGHT_GREY, hover_color=GREY, corner_radius= 6)
        minus_button.grid(row = 0, column = 0, sticky = 'ns', padx = 8, pady = 8)

        plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'large')), text = '+', font=font, text_color= BLACK, fg_color=LIGHT_GREY, hover_color=GREY, corner_radius= 6)
        plus_button.grid(row = 0, column = 4, sticky = 'ns', padx = 8, pady = 8)

        small_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'small')), text = '+', font=font, text_color= BLACK, fg_color=LIGHT_GREY, hover_color=GREY, corner_radius= 6)
        small_plus_button.grid(row = 0, column = 3, padx = 4, pady = 4)

        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'small')), text = '-', font=font, text_color= BLACK, fg_color=LIGHT_GREY, hover_color=GREY, corner_radius= 6)
        small_minus_button.grid(row = 0, column = 1, padx = 4, pady = 4)

    def update_weight(self, info = None):
        if info:
            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16
            
            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        
        if self.metric_bool.get():
            self.label_text.set(f'{round(self.weight_float.get(), 2)} kg')
        else:
            pounds, ounces = divmod(self.weight_float.get() * 2.20462 * 16, 16)
            self.label_text.set(f'{int(pounds)}lb {int(ounces)}oz')

class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int : ctk.IntVar, metric_bool : ctk.BooleanVar):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row = 3, column = 0, sticky = 'nswe', padx = 10, pady = 10)

        self.metric_bool = metric_bool

        # widgets
        slider = ctk.CTkSlider(master= self,
                               button_color=GREEN,
                               button_hover_color=GREY,
                               progress_color=GREEN,
                               fg_color=LIGHT_GREY,
                               variable= height_int,
                               from_ = 100,
                               to = 250,
                               command=self.update_text)
        slider.pack(side = 'left', fill = 'x', expand = True, padx = 10, pady = 10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        ouput_text = ctk.CTkLabel(self, 
                                  text_color=BLACK, 
                                  font= ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE), 
                                  textvariable = self.output_string)
        ouput_text.pack(side = 'left', padx = 20)

    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
        else: # imperial units
            feet, inches = divmod(amount / 2.54, 12)
            self.output_string.set(f'{int(feet)}\'{int(inches)}\"')

class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool : ctk.BooleanVar):
        self.metric_bool = metric_bool
        super().__init__(master=parent, 
                         text='metric', 
                         text_color=DARK_GREEN, 
                         font=ctk.CTkFont(FONT, SWITCH_FONT_SIZE, weight = 'bold')
                         )
        self.place(relx = 0.98, rely = 0.01, anchor = 'ne')
        self.bind('<Button>', self.change_units)

    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text = 'metric')
        else:
            self.configure(text = 'imperial')

if __name__ == '__main__':
    App()