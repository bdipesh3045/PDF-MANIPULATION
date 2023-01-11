from flask import Flask,redirect,url_for,flash,render_template,request,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from pypdf import PdfWriter
import threading
import os
import time
merger = PdfWriter()



app = Flask(__name__,template_folder="templates")
app.config['MAX_CONTENT_LENGTH']=50*1024*1024
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
# db=SQLAlchemy(app )

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
ALLOWED_EXTENSIONS = { 'pdf','epub'}






def remove_files():
    # Set the interval to 24 hours (in seconds)
    interval =7

    while True:
        print("A")
        # Iterate through all files in the upload folder
        for file in os.listdir('Store'):
            print("o")
            # Get the full file path
            file_path = os.path.join('Store', file)

            # Check if the file was last modified more than 24 hours ago
            if time.time() - os.path.getmtime(file_path) > interval:
                # Remove the file if it was last modified more than 24 hours ago
                os.remove(file_path)

        # Sleep for 1 hour before checking again
        time.sleep( 5)

# Create a new thread and run the remove_files function in it
thread = threading.Thread(target=remove_files)
thread.start()

def check(file):   
    if '.' in file and file.rsplit(".",1)[1] in ALLOWED_EXTENSIONS :
        return True
    else:
        return False

@app.route('/uploads/<path:filename>')
def download_file(filename):
    try:
        a=(send_from_directory('Store',
                                escape(filename), as_attachment=True))
        return(a)
    except:
        flash("Sorry the file has been deleted from the server")
        return render_template("demo1.html")
        
    

# @app.route('/downloads')
# def downloads():
#     ret

@app.route("/combinepdf",methods=['GET','POST'])
def combinepdf():
    error=None
    if request.method=='POST':
        files = request.files.getlist('files')
        if escape(files[0].filename) =='':
            flash("NO files selected")
            return render_template("work.html")
        if len(files)==1:
            flash("Select more than one file")    
            return render_template("work.html")
        for file in files:
            if file and check(escape(file.filename)):
                pass
            else:
                flash('Invalid filetype')
                return render_template("work.html")
                
            
        for pdf in files:
            merger.append(pdf)

        merger.write("Store/merged-pdf.pdf")
        merger.close()  
        filename="merged-pdf.pdf"
        return render_template("demo.html",filename=filename)
        
    else:
        return render_template('work.html')




    

if __name__ == "__main__":
    app.run(debug=True) 