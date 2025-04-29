#Merging PDFs#
#Earlier we learned how to merge PDFs together. Now, we extend that using GUI
#GUI should allow users to select as many and whichever PDF users want

import tkinter as tk  # Import the tkinter module for GUI
from tkinter import filedialog, messagebox  # Import dialog and messagebox for file selection and alerts
from PyPDF2 import PdfMerger  # Import PdfMerger to merge multiple PDF files

# Initialize the Tkinter window (WITHOUT using a function)
root = tk.Tk()  # Create the main application window
root.title("PDF Merger")  # Set window title
root.geometry("300x150")  # Set window size

# Function to merge selected PDF files
def merge_pdfs():
 # Open a new file dialog window which allows you to select multiple PDF files. This window will say "Select PDF file/s"
 files = filedialog.askopenfilenames(title="Select PDF file/s", filetypes=[("PDF Files", "*.pdf")])

 if not files:  # Check if no files were selected
   messagebox.showwarning("No Files Selected", "Please select some PDF files.")
   return

 # Open a new "SAVE as" dialog window which allows us to give a name and save this merged file
 output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],
                                            title="Save Merged PDF As")

 if not output_file:  # Check if no output file was specified
   return

 try:
   merger = PdfMerger()  # Create a PdfMerger object
   for pdf in files:  # Loop through each selected PDF file
     merger.append(pdf)  # Append the PDF to the merger
   merger.write(output_file)  # Write the merged PDF to the specified output file
   merger.close()  # Close the PdfMerger object to release resources
   messagebox.showinfo("Success", f"PDFs merged successfully into {output_file}")  # Show success message
 except Exception as e:  # Handle any exceptions that occur
   messagebox.showerror("Error", f"An error occurred: {e}")  # Show error message


# Create and add a button to merge PDFs
merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs, padx=30, pady=25)
#The padx and pady specify internal padding INSIDE the button itself. padx adds space on the left and right of the button’s text.
#pady adds space above and below the button's text.

merge_button.pack(padx=10, pady=50, expand=True)
#note: expand=True ensures the widget will expand and center within the window.
#note: padx=10 and pady=50 provide some spacing OUTSIDE of the button
#padx adds space on the left and right sides of the button relative to the window.
#pady adds space above and below the button relative to the window.

# Start the main event loop
root.mainloop()