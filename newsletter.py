##################################################
## For more Details --> README
##################################################
## Author: "Estella Kinzel"
## Version: "0.1.1"
## Status: "dev"
##################################################

# for mail-sending
import csv
import smtplib
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# for the GUI
import tkinter as tk
from tkinter import filedialog

# TODO no automation --> windows task scheduler, bath file etc. --> work if computer turned off? --> server?

class NewsletterWithGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Newsletter")
        self.master.geometry("600x400") # size window
        self.master.configure(bg="#2E2E2E")

        #calling the forms and buttons
        self.create_subject_form()
        self.create_html_form()
        self.create_text_form()
        self.create_subs_form()
        self.create_user_form()
        self.create_submit_button()

    # method for each form/button for more structure (personal)
    def create_subject_form(self):
        self.subject_label = tk.Label(self.master, text="Subject:", bg="#2E2E2E", fg="white")
        self.subject_label.pack() #position
        self.subject_entry = tk.Entry(self.master, width=70, bg="#2E2E2E", fg="white")
        self.subject_entry.pack()

    def create_html_form(self):
        self.html_label = tk.Label(self.master, text="HTML File:", bg="#2E2E2E", fg="white")
        self.html_label.pack()
        self.html_entry = tk.Entry(self.master, width=70, bg="#2E2E2E", fg="white")
        self.html_entry.pack()
        self.html_button_select = tk.Button(self.master, text="Select", command=self.select_html, bg="#2E2E2E", fg="white")
        self.html_button_select.pack()

    def create_text_form(self):
        self.text_label = tk.Label(self.master, text="Text:", bg="#2E2E2E", fg="white")
        self.text_label.pack()
        self.text_entry = tk.Text(self.master, width=70, height=5, bg="#2E2E2E", fg="white")
        self.text_entry.pack()

    def create_subs_form(self):
        self.sub_label = tk.Label(self.master, text="Subscriber CSV File:", bg="#2E2E2E", fg="white")
        self.sub_label.pack()
        self.sub_entry = tk.Entry(self.master, width=70, bg="#2E2E2E", fg="white")
        self.sub_entry.pack()
        self.sub_button_select = tk.Button(self.master, text="Select", command=self.select_subs, bg="#2E2E2E", fg="white")
        self.sub_button_select.pack()

    def create_user_form(self):
        self.mail_label = tk.Label(self.master, text="Your Mail address:", bg="#2E2E2E", fg="white")
        self.mail_label.pack()
        self.mail_entry = tk.Entry(self.master, width=70, bg="#2E2E2E", fg="white")
        self.mail_entry.pack()

        self.password_label = tk.Label(self.master, text="Your Password:", bg="#2E2E2E", fg="white")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*", width=70, bg="#2E2E2E", fg="white")
        self.password_entry.pack()

    def create_submit_button(self):
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit, bg="#2E2E2E", fg="white")
        self.submit_button.pack()

    def select_html(self):
        path = filedialog.askopenfilename(title="Select HTML File", filetypes=[("HTML Files", "*.html")])
        self.html_entry.delete(0, tk.END)
        self.html_entry.insert(0, path)

    def select_subs(self):
        path = filedialog.askopenfilename(title="Select Subscriber CSV File", filetypes=[("CSV Files", "*.csv")])
        self.sub_entry.delete(0, tk.END)
        self.sub_entry.insert(0, path)

    def config_send_newsletter(self, subs, content, subject):
        mail_user = self.mail_entry.get()
        password_user = self.password_entry.get()

        msg = MIMEMultipart()
        msg['From'] = mail_user
        msg['To'] = subs['email']
        msg['Subject'] = subject

        # checking if HTML file
        msg.attach(MIMEText(content, 'html' if content.startswith('<') else 'plain'))

        # ssl secured with smtplib.SMTP_SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server: # port, context, smtp
            server.login(mail_user, password_user)
            server.sendmail(mail_user, subs['email'], msg.as_string())

    def send_newsletters(self):
        content_html_path = self.html_entry.get()
        content_text = self.text_entry.get("1.0", tk.END).strip()

        # either HTML file or plain text --> otherwise invalid
        if content_html_path and os.path.isfile(content_html_path):
            with open(content_html_path, 'r') as html_file:
                content = html_file.read()
        elif content_text:
            content = content_text
        else:
            print("Invalid input")
            return

        subject = self.subject_entry.get()
        subs_path = self.sub_entry.get()
        subs = self.csv_read_subs(subs_path)

        # sending mail
        for subscriber in subs:
            self.config_send_newsletter(subscriber, content, subject)
            print(f"Mail was sent to {subscriber['email']}") # terminal messages

    def submit(self):
        self.send_newsletters()

    def csv_read_subs(self, csv_file):
        sub_list = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file) # read CSV files with csv.reader()
            next(reader)
            for row in reader:
                sub_mail = row[0]
                sub_list.append({'email': sub_mail}) # adding to list
        return sub_list

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsletterWithGUI(root)
    root.mainloop()
