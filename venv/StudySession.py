import tkinter
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class StudySession(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (WelcomePage, DefinitionPage, FlashCards):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None



class WelcomePage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        title_font = ('Times', 70)
        button_font = ('Times', 20)
        bolded_font = ('Times 20 bold')
        description_font = ('Times', 20)
        self.file_check = 0
        tkinter.Label(self,
                      text="Welcome\nTo\nStudy Session!",
                      font=title_font,
                      pady=15).grid(row=0,
                                    columnspan=2)
        tkinter.Button(self,
                       text="Definition/Terms",
                       font=button_font,
                       width=15,
                       height=1,
                       fg='SteelBlue2',
                       command=lambda: controller.show_frame('DefinitionPage')).grid(row=2,
                                                                                 column=1)
        tkinter.Button(self,
                       text='Open File',
                       font=button_font,
                       width=15,
                       fg='SteelBlue2',
                       height=1,
                       command=self.file_name).grid(row=2,
                                                    column=0)
        tkinter.Label(self,
                      text='Please enter your Definitions/Terms to get started!',
                      pady=30,
                      font=description_font,
                      fg='grey').grid(row=3,
                                      columnspan=2)
        tkinter.Label(self,
                      text='How to use the program:',
                      font=bolded_font).grid(row=4,
                                             columnspan=2)
        tkinter.Label(self,
                      text='To begin please press the button and enter your information.\n You will be prompted to enter your definition and terms,\n enter up to 20 definitions and terms and you will be\nable to use those in a flash card application.\n Thank you again for using my program!',
                      font=description_font,
                      fg='LightBlue3').grid(row=5,
                                                  columnspan=2)

    def file_name(self):
        self.file_check += 1
        self.definition_page = self.controller.get_page("DefinitionPage")
        ftypes = [('All Files', "*.*")]
        ttl = "Open Flash Cards"
        dir1 = 'C:\\'
        fname = askopenfilename(filetypes=ftypes, initialdir=dir1, title=ttl)
        f = open(fname, 'r')
        f_lines = (sum(1 for line in f))
        self.def_term_lines = int(f_lines / 2)
        f.close()

        f = open(fname, 'r')
        for x in range(self.def_term_lines):
            self.definition_page.filedefinition.append(f.readline().rstrip())
        for x in range(self.def_term_lines):
            self.definition_page.fileterm.append(f.readline().rstrip())
        # print(self.definition_page.filedefinition)
        # print(self.definition_page.fileterm)
        f.close()
        self.controller.show_frame('FlashCards')

class DefinitionPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        description_font = ('Times 15')
        # Initializes and Grids the Label onto the screen
        tkinter.Label(self,
                      font=description_font,
                      text='Enter up to 20 Definitions and Terms:' ).grid(row=0,
                                                                           columnspan=4)
        tkinter.Label(self,
                      text='Definitions').grid(row=1,
                                               column=1)
        tkinter.Label(self,
                      text='Terms').grid(row=1,
                                         column=2)

        tkinter.Button(self,
                       text="Flash Cards",
                       width=25,
                       height=2,
                       command=lambda: controller.show_frame("FlashCards")).grid(row=22,
                                                                                  column=2,
                                                                                  columnspan=3,
                                                                                  pady=10,
                                                                                  padx=20,)
        tkinter.Label(self,
                      fg='red',
                      text='Enter how many Definition/Terms you have entered:').grid(row=22,
                                                                                     column=1,
                                                                                     sticky='w')
        self.flash_len = [tkinter.Entry(self)]
        self.flash_len[0].grid(row=22,
                               column=1,
                               ipadx=10,
                               ipady=5,
                               sticky='e')

        for x in range(20):
            tkinter.Label(self,
                          text=('%s' % (x + 1))).grid(row=x + 2,
                                                      column=0,
                                                      sticky='e')

        #   Creates a list for the definitions to go in for the terms
        self.definition = []
        self.filedefinition = []
        for x in range(20):
            self.definition.append(tkinter.Entry(self))
            self.definition[x].grid(row=x + 2,
                                    column=1,
                                    ipadx=170,
                                    ipady=5,
                                    pady=3)
        #     Creates a list for the terms to go in to the definition
        self.term = []
        self.fileterm = []
        for x in range(20):
            self.term.append(tkinter.Entry(self))
            self.term[x].grid(row=x + 2,
                              column=2,
                              ipady=3,
                              ipadx=35,
                              pady=3,
                              padx=20)

class FlashCards(DefinitionPage):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.count = tkinter.StringVar()
        self.def_flash = tkinter.StringVar()
        self.term_flash = tkinter.StringVar()
        self.term_flash.set('Welcome, click Start to begin!')
        self.count.set('1')
        self.counter = 1

        counter_font = ('Times 20')
        def_font = ('Times 20')
        term_font = ('Times 35')
        btn_font = ('Times 15')

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        tkinter.Label(self,
                      font=counter_font,
                      fg='red4',
                      textvariable=self.count).grid(row=0,
                                                    sticky='w')
        tkinter.Button(self, #Begin Button
                       text='Start',
                       font=btn_font,
                       fg='red4',
                       command=self.update).grid(row=0,
                                                 columnspan=2)
        tkinter.Label(self,
                      font=term_font,
                      fg='IndianRed2',
                      textvariable=self.term_flash).grid(row=1,
                                                         columnspan=2,
                                                         ipady=125)
        tkinter.Label(self,
                      text='------------------------------------------------------------------------------------------------------------------',
                      fg='slate grey').grid(row=1,
                                                                                                                                                  columnspan=2,
                                                                                                                                                  sticky='s')
        tkinter.Label(self,
                      font=def_font,
                      wraplength=650,
                      fg='DeepSkyBlue3',
                      textvariable=self.def_flash).grid(row=2,
                                                        columnspan=2,
                                                        ipady=100,
                                                        sticky='n')
        tkinter.Button(self,
                       text='Next',
                       font=btn_font,
                       fg='red4',
                       command=self.next).grid(row=3,
                                               columnspan=5,
                                               ipadx=30,
                                               ipady=4,
                                               padx=20,
                                               pady=5,
                                               sticky='e')
        tkinter.Button(self,
                       text='Previous',
                       fg='red4',
                       font=btn_font,
                       command=self.previous).grid(row=3,
                                                   columnspan=5,
                                                   ipadx=30,
                                                   ipady=4,
                                                   padx=20,
                                                   pady=5,
                                                   sticky='w')
        tkinter.Button(self,
                       text='Save',
                       fg='slate gray',
                       font=btn_font,
                       command=self.save).grid(row=3,
                                           columnspan=3,
                                           ipadx=30,
                                           ipady=4)
    def update(self):
        self.welcome_page = self.controller.get_page("WelcomePage")
        self.definition_page = self.controller.get_page("DefinitionPage")
        if self.welcome_page.file_check == 1:
            self.def_flash.set(self.definition_page.filedefinition[0])
            self.term_flash.set(self.definition_page.fileterm[0])
        else:
            #   Definition Value
            self.definition_value = self.definition_page.definition[self.counter - 1].get()
            self.def_flash.set(self.definition_value)

            # Term Value
            self.definition_page = self.controller.get_page("DefinitionPage")
            self.term_value = self.definition_page.term[self.counter - 1].get()
            self.term_flash.set(self.term_value)

    def save(self):
        self.definition_page = self.controller.get_page('DefinitionPage')
        self.welcome_page = self.controller.get_page('WelcomePage')
        ftype = [('Text files', '*.txt*', 'TEXT')]
        base = 'FlashCards'
        dir1 = 'C:\\'
        ttl = 'Save'
        file_name = asksaveasfilename(confirmoverwrite=False,
                                      filetypes= ftype,
                                      initialdir= dir1,
                                      initialfile= base,
                                      title = ttl,
                                      defaultextension='.txt')
        if self.welcome_page.file_check == 1:
                tkinter.messagebox.showinfo("Why?",
                                            "Didn't you open this file? Why do you want to re-save it?\nYou're obviously not the brightest tool in the shed \n¯\_(⊙_ʖ⊙)_/¯Just so you know, I didn't save it.")
        else:
            if file_name:
                f = open(file_name, 'w')
                for x in range(int(self.definition_page.flash_len[0].get())):
                    f.write(self.definition_page.definition[x].get() + '\n')
                for x in range(int(self.definition_page.flash_len[0].get())):
                    f.write(self.definition_page.term[x].get() + '\n')

    def next(self):  # Iterates the Flash Card to the next Definition/Term from the DefinitionPage Class
        self.definition_page = self.controller.get_page("DefinitionPage")
        self.welcome_page = self.controller.get_page('WelcomePage')
        # Stops the counter at the top left from ascending too far
        if self.welcome_page.file_check == 1:
            # print(self.counter)
            # print(self.welcome_page.def_term_lines)
            # print(self.definition_page.filedefinition[0])
            # print(self.definition_page.fileterm[0])
            try:
                if self.counter < self.welcome_page.def_term_lines:
                    self.counter += 1
                    self.count.set(self.counter)
                    self.def_flash.set(self.definition_page.filedefinition[self.counter - 1])
                    self.term_flash.set(self.definition_page.fileterm[self.counter - 1])
                else:
                    pass
            # except(NameError):
            #     print('Number Overflow (file)')
            except(ValueError):
                print('Failure to enter how many flash cards you have, please restart the program')
        else:
            try:
                if self.counter < int(self.definition_page.flash_len[0].get()):
                    self.counter += 1
                    self.count.set(str(self.counter))

                    #   Definition Value
                    self.definition_value = self.definition_page.definition[self.counter - 1].get()
                    self.def_flash.set(self.definition_value)
                    # print('Test Definition: ' + self.definition_value)

                    # Term Value
                    self.term_value = self.definition_page.term[self.counter - 1].get()
                    self.term_flash.set(self.term_value)
                    # print('Test Term: ' + self.term_value)
                else:
                    pass
            except(NameError):
                print('Number Overflow')
            except(ValueError):
                print('Failure to enter how many flash cards you have, please restart the program')

    def previous(self): # Deiterates the Flash Card to the next Definition/Term from the DefinitionPage Class

        #   Stops the counter at the top left from descending too far
        self.definition_page = self.controller.get_page("DefinitionPage")
        self.welcome_page = self.controller.get_page('WelcomePage')
        # Stops the counter at the top left from ascending too far

            # print(self.counter)
            # print(self.welcome_page.def_term_lines)
            # print(self.definition_page.filedefinition[0])
            # print(self.definition_page.fileterm[0])
        if self.welcome_page.file_check == 1:
            try:
                if self.counter != 1:
                    self.counter -= 1
                    self.count.set(self.counter)
                    self.def_flash.set(self.definition_page.filedefinition[self.counter - 1])
                    self.term_flash.set(self.definition_page.fileterm[self.counter - 1])
                else:
                    pass
            # except(NameError):
            #     print('Number Overflow (file)')
            except(ValueError):
                print('Failure to enter how many flash cards you have, please restart the program')
        else:
            try:
                if self.counter != 1:
                    self.counter -= 1
                    self.count.set(str(self.counter))
                    #   Definition Value
                    self.definition_page = self.controller.get_page("DefinitionPage")
                    self.definition_value = self.definition_page.definition[self.counter - 1].get()
                    self.def_flash.set(self.definition_value)
                    # print('Test Definition: ' + self.definition_value)

                    # Term Value
                    self.definition_page = self.controller.get_page("DefinitionPage")
                    self.term_value = self.definition_page.term[self.counter - 1].get()
                    self.term_flash.set(self.term_value)
                    # print('Test Term: ' + self.term_value)
                else:
                    pass
            except(NameError):
                print('Number Overflow')

if __name__ == "__main__":
    app = StudySession()
    # app.geometry('990x540')
    app.title('Study Session')
    app.update_idletasks()
    app.iconbitmap(r'C:\Users\ZachP\PycharmProjects\Study_Session\lib\favicon.ico')
    app.mainloop()