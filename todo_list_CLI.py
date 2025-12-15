import os
import sys


class TodoApp:
    def __init__(self):
        self.list_ = []
        self.redo_list_ = []

        self.commands = {
            "/help": self.help_function,
            "/clear": self.clear_function,
            "/del": self.delete_function,
            "/show": self.show_function,
            "/edit": self.edit_function,
            "/done": self.done_function,
            "/add": self.add_function,
            "/undo": self.undo_function,
            "/redo": self.redo_function,
            "/save": self.save_function,
            "/exit": self.exit_function,
            "/search": self.search_function,
            "/priority":self.priority_function,
            "/unpriority":self.unpriority_function,
        }

        self.display_list()

    # ================= HELP LIST =================

    def help_function(self):
        os.system('cls')
        print("-----------------------------------------")
        print("\t\tTO DO LIST")
        print("-----------------------------------------")
        print("\t\tHELP LIST")
        print("-----------------------------------------")
        print("/exit","\tClose the program")
        print("/show","\tShow the list")
        print("/add","\tAdd and element at the positon you want")
        print("/edit","\tEdit an element")
        print("/done","\tMark an task done")
        print("/clear","\tDelets the list")
        print("/del", "\tDelets the elemt you choose")
        print("/undo","\tUndo the last input")
        print("/redo","\tRedo the last undo")
        print("/search","\tSearch in the list")
        print("/priority","\tMarks an elem as priority")
        print("/unpriority","\tMarks an priority elem as non-priority")
        print("/save","\tSaves the list")
        print("-----------------------------------------")

    # ================= FUNCTIONS =================

    def save_function(self):
        if self.empty_list_check() == False:
            return

        user_save_input = input("Do you want to save the todo list? (Y/N): ").strip().upper()
        if user_save_input == "Y":
            file_name = input("How should your list be named?")
            desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_folder, file_name + ".txt")

            with open(file_path, "w") as f:
                for i, item in enumerate(self.list_, start=1):
                    f.write(f"{i}. {item}\n")

            print(f"List saved to {file_path}")
            sys.exit()

        elif user_save_input == "N":
            print("Save cancelled.")
            return True
        else:
            self.display_list()
            print("Invalid answear!Try again.")
            return self.save_function()

    def check_if_empty_input(self, user_input):
        if not user_input.strip():
            self.display_list()
            print("Cant add nothing!")
            return True
        return False

    def check_if_cmd(self, user_input):
        if user_input in self.commands:
            self.commands[user_input]()
            return True
        elif user_input[0] == "/" and user_input not in self.commands:
            self.display_list()
            print("Invalid command!Try again.")
            return True

    def exit_function(self):
        os.system('cls')
        sys.exit()

    def display_list(self):
        os.system('cls')
        print("-----------------------------------------")
        print("\t\tTO DO LIST\n")
        print("\t '/help -> for help'")
        print("-----------------------------------------")
        for i, elem in enumerate(self.list_, start=1):
            print(f"{i}.{elem}")
        print("-----------------------------------------")

    def empty_list_check(self):
        if not self.list_:
            self.display_list()
            print("Cant use command if list is empty")
            return False
        return True

    # ================= COMMANDS =================

    def search_function(self):
        if self.empty_list_check()==False:
            return
        self.display_list()
        srch_input=input("What do you want to search for ?").strip().lower()
        
        if srch_input == "":
            self.display_list()
            print("You cant search nothing!")
            return self.search_function()
        
        found=[]
        for i,elem in enumerate(self.list_,start=1):
            if srch_input in elem.lower():
                found.append(i)
        if found:
            print(f"Found {srch_input} in position:{found}")
        else:
            print(f"The word {srch_input} was not found!")
            

    def priority_function(self):
        if self.empty_list_check() == False:
            return
        try:
            priority_input=int(input("What element do you want to be a priority?"))
        except ValueError:
            self.display_list()
            print("Must use a number!")
            return self.priority_function()
        
        if priority_input < 1 or priority_input > len(self.list_):
            self.display_list()
            print("Please use a valid index!")
            return self.priority_function()

        elif self.list_[priority_input-1].startswith("[!!!]"):
            value=self.list_.pop(priority_input-1)
            self.list_.insert(0,value)
            self.display_list()
            print(f"The element at the positon {priority_input} was prioritized!")
        else:
            value=self.list_.pop(priority_input-1)
            self.list_.insert(0,"[!!!]"+value)
            self.display_list()
            print(f"The element at the positon {priority_input} was prioritized!")

    def unpriority_function(self):
        if self.empty_list_check() == False:
            return
        prefix  = "[!!!]"
        
        if not any(elem.startswith(prefix) for elem in self.list_):
                self.display_list()
                print("You dont have an priority elem!")
                return 
        

        try:
            unpriority_input = int(input("What element do you want to remove priority from? "))
            elem = self.list_[unpriority_input - 1]
            
        except ValueError:
            self.display_list()
            print("Must use a number!")
            return self.unpriority_function()
        
        if unpriority_input < 1 or unpriority_input > len(self.list_):
            self.display_list()
            print("Please use a valid index!")
            return self.unpriority_function()
        

       

        if elem.startswith(prefix):
            clean_elem = elem[len(prefix):]
            self.list_.pop(unpriority_input - 1)
            self.list_.append(clean_elem)
            self.display_list()
            print(f"Priority removed from element at position {unpriority_input}!")
        else:
            self.display_list()
            print("That element is not marked as priority!")
            return self.unpriority_function()


    def show_function(self):
        if self.empty_list_check() == False:
            return
        self.display_list()

    def clear_function(self):
        if self.empty_list_check() == False:
            return
        self.list_.clear()
        self.redo_list_.clear()
        self.display_list()
        print("The list was cleared!")

    def undo_function(self):
        lenght_list_ = len(self.list_)
        if not self.list_:
            self.display_list()
            print("Nothing to undo!")
            return
        self.redo_list_.append(self.list_[lenght_list_ - 1])
        self.list_.pop()
        self.display_list()

    def redo_function(self):
        lenght_list_ = len(self.redo_list_)
        if not self.redo_list_:
            self.display_list()
            print("Nothing to redo!")
            return
        self.list_.append(self.redo_list_[lenght_list_ - 1])
        self.redo_list_.pop()
        self.display_list()

    def add_function(self):
        self.display_list()
        if self.empty_list_check() == False:
            return
        while True:
            try:
                index = int(input("At what position would you like to add?:"))
                if index > len(self.list_) or index < 1:
                    self.display_list()
                    print("Please use an valid index!")
                    continue
                break
            except ValueError:
                self.display_list()
                print("Must use an number!")

        new_elem = input("Write the new element to add:")
        self.list_.insert(index - 1, new_elem)
        self.display_list()

    def edit_function(self):
        self.display_list()
        if self.empty_list_check() == False:
            return
        while True:
            try:
                index = int(input("At what position would you like to replace?:"))
                if index > len(self.list_) or index < 1:
                    self.display_list()
                    print("Please use an valid index!")
                    continue
                break
            except ValueError:
                print("Must use an number!")
                self.display_list()

        new_elem = input("Write the new element to replace:")
        self.list_[index - 1] = new_elem
        os.system('cls')
        print("Element replaced!")
        self.display_list()

    def done_function(self):
        self.display_list()
        if self.empty_list_check() == False:
            return
        while True:
            try:
                index = int(input("Which element to mark done?:"))
                if index > len(self.list_) or index < 1:
                    self.display_list()
                    print("Please use an valid index!")
                    continue
                break
            except ValueError:
                self.display_list()
                print("Must use an number!")

        self.list_[index - 1] = "[DONE] " + self.list_[index - 1]
        os.system('cls')
        self.display_list()

    def delete_function(self):
        if self.empty_list_check() == False:
            return
        self.display_list()
        while True:
            try:
                index = int(input("Which element delete?:"))
                if index > len(self.list_) or index < 1:
                    self.display_list()
                    print("Please use an valid index!")
                    continue
                break
            except ValueError:
                self.display_list()
                print("Must use an number!")

        del self.list_[index - 1]
        os.system('cls')
        print(f"The element at the position {index} was deleted!")
        self.display_list()

    # ================= MAIN LOOP =================

    def run(self):
        while True:
            user_input = input("What do you need to do:")
            if self.check_if_empty_input(user_input):
                continue
            if self.check_if_cmd(user_input):
                continue

            self.list_.append(user_input)
            self.display_list()


# ================= START =================

app = TodoApp()
app.run()
