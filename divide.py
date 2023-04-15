import os
from tkinter import *
from tkinter import filedialog
from csv import reader, writer

root = Tk()
root.title("CSV Splitter Tool")
root.geometry("600x300")
root.resizable(False, False)

myfont = ('Noto Sans UI', 32, 'bold') 
uifont = ('Noto Sans UI', 24, 'bold') 
txfont = ('Noto Sans UI', 12, 'bold') 

title_label = Label(root, text="CSV Splitter Tool V1.0", padx=10, pady=10, font=myfont)
title_label.pack()

frame = Frame(root)
frame.pack()

info = LabelFrame(frame, text="")
info.grid(row=0, column=0, padx=50, pady=10)

filename_entry = Entry(info, width=30)
filename_entry.grid(row = 0, column = 1, padx=10, pady=10)
filename_entry["state"] = "disabled"

def openfile(): 
    filename_entry.delete(0, len(filename_entry.get()))
    filename = filedialog.askopenfile().name
    filename_entry["state"] = "normal"
    filename_entry.insert(0, filename)
    button["state"] = "normal"

button_entry = Button(info, text="Apri file:", font=txfont,command=openfile)
button_entry.grid(row=0, column=0, padx=10, pady=10)
split_label = Label(info, text="Numero di files: ",font=txfont)
split_label.grid(row = 1, column = 0, padx=10, pady=10)
split_spinbox = Spinbox(info, from_=1, to=10)
split_spinbox.grid(row = 1, column = 1, padx=10, pady=10)

label_output = Label(frame, text="", font=txfont)
label_output.grid(row=6, column=0, padx=10, pady=10) 

def split_files():
    try :
        filename = filename_entry.get()
        
        if (not filename):
            raise Exception("Path vuoto")
        if (filename.split(".")[1] != 'csv') :
            raise Exception("Formato del file non valido: solo .csv ammessi!")
        head,tail = os.path.split(filename)
        newpath = filedialog.askdirectory()
        os.makedirs(os.path.dirname(newpath), exist_ok=True)

        # Lista per caricare il csv:
        data = list(reader(open(filename, "r"), delimiter=','))


        # Array di writers: 
        out = []

        # Numero di files generati: 
        split = getint(split_spinbox.get())

        # Scrive in testa ad ogni file l'instestazione: 
        for x in range(split) :
            fn = newpath + "/" + tail.split(".")[0] + ("-Split-%d.csv" %x)
            out.append(writer(open(fn, "w"), delimiter=',')) 
            out[x].writerow(data[0])

        # Rimuove l'intestazione:
        data.pop(0) 

        written = 0
        i = 0
        size = len(data)

        for row in data: 
            # Finche' non scrivo 1 / n di file: 
            if(written < size / split): 
                out[i].writerow(row)
                written += 1
            else: 
                # Resetta il counter e passa al file successivo: 
                written = 0
                i += 1
                out[i].writerow(row)
                written += 1    
        label_output["fg"] = 'green'
        label_output["text"] =  "%d file salvati in: " %split + newpath
        
    except Exception as e:
        label_output["fg"] = 'red'
        label_output["text"] = "Errore: " + repr(e)
    finally:
        filename_entry.delete(0, len(filename_entry.get()))
        filename_entry["state"] = "disabled"
        button["state"] = "disable"
        


button = Button(frame, text="Split", padx=15, pady=15,font=txfont, command=split_files)
button["state"] = "disable"
button.grid(row=5, column=0)


if __name__ == "__main__":
    root.mainloop()