from flask  import Flask, request, jsonify
import boto3 
import os 

app = Flask(__name__)

#AWS S3 bucket 
s3 = boto3.client('s3', 
                  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], 
                  region_name=os.environ['AWS_REGION'])

BUCKET_NAME = os.environ['AWS_BUCKET_NAME']

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error', 'No selected file'}), 400
    
    file_path = os.path.join('/temp', file.filename)
    file.save(file_path)
    
    # Upload the file to S3
    s3.upload_file(file_path, BUCKET_NAME, file.filename)
    
    os.remove(file_path)
    
    return jsonify({"sucess": True, "messsage": f"File {file.filename} uploaded successfully to S3 bucket"}), 200

if __name__ == '__main__': 
    if not os.path.exists('/temp'):
        os.makedirs('/temp')
    app.run(debug=True, port=5000)