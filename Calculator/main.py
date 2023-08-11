import darkdetect
from settings import *
from PIL import Image
import customtkinter as ctk
from buttons import Button, ImageButton, NumButton, MathButton
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        
        # setup
        super().__init__(fg_color=(WHITE, BLACK))
        if is_dark:
            self._set_appearance_mode('dark')
        else:
            self._set_appearance_mode('light')
        
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+900+100')
        self.resizable(False, False)
        self.title('Calculator')
        self.iconbitmap('icon.ico')
        self.title_bar_color(is_dark)

        # layout
        self.columnconfigure(tuple(range(MAIN_COLUMNS)), weight=1, uniform='a')
        self.rowconfigure(tuple(range(MAIN_ROWS)), weight=1, uniform='a')

        # data
        self.result_string = ctk.StringVar(value = '0')
        self.farmula_string = ctk.StringVar(value = '')
        self.display_nums = []
        self.full_operation = []

        # Widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        # fonts
        main_font = ctk.CTkFont(family= FONT, size = NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family= FONT, size = OUTPUT_FONT_SIZE)

        # output labels
        OutputLabel(self, 0, 'se', main_font, self.farmula_string) # farmula label
        OutputLabel(self, 1, 'e', result_font, self.result_string) # result label

        # clear (AC) button
        Button(
            parent=self,
            text=OPERATORS['clear']['text'],
            func=self.clear,
            col=OPERATORS['clear']['col'],
            row=OPERATORS['clear']['row'],
            font=main_font,
        )

        # percent (%) button
        Button(
            parent=self,
            text=OPERATORS['percent']['text'],
            func=self.percent,
            col=OPERATORS['percent']['col'],
            row=OPERATORS['percent']['row'],
            font=main_font,
        )

        # invert button
        Button(
            parent=self,
            func=self.invert,
            text=OPERATORS['invert']['text'],
            col=OPERATORS['invert']['col'],
            row=OPERATORS['invert']['row'],
            font=main_font,
        )

        # Number Buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent = self,
                text= num,
                func=self.num_press,
                col=data['col'],
                row=data['row'],
                span=data['span'],
                font=main_font
            )

        # Math buttons
        for operator, data in MATH_POSTIONS.items():
            MathButton(
                parent=self,
                text=data['character'],
                operator=operator,
                func=self.math_press,
                col=data['col'],
                row=data['row'],
                font=main_font
            )
    
    def math_press(self, operator):
        current_number = ''.join(self.display_nums)

        if current_number:
            self.full_operation.append(current_number)
            self.display_nums.clear()

            if operator != '=':
                # update data
                self.full_operation.append(operator)
                # self.display_nums.clear()

                # update output
                self.result_string.set('')
                self.farmula_string.set(' '.join(self.full_operation))
            else:
                farmula = ' '.join(self.full_operation)
                result = eval(farmula)

                # format result
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)

                # update output and data
                self.result_string.set(result)
                self.farmula_string.set(farmula)
                self.full_operation.clear()
                self.display_nums.append(str(result))


    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number)
    
    def clear(self):
        self.display_nums.clear()
        self.full_operation.clear()
        self.result_string.set('0')
        self.farmula_string.set('')

    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percentage = current_number / 100
            self.display_nums = list(str(percentage))
            self.result_string.set(percentage)

    def invert(self):
        current_number = ''.join(self.display_nums)

        if current_number:
            if float(current_number) > 0:
                self.display_nums.insert(0, '-')
            else:
                del self.display_nums[0]
            # update output
            self.result_string.set(''.join(self.display_nums))

    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLOR['dark'] if is_dark else TITLE_BAR_HEX_COLOR['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, sticky, font, string_var):
        super().__init__(master = parent, font= font, textvariable = string_var, anchor='e')
        self.grid(column = 0, columnspan = 4, row = row, sticky = sticky, padx = 10)

if __name__ == "__main__":
    Calculator(darkdetect.isDark())
    # Calculator(False)