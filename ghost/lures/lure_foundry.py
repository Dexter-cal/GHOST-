from docx import Document
from openpyxl import Workbook
import os
import shutil
import qrcode
import pyshorteners

class LureFoundry:
    """
    A powerful workshop for creating a wide variety of lure file types,
    including documents, QR codes, and shortened URLs.
    """
    def __init__(self, template_dir="ghost/lures/templates"):
        self.template_dir = template_dir
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        self.shortener = pyshorteners.Shortener()

    def create_lure(self, lure_type, output_path, payload_data, lure_name=None, benign_file=None):
        """
        Main entry point for creating any type of lure.
        """
        print(f"LureFoundry: Creating lure of type '{lure_type}'...")

        if lure_type == "qr_code":
            self.create_qr_code_lure(output_path, payload_data["url"])
        elif lure_type == "short_url":
            return self.create_short_url_lure(payload_data["url"])
        elif lure_type == "js_dropper":
            self.create_js_dropper(output_path, payload_data["url"])
        elif lure_type in ["docx", "xlsm"]:
             self.weaponize_document(lure_name, output_path, payload_data['technique'], payload_data, benign_file)
        else:
            raise ValueError(f"Unsupported lure type: {lure_type}")
        return output_path

    def create_qr_code_lure(self, output_path, url):
        """Creates a QR code that points to the payload URL."""
        img = qrcode.make(url)
        img.save(output_path)
        print(f"LureFoundry: QR code saved to '{output_path}'")

    def create_short_url_lure(self, url):
        """Creates a shortened URL lure."""
        try:
            short_url = self.shortener.tinyurl.short(url)
            print(f"LureFoundry: Shortened URL created: {short_url}")
            return short_url
        except Exception as e:
            print(f"Error creating short URL: {e}")
            return url # Fallback to the original URL

    def create_js_dropper(self, output_path, url):
        """Creates a simple JavaScript dropper file."""
        js_code = f"""
        // Simple dropper for authorized pentesting.
        // This script will attempt to download and execute a payload from the specified URL.
        var payload_url = "{url}";
        // In a real scenario, you would use a more sophisticated execution method.
        // For safety, this example will just log to the console.
        console.log("Attempting to fetch payload from: " + payload_url);
        // fetch(payload_url).then(...);
        """
        with open(output_path, 'w') as f:
            f.write(js_code)
        print(f"LureFoundry: JS dropper saved to '{output_path}'")

    def weaponize_document(self, lure_name, output_path, technique, payload_data, benign_file=None):
        """
        (Conceptual Placeholder) Creates or modifies a document to include a payload.
        """
        print("\n--- Feature Not Yet Implemented ---")
        print("The ability to weaponize documents (docx, xlsm, etc.) is a planned feature.")
        print("This is a conceptual placeholder, and no payload has been injected.")
        print("---------------------------------")
        # Create a blank file to satisfy the workflow for now.
        with open(output_path, 'w') as f:
            f.write("Placeholder for weaponized document.")
