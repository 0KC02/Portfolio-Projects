import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
from password_utils import PasswordGenerator, PasswordStrength

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        self.db = Database()
        self.master_password = None
        self.current_password_id = None
        
        self.show_login_screen()
    
    def show_login_screen(self):
        """Display the login/setup screen"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=50, pady=50)
        main_frame.pack(expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Password Manager", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 30))
        
        # Password entry frame
        password_frame = tk.Frame(main_frame, bg="#f0f0f0")
        password_frame.pack(pady=20)
        
        password_label = tk.Label(
            password_frame,
            text="Master Password:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        password_label.pack(anchor="w", pady=5)
        
        self.master_password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            show="*",
            width=30
        )
        self.master_password_entry.pack(pady=5)
        self.master_password_entry.bind("<Return>", lambda e: self.authenticate())
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        if self.db.has_master_password():
            login_btn = tk.Button(
                button_frame,
                text="Login",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                padx=30,
                pady=10,
                cursor="hand2",
                command=self.authenticate
            )
            login_btn.pack(side=tk.LEFT, padx=10)
        else:
            setup_btn = tk.Button(
                button_frame,
                text="Set Master Password",
                font=("Arial", 12, "bold"),
                bg="#2196F3",
                fg="white",
                padx=30,
                pady=10,
                cursor="hand2",
                command=self.setup_master_password
            )
            setup_btn.pack(side=tk.LEFT, padx=10)
    
    def setup_master_password(self):
        """Set up the master password for the first time"""
        password = self.master_password_entry.get()
        
        if len(password) < 8:
            messagebox.showerror("Error", "Master password must be at least 8 characters long")
            return
        
        # Confirm password
        confirm = simpledialog.askstring(
            "Confirm Password",
            "Re-enter master password:",
            show="*"
        )
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Hash and store master password
        password_hash = self.db.hash_password(password)
        self.db.set_master_password(password_hash)
        self.master_password = password
        
        messagebox.showinfo("Success", "Master password set successfully!")
        self.show_main_screen()
    
    def authenticate(self):
        """Authenticate user with master password"""
        password = self.master_password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter master password")
            return
        
        stored_hash = self.db.get_master_password_hash()
        if not stored_hash:
            messagebox.showerror("Error", "No master password found")
            return
        
        password_hash = self.db.hash_password(password)
        
        if password_hash == stored_hash:
            self.master_password = password
            self.show_main_screen()
        else:
            messagebox.showerror("Error", "Incorrect master password")
            self.master_password_entry.delete(0, tk.END)
    
    def show_main_screen(self):
        """Display the main password management screen"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main container
        container = tk.Frame(self.root, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = tk.Frame(container, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text="Password Manager",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)
        
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.logout
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Search frame
        search_frame = tk.Frame(container, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_label = tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 10),
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_passwords())
        
        refresh_btn = tk.Button(
            search_frame,
            text="Refresh",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.refresh_passwords
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # View passwords tab
        view_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(view_frame, text="View Passwords")
        
        # Treeview for password list
        tree_frame = tk.Frame(view_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.password_tree = ttk.Treeview(
            tree_frame,
            columns=("Website", "Username", "Password"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.password_tree.yview)
        
        self.password_tree.heading("#0", text="ID")
        self.password_tree.heading("Website", text="Website")
        self.password_tree.heading("Username", text="Username")
        self.password_tree.heading("Password", text="Password")
        
        self.password_tree.column("#0", width=50)
        self.password_tree.column("Website", width=200)
        self.password_tree.column("Username", width=200)
        self.password_tree.column("Password", width=250)
        
        self.password_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.password_tree.bind("<Double-1>", self.on_item_select)
        
        # Buttons frame for view tab
        view_buttons = tk.Frame(view_frame, bg="#f0f0f0")
        view_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        delete_btn = tk.Button(
            view_buttons,
            text="Delete",
            font=("Arial", 10, "bold"),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.delete_password
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(
            view_buttons,
            text="Edit",
            font=("Arial", 10, "bold"),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.edit_password
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        view_btn = tk.Button(
            view_buttons,
            text="View",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.view_password_details
        )
        view_btn.pack(side=tk.LEFT, padx=5)
        
        # Add password tab
        add_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(add_frame, text="Add/Edit Password")
        
        form_frame = tk.Frame(add_frame, bg="#f0f0f0")
        form_frame.pack(pady=50)
        
        # Website field
        website_frame = tk.Frame(form_frame, bg="#f0f0f0")
        website_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            website_frame,
            text="Website:",
            font=("Arial", 11),
            bg="#f0f0f0",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.website_entry = tk.Entry(
            website_frame,
            font=("Arial", 11),
            width=40
        )
        self.website_entry.pack(side=tk.LEFT, padx=10)
        
        # Username field
        username_frame = tk.Frame(form_frame, bg="#f0f0f0")
        username_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=("Arial", 11),
            bg="#f0f0f0",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 11),
            width=40
        )
        self.username_entry.pack(side=tk.LEFT, padx=10)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg="#f0f0f0")
        password_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            password_frame,
            text="Password:",
            font=("Arial", 11),
            bg="#f0f0f0",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        password_input_frame = tk.Frame(password_frame, bg="#f0f0f0")
        password_input_frame.pack(side=tk.LEFT, padx=10)
        
        self.password_entry = tk.Entry(
            password_input_frame,
            font=("Arial", 11),
            width=32,
            show="*"
        )
        self.password_entry.pack(side=tk.LEFT)
        
        self.show_btn = tk.Button(
            password_input_frame,
            text="Show",
            font=("Arial", 9),
            bg="#666666",
            fg="white",
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.toggle_password_visibility
        )
        self.show_btn.pack(side=tk.LEFT, padx=5)
        
        # Password strength indicator
        strength_frame = tk.Frame(form_frame, bg="#f0f0f0")
        strength_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            strength_frame,
            text="Strength:",
            font=("Arial", 11),
            bg="#f0f0f0",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.strength_label = tk.Label(
            strength_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0"
        )
        self.strength_label.pack(side=tk.LEFT, padx=10)
        
        self.password_entry.bind("<KeyRelease>", lambda e: self.update_strength_indicator())
        
        # Password generator frame
        generator_frame = tk.Frame(form_frame, bg="#f0f0f0")
        generator_frame.pack(fill=tk.X, pady=20)
        
        gen_options_frame = tk.Frame(generator_frame, bg="#f0f0f0")
        gen_options_frame.pack(pady=10)
        
        tk.Label(
            gen_options_frame,
            text="Generate Password:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=5)
        
        self.length_var = tk.StringVar(value="16")
        length_spin = tk.Spinbox(
            gen_options_frame,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=5,
            font=("Arial", 10)
        )
        length_spin.pack(side=tk.LEFT, padx=5)
        
        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            gen_options_frame,
            text="A-Z",
            variable=self.include_upper,
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Checkbutton(
            gen_options_frame,
            text="a-z",
            variable=self.include_lower,
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Checkbutton(
            gen_options_frame,
            text="0-9",
            variable=self.include_numbers,
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Checkbutton(
            gen_options_frame,
            text="!@#",
            variable=self.include_symbols,
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=2)
        
        generate_btn = tk.Button(
            gen_options_frame,
            text="Generate",
            font=("Arial", 10, "bold"),
            bg="#9C27B0",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.generate_password
        )
        generate_btn.pack(side=tk.LEFT, padx=10)
        
        # Submit button
        submit_frame = tk.Frame(form_frame, bg="#f0f0f0")
        submit_frame.pack(pady=30)
        
        save_btn = tk.Button(
            submit_frame,
            text="Save Password",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.save_password
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(
            submit_frame,
            text="Clear",
            font=("Arial", 12),
            bg="#999999",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Load passwords
        self.refresh_passwords()
    
    def search_passwords(self):
        """Search passwords based on query"""
        query = self.search_entry.get().strip()
        
        if query:
            passwords = self.db.search_passwords(query, self.master_password)
        else:
            passwords = self.db.get_all_passwords(self.master_password)
        
        self.populate_tree(passwords)
    
    def refresh_passwords(self):
        """Refresh the password list"""
        self.search_entry.delete(0, tk.END)
        passwords = self.db.get_all_passwords(self.master_password)
        self.populate_tree(passwords)
    
    def populate_tree(self, passwords):
        """Populate the treeview with password entries"""
        # Clear existing items
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)
        
        # Add passwords
        for pwd in passwords:
            self.password_tree.insert(
                "",
                tk.END,
                text=pwd['id'],
                values=(pwd['website'], pwd['username'], "•" * len(pwd['password']))
            )
    
    def on_item_select(self, event):
        """Handle double-click on password item"""
        selection = self.password_tree.selection()
        if selection:
            self.view_password_details()
    
    def view_password_details(self):
        """View password details in a dialog"""
        selection = self.password_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry")
            return
        
        item = self.password_tree.item(selection[0])
        password_id = int(item['text'])
        
        passwords = self.db.get_all_passwords(self.master_password)
        password = next((p for p in passwords if p['id'] == password_id), None)
        
        if password:
            details_window = tk.Toplevel(self.root)
            details_window.title("Password Details")
            details_window.geometry("400x200")
            details_window.configure(bg="#f0f0f0")
            
            details_frame = tk.Frame(details_window, bg="#f0f0f0", padx=20, pady=20)
            details_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                details_frame,
                text=f"Website: {password['website']}",
                font=("Arial", 11),
                bg="#f0f0f0",
                anchor="w"
            ).pack(fill=tk.X, pady=5)
            
            tk.Label(
                details_frame,
                text=f"Username: {password['username']}",
                font=("Arial", 11),
                bg="#f0f0f0",
                anchor="w"
            ).pack(fill=tk.X, pady=5)
            
            pwd_frame = tk.Frame(details_frame, bg="#f0f0f0")
            pwd_frame.pack(fill=tk.X, pady=5)
            
            pwd_var = tk.StringVar(value=password['password'])
            pwd_entry = tk.Entry(
                pwd_frame,
                textvariable=pwd_var,
                font=("Arial", 11),
                width=30
            )
            pwd_entry.pack(side=tk.LEFT)
            pwd_entry.config(state="readonly")
            
            copy_btn = tk.Button(
                pwd_frame,
                text="Copy",
                font=("Arial", 9),
                bg="#2196F3",
                fg="white",
                padx=10,
                pady=2,
                cursor="hand2",
                command=lambda: self.copy_to_clipboard(password['password'])
            )
            copy_btn.pack(side=tk.LEFT, padx=5)
            
            close_btn = tk.Button(
                details_frame,
                text="Close",
                font=("Arial", 10),
                bg="#999999",
                fg="white",
                padx=20,
                pady=5,
                cursor="hand2",
                command=details_window.destroy
            )
            close_btn.pack(pady=10)
    
    def delete_password(self):
        """Delete selected password"""
        selection = self.password_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this password?"):
            return
        
        item = self.password_tree.item(selection[0])
        password_id = int(item['text'])
        
        self.db.delete_password(password_id)
        messagebox.showinfo("Success", "Password deleted successfully")
        self.refresh_passwords()
    
    def edit_password(self):
        """Load selected password into edit form"""
        selection = self.password_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry to edit")
            return
        
        item = self.password_tree.item(selection[0])
        password_id = int(item['text'])
        
        passwords = self.db.get_all_passwords(self.master_password)
        password = next((p for p in passwords if p['id'] == password_id), None)
        
        if password:
            self.current_password_id = password_id
            self.website_entry.delete(0, tk.END)
            self.website_entry.insert(0, password['website'])
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, password['username'])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password['password'])
            self.update_strength_indicator()
            
            # Switch to add/edit tab
            notebook = self.root.winfo_children()[0].winfo_children()[1]
            notebook.select(1)
    
    def save_password(self):
        """Save password (add new or update existing)"""
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not website or not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.current_password_id:
            # Update existing
            self.db.update_password(
                self.current_password_id,
                website,
                username,
                password,
                self.master_password
            )
            messagebox.showinfo("Success", "Password updated successfully")
            self.current_password_id = None
        else:
            # Add new
            self.db.add_password(
                website,
                username,
                password,
                self.master_password
            )
            messagebox.showinfo("Success", "Password saved successfully")
        
        self.clear_form()
        self.refresh_passwords()
    
    def clear_form(self):
        """Clear the password form"""
        self.website_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.current_password_id = None
        self.strength_label.config(text="", bg="#f0f0f0")
    
    def generate_password(self):
        """Generate a random password"""
        try:
            length = int(self.length_var.get())
            password = PasswordGenerator.generate(
                length=length,
                include_uppercase=self.include_upper.get(),
                include_lowercase=self.include_lower.get(),
                include_numbers=self.include_numbers.get(),
                include_symbols=self.include_symbols.get()
            )
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.update_strength_indicator()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def update_strength_indicator(self):
        """Update password strength indicator"""
        password = self.password_entry.get()
        if password:
            score, strength, color, feedback = PasswordStrength.analyze(password)
            self.strength_label.config(
                text=f"{strength} ({score}/9)",
                fg=color,
                bg="#f0f0f0"
            )
        else:
            self.strength_label.config(text="", bg="#f0f0f0")
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
            self.show_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.show_btn.config(text="Show")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def logout(self):
        """Logout and return to login screen"""
        self.master_password = None
        self.show_login_screen()


def main():
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

