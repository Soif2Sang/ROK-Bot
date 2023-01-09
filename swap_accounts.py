with open('proton_accounts.txt') as f:
    lines = f.readlines()
final_accounts = [(line.split(" ")[0],line.split(" ")[1]) for line in lines]
print(final_accounts)

import tkinter


class ButtonAdb(tkinter.Button):
    def __init__(self, master, index,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(command=lambda : print(index))

app = tkinter.Tk()
i = 1
for element in final_accounts:
    ButtonAdb(master=app, index=i, text=f"{i} - {element[0]}").pack()
    i += 1

app.mainloop()