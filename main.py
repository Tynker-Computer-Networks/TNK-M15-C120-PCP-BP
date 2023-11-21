from tkinter import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tkinter import messagebox
from tkinter import filedialog
import random
import threading
import time


class SecretSanta(Tk):
    def __init__(self):
        super().__init__()
        self.title("Secret Santa App")

        # is_reminder is the flag variable for reminder emails.
        self.is_reminder = BooleanVar()
        self.is_reminder.set(False)

        self.frame = Frame()
        self.frame.grid(column=0, row=0, padx=10, pady=10)

        Label(self.frame, text="Participant Name:").grid(
            column=0, row=0, sticky="w")
        self.participant_name_entry = Entry(self.frame)
        self.participant_name_entry.grid(
            column=1, row=0, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Participant Email:").grid(
            column=0, row=1, sticky="w")
        self.participant_email_entry = Entry(self.frame)
        self.participant_email_entry.grid(
            column=1, row=1, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Participant Comma Seprated Wishlist:").grid(
            column=0, row=2, sticky="w")
        self.participant_whishlist_entry = Entry(self.frame)
        self.participant_whishlist_entry.grid(
            column=1, row=2, padx=10, pady=5, columnspan=2)

        self.add_button = Button(
            self.frame, text="Add Participant", command=self.add_participant)
        self.add_button.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Participants List:").grid(
            column=0, row=4, sticky="w")
        self.participants_listbox = Listbox(self.frame)
        self.participants_listbox.grid(
            column=1, row=4, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Sender's Email:").grid(
            column=0, row=5, sticky="w")
        self.sender_email_entry = Entry(self.frame)
        self.sender_email_entry.grid(
            column=1, row=5, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Sender's Password:").grid(
            column=0, row=6, sticky="w")
        self.sender_password_entry = Entry(self.frame, show="*")
        self.sender_password_entry.grid(
            column=1, row=6, padx=10, pady=5, columnspan=2)

        self.attached_files_label = Label(self.frame, text="Attached Files:")
        self.attached_files_label.grid(
            column=0, row=7, sticky="w", padx=10, pady=5)

        # Call attach_file() function on button click
        self.attach_button = Button(self.frame, text="Attach File")
        self.attach_button.grid(column=1, row=8, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Send After (seconds):").grid(
            column=0, row=9, sticky="w")
        self.send_after_entry = Entry(self.frame)
        self.send_after_entry.grid(
            column=1, row=9, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Check for Reminder:").grid(
            column=0, row=10, sticky="w")

        self.recurring_email_checkbox = Checkbutton(
            self.frame, variable=self.is_reminder)

        self.recurring_email_checkbox.grid(
            column=1, row=10, padx=10, pady=5, columnspan=2)

        self.send_button = Button(
            self.frame, text="Send Assignments", command=self.handle_assignments)
        self.send_button.grid(column=1, row=11, padx=10, pady=10, columnspan=2)

        self.status_label = Label(self.frame, text="", fg="green")
        self.status_label.grid(column=1, row=12, padx=10,
                               pady=10, columnspan=2)

        self.isEmailNotSent = False
        self.participants = []
        self.assignments = []

        # Create list to keep track of attached file paths

    def add_participant(self):
        name = self.participant_name_entry.get()
        email = self.participant_email_entry.get()
        wishlist = self.participant_whishlist_entry.get()
        if (name and email and wishlist):
            self.participants.append((name, email, wishlist))
            self.update_listbox()
            self.participant_name_entry.delete(0, END)
            self.participant_email_entry.delete(0, END)
            self.participant_whishlist_entry.delete(0, END)

    # Define attach_file() function

    def update_attached_files_label(self):
        attached_files_text = "\n".join(
            [file.split("/")[-1] for file in self.attached_files])
        self.attached_files_label.config(
            text=f"Attached Files:\n{attached_files_text}")

    def update_listbox(self):
        self.participants_listbox.delete(0, END)
        for participant in self.participants:
            self.participants_listbox.insert(END, participant[0])

    # Update the handle_assignments() function logic to send reminder emails.
    def handle_assignments(self):
        threading.Thread(target=self.send_assignments).start()

    # Update the send_assignments() function logic to send reminder emails.
    def send_assignments(self):
        if len(self.participants) < 3:
            self.status_label.config(
                text="At least 3 participants are required.")
            return

        random.shuffle(self.participants)
        self.assignments = self.participants.copy()

        while self.has_self_assignments():
            random.shuffle(self.assignments)

        for i, participant in enumerate(self.participants):
            name, email, w = participant
            assigned_to = self.assignments[i][0]
            wishlist = self.assignments[i][2]

            self.send_email(name, email, assigned_to, wishlist)

        messagebox.showinfo("Assignments Sent",
                            "Assignments sent. Check your emails!")

    def has_self_assignments(self):
        for i in range(len(self.participants)):
            if self.participants[i][0] == self.assignments[i][0]:
                return True
        return False

    def send_email(self, recipient_name, recipient_email, assigned_to, wishlist):
        try:
            sender_email = self.sender_email_entry.get()
            password = self.sender_password_entry.get()

            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, password)

            subject = "Your Secret Santa Assignment"
            msg_body = f"Hello {recipient_name},\n\nYour Secret Santa assignment is: {assigned_to}\n\nWishlist: {wishlist}"

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(msg_body, "plain"))

            # Open and read the local files and attach as email attachments.

            smtp_server.sendmail(
                sender_email, recipient_email, message.as_string())
            smtp_server.quit()

        except Exception as e:
            self.isEmailNotSent = True
            messagebox.showerror("Error", f"An error occurred:{str(e)}")

    def schedule_reminder_email(self, send_after_seconds):
        while True:
            self.send_assignments()
            time.sleep(send_after_seconds)


def main():
    app = SecretSanta()
    app.mainloop()


if __name__ == "__main__":
    main()
