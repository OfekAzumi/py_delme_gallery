import os
from flask import Flask, render_template, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
from helper import save_data,load_data

app = Flask(__name__)

IMAGE_MIME_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
}

# users = [
#     {"username": "user1", "password": "password1", "img":"static/prfpic.jpg", "gallery" : []},
#     {"username": "user2", "password": "password2", "img":"static/prfpic2.png", "gallery" : []},
#     {"username": "user3", "password": "password3", "img":"static/ptfpic3.jpg", "gallery" : []}
# ]

# Set the maximum file size (in bytes) for uploaded images (2 MB in this example)
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

def allowed_filesize(file):
    # Check if the file size is within the allowed limit
    return len(file.read()) <= MAX_FILE_SIZE

@app.route("/", methods = ["get","post"])
def login():
    uname = request.form.get('username')
    pswd = request.form.get('password')
    slc_user = ''
    for usr in users:
        if uname == usr["username"]:
            if pswd == usr["password"]: slc_user = usr
    print(slc_user)
    if(slc_user):
        return render_template('homepage.html', username = uname, imagepath = slc_user["img"], user = slc_user)
    else:
        if (uname != None and pswd != None):
            return render_template('login.html', msg = 'password or username is incorrect.')
        else: 
            return render_template('login.html', msg = '')
        
@app.route('/display_image')
def display_image():
    # Specify the path to your image file (update with the actual path)
    
    image_path = request.args.get('imagepath')

    # Determine the file extension from the path
    file_extension = image_path.split('.')[-1].lower()

    # Set the MIME type based on the file extension
    if file_extension in IMAGE_MIME_TYPES:
        mimetype = IMAGE_MIME_TYPES[file_extension]
    else:
        # Default to 'application/octet-stream' if the extension is not recognized
        mimetype = 'application/octet-stream'

    # Use Flask's send_file function to send the image with the specified MIME type
    return send_file(image_path, mimetype=mimetype)

@app.route("/signupform", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        uname = request.form.get('username')
        pswd = request.form.get('password')
        print(request.files)
        if 'image' not in request.files:
            return "No file part"

        image = request.files['image']

        if image.filename == '':
            return "No selected file"

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static', filename))

        imagepath = f'static/{filename}'

        newuser = {"username": uname, "password": pswd, "img": imagepath, "gallery" : []}
        users.append(newuser)
        save_data(users)
        return render_template('homepage.html', username=uname, imagepath = imagepath, user=newuser)
    
    return render_template('signup.html')

     
@app.route("/signup")
def signupfromform():
    return render_template('signup.html')

@app.route("/uploadimage", methods=["GET", "POST"])
def uploadimage():

    if 'image' not in request.files:
        return ("No file part")


    image = request.files['image']

    if image.filename == '':
        return ("No selected file")

    if image and allowed_filesize(image):
        image.seek(0)
        filename = secure_filename(image.filename)
        image.save(os.path.join('static', filename))
        glry_imgpath = f'static/{filename}'
        uname = request.args.get("username")
        imagepath = request.args.get("imagepath")
        i = 0
        index = 0
        for x in users:
            if x["username"] == uname: 
                index = i
            i+=1
        users[index]["gallery"].append(glry_imgpath)
        save_data(users)
        return render_template('gallery.html', username=uname, imagepath = imagepath, user=users[index])
    else:
        return (f"File size exceeds the maximum allowed size ({MAX_FILE_SIZE / (1024 * 1024)} MB)", 'error')



    

@app.route("/home")
def home():
    uname = request.args.get('username')
    imagepath = request.args.get('imagepath')
    user = findInArray(uname)
    return render_template('homepage.html', username = uname, imagepath = imagepath, user = user)

@app.route("/gallery")
def gallery():
    uname = request.args.get('username')
    imagepath = request.args.get('imagepath')
    user = findInArray(uname)
    return render_template('gallery.html', username = uname, imagepath = imagepath, user = user)

@app.route("/about")
def about():
    uname = request.args.get('username')
    imagepath = request.args.get('imagepath')
    user = findInArray(uname)
    return render_template('about.html', username = uname, imagepath = imagepath, user = user)

def findInArray(uname):
    users = load_data()
    for usr in users:
        if usr["username"] == uname: return usr

if __name__=='__main__':
    users = load_data()
    app.run(debug=True)
