import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from stegano import lsb
from cryptography.fernet import Fernet


class SteganographyApp:
    """Class representing the Steganography App."""

    def __init__(self, master):
        """Initialize the Steganography App."""
        self.master = master
        master.title("Steganography App")

        self.browse_button = tk.Button(master, text="Select Image", command=self.browse_image)
        self.browse_button.grid(row=0, column=1, pady=10)

        self.encode_button = tk.Button(master, text="Encode Text", command=self.encode_text)
        self.encode_button.grid(row=1, column=0, padx=5)
        self.reveal_button = tk.Button(master, text="Reveal Text", command=self.reveal_text)
        self.reveal_button.grid(row=1, column=2, padx=5)

        self.image_path_label = tk.Label(master, text="")
        self.image_path_label.grid(row=2, columnspan=3, pady=5)

        self.text_entry = tk.Text(master, height=5, width=50)
        self.text_entry.grid(row=3, columnspan=3, pady=5)

        self.encrypt_button = tk.Button(master, text="Encrypt Text", command=self.encrypt_text)
        self.encrypt_button.grid(row=4, column=0, pady=5)
        self.decrypt_button = tk.Button(master, text="Decrypt Text", command=self.decrypt_text)
        self.decrypt_button.grid(row=4, column=2, pady=5)

    def browse_image(self):
        """Open file dialog to select an image."""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.bmp")])
        self.image_path_label.config(text=self.image_path)

    def encode_text(self):
        """Encode text into the selected image."""
        text = self.text_entry.get("1.0", tk.END)
        if not text.strip():
            messagebox.showerror("Error", "Text to encode is empty.")
            return
        if not hasattr(self, 'image_path') or not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        try:
            secret = lsb.hide(self.image_path, text)
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            secret.save(save_path)
            messagebox.showinfo("Success", "Text has been hidden in the image and saved.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while encoding text: {e}")

    def reveal_text(self):
        """Reveal text hidden in the selected image."""
        if not hasattr(self, 'image_path') or not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        try:
            secret = lsb.reveal(self.image_path)
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, secret)
            messagebox.showinfo("Success", "Text has been revealed from the image.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while revealing text: {e}")

    def encrypt_text(self):
        """Encrypt text using Fernet symmetric encryption."""
        text = self.text_entry.get("1.0", tk.END)
        if not text.strip():
            messagebox.showerror("Error", "Text to encrypt is empty.")
            return
        key = Fernet.generate_key()
        with open('key.txt', 'wb') as key_file:
            key_file.write(key)
        try:
            cipher_key = Fernet(key)
            encrypted_text = cipher_key.encrypt(text.encode())
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, encrypted_text.decode())
            messagebox.showinfo("Success", "Text has been encrypted. The key has been saved to 'key.txt'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while encrypting text: {e}")

    def decrypt_text(self):
        """Decrypt text using Fernet symmetric encryption."""
        key_file_path = filedialog.askopenfilename(title="Choose Key File", filetypes=[("Text files", "*.txt")])
        if not key_file_path:
            messagebox.showerror("Error", "No key file selected.")
            return
        try:
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()
                cipher_key = Fernet(key)
                encrypted_text = self.text_entry.get("1.0", tk.END)
                decrypted_text = cipher_key.decrypt(encrypted_text.encode()).decode()
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, decrypted_text)
                messagebox.showinfo("Success", "Text has been decrypted.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while decrypting text: {e}")


def main():
    root = tk.Tk()
    SteganographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
