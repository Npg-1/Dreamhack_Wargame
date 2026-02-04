from flask import Flask, render_template, request
import tarfile
import os.path
import io
import os

app = Flask(__name__)
TEMP_DIR = "temp"


if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)


def check_tar(file_storage) -> bool:        # file_storage가 Tar형식이 아니거나 깨졌다면 False를 리턴하고 그게 아니면 True를 리턴함
    binary_data = file_storage.stream.read()        # 
    binary_file = io.BytesIO(binary_data)           # 

    try:
        with tarfile.open(fileobj=binary_file, mode="r") as tar:    # 
            tar.extractall(TEMP_DIR)                                # 
        return True

    except:
        return False        # 




@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files["file"]

    if check_tar(f):
        f.save(os.path.join(TEMP_DIR, "output.tar"))
        msg = "Success"
    else:
        msg = "Fail"

    return render_template("index.html", msg = msg)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
