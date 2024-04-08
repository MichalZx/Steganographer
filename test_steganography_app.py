import unittest
import tkinter as tk
from unittest.mock import patch

from cryptography.fernet import Fernet

from steganography_app import SteganographyApp

class TestSteganographyApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SteganographyApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.filedialog.askopenfilename', return_value='secretImage.png')
    def test_browse_image(self, mock_file_dialog):
        self.app.browse_image()
        self.assertEqual(self.app.image_path, 'secretImage.png')
        self.assertEqual(self.app.image_path_label.cget('text'), 'secretImage.png')

    @patch('tkinter.filedialog.askopenfilename', return_value='secretImage.png')
    def test_encode_text(self, mock_file_dialog):
        self.app.image_path = 'secretImage.png'
        self.app.text_entry.insert(tk.END, 'Hello, world!')
        with patch('tkinter.messagebox.showinfo') as mock_messagebox:
            self.app.encode_text()
            mock_messagebox.assert_called_once_with('Success', 'Text has been hidden in the image and saved.')

    @patch('tkinter.filedialog.askopenfilename', return_value='secretImage.png')
    @patch('stegano.lsb.reveal', return_value='Hello, world!')
    def test_reveal_text(self, mock_reveal, mock_file_dialog):
        self.app.image_path = 'secretImage.png'
        with patch('tkinter.messagebox.showinfo') as mock_messagebox:
            self.app.reveal_text()
            mock_messagebox.assert_called_once_with('Success', 'Text has been revealed from the image.')
        self.assertEqual(self.app.text_entry.get("1.0", tk.END), 'Hello, world!\n')

if __name__ == '__main__':
    unittest.main()
