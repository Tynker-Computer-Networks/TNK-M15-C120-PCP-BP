Secret Santa
======================


In this activity, you will attach the files and send reminder mails for the secret santa gifting game.


<img src= "https://s3.amazonaws.com/media-p.slid.es/uploads/1525749/images/10961791/C120PCP.gif" width = "50%" height = "auto">


Follow the given steps to complete this activity:
1. Perform DDOS attack




* Open file `main.py`.




* Create list to keep track of attached file paths


```sh
self.attached_files = []
```
   
* Define a function to attach a file.


```sh
def attach_file(self):
    file_path = filedialog.askopenfilename()
    if file_path:
        self.attached_files.append(file_path)
        self.update_attached_files_label()
```
   
* Update the function to send reminder mails.
 
```sh
def handle_assignments(self):
    is_reminderset = self.is_reminder.get()
    if is_reminderset:
        send_after_seconds = float(self.send_after_entry.get())
        threading.Thread(target=self.schedule_reminder_email, args=(send_after_seconds,)).start()
    else:
        threading.Thread(target=self.send_assignments).start()
```
   




* Update the send assignment function to send reminder mails.


```sh
def send_assignments(self):
    if len(self.participants) < 3:
    self.status_label.config(text="At least 3 participants are required.")
        return
```
   




* Open and read the local files and attach as email attachments.


```sh
for file_path in self.attached_files:
    with open(file_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=file_path.split("/")[-1])
        part["Content-Disposition"] = f'attachment; filename="{file_path.split("/")[-1]}"'
                message.attach(part)
```
* Call attach_file() function on button click
```
self.attach_button = Button(self.frame, text="Attach File", command=self.attach_file)
``              
* Save and run the code to check the output.
