import tkinter as tk
from tkinter import messagebox
import json
import requests

class ManageProfilePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent 
        
        # create label for page title
        title_label = tk.Label(self, text="Edit and Delete the address", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # create labels and entry fields for user information
        username_label = tk.Label(self, text="Username:", font=("Arial", 12))
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        
        email_label = tk.Label(self, text="Company:", font=("Arial", 12))
        email_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.company_entry = tk.Entry(self, width=30)
        self.company_entry.grid(row=2, column=1, padx=10, pady=5)
        
        password_label = tk.Label(self, text="Country:", font=("Arial", 12))
        password_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.country_entry = tk.Entry(self, width=30)
        self.country_entry.grid(row=3, column=1, padx=10, pady=5)
        
        password_label = tk.Label(self, text="State:", font=("Arial", 12))
        password_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.state_entry = tk.Entry(self, width=30)
        self.state_entry.grid(row=4, column=1, padx=10, pady=5)
        
        password_label = tk.Label(self, text="City:", font=("Arial", 12))
        password_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        self.city_entry = tk.Entry(self, width=30)
        self.city_entry.grid(row=5, column=1, padx=10, pady=5)
        
        password_label = tk.Label(self, text="Address:", font=("Arial", 12))
        password_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)
        self.address_entry = tk.Entry(self, width=30)
        self.address_entry.grid(row=6, column=1, padx=10, pady=5)
        
        password_label = tk.Label(self, text="Phone number:", font=("Arial", 12))
        password_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.E)
        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=5)
        
        password_label = tk.Label(self, text="Postal code:", font=("Arial", 12))
        password_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.E)
        self.postal_entry = tk.Entry(self, width=30)
        self.postal_entry.grid(row=8, column=1, padx=10, pady=5)
  
        # create save button
        edit_button = tk.Button(self, text="Edit", font=("Arial", 12), command=self.save_changes)
        edit_button.grid(row=9, column=0, columnspan=1, pady=20)
        
        delete_button = tk.Button(self, text="Delete", font={"Arial",12},command = self.delete_changes)
        delete_button.grid(row=9, column=1, columnspan=3, pady=0)
        
    def save_changes(self):
        # save changes to user information
        new_add = {
            "name":self.username_entry.get(),
            "company":self.company_entry.get(),
            "country":self.country_entry.get(),
            "state":self.state_entry.get(),
            "city":self.city_entry.get(),
            "address":self.address_entry.get(),
            "phone_number":self.phone_entry.get(),
            "postal_code":self.postal_entry.get()
        }
        name  = new_add["name"]
        r1 = requests.put("http://127.0.0.1:8000/customer/address/",data=json.dumps(new_add))
        res1 = json.loads(r1.text)   
        # show message box indicating changes have been saved
        if  res1 == {"data":"Unable to edit address. Please try again"}:
            messagebox.showinfo(title='Error',message="You don't have account in this system. Please try again")
            print(r1.json())
        else:
            r2 = requests.get(f"http://127.0.0.1:8000/customer/address?name={name}")
            res2 = json.loads(r2.text)
            messagebox.showinfo(title='Notice',message=f"Success edit the address {res2['data']}")
            print(r2.json())
            
    def delete_changes(self):
        # save changes to user information
        user_info = {
            "name":self.username_entry.get()
        }
        name = user_info['name']
        r = requests.delete("http://127.0.0.1:8000/customer/address",data=json.dumps(user_info))
        res = json.loads(r.text)
        # show message box indicating changes have been saved
        if  res == {"data":"Unable to delete the address"}:
            messagebox.showinfo(title='Error',message="You don't have account in this system. Please try again")
            print(r.json())
        else:
             messagebox.showinfo(title='Notice',message="Success delete the address")
             r2 = requests.get(f"http://127.0.0.1:8000/customer/address?name={name}")
             res2 = json.loads(r2.text)
             print(res2['data'])
             print(r2.json())

# create tkinter window
root = tk.Tk()

# create manage profile page
manage_profile_page = ManageProfilePage(root)

# add manage profile page to tkinter window
manage_profile_page.pack()

# start tkinter event loop
root.mainloop()