from Tkinter import *
import tkFileDialog
import sqlite3

class Disco:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()

    img = PhotoImage(file="discoball.gif")
    title = Label(frame, image=img)
    title.img = img
    title.grid(row=0, columnspan=2)
    self.filename = StringVar()
    self.filename.set("No file selected")
    Label(frame, textvariable=self.filename).grid(row=1, column=0)
    Button(frame, text="Choose File ", command=self.get_lightroom_catalog_filename).grid(row=1, column=1)
    Button(frame, text="Perform Correction in Adobe Lightroom", command=self.perform_correction).grid(row=2)
    Button(frame, text="QUIT", command=frame.quit).grid(row=3)

  def get_lightroom_catalog_filename(self):
    self.filename.set(tkFileDialog.askopenfilename(filetypes=[("Adobe Lightroom Catalog Files", ".lrcat")]))

  # this writes to Lightroom's SQLite database and sets the value for Vertical perspective correction
  def perform_correction(self):
    conn = sqlite3.connect(self.filename.get())
    db = conn.cursor()
    db.execute("select image from Adobe_imageDevelopSettings")
    # for image in db.fetchall():
      # pass

root = Tk()
root.title("HELLO")

app = Disco(root)

root.mainloop()