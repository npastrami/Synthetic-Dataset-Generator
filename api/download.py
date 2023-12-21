from azure.storage.blob import BlobServiceClient
from flask import Blueprint, Response
from flask_cors import CORS
import io
import zipfile
import logging
import traceback 
import azure_credentials  
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(azure_credentials.CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client("generator-1065k1")

download_blueprint = Blueprint('download', __name__)
CORS(download_blueprint)

def download_and_zip(container_client):
    try:
        zip_buffer = io.BytesIO()
        images_for_pdf = {}
        pdf_buffers = {}  # Store PDFs in memory

        # Create PDFs first
        print("writing pdfs")
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            blob_name = blob.name
            if not blob_name.endswith('/'):  # Skip folders
                blob_client = container_client.get_blob_client(blob=blob_name)
                stream = blob_client.download_blob()
                data = stream.readall()
                folder = '/'.join(blob_name.split('/')[:-1])  # Extract the folder name from the blob name
                if blob_name.lower().endswith('.jpg'):
                    if folder not in images_for_pdf:
                        images_for_pdf[folder] = []
                    images_for_pdf[folder].append((blob_name, data))

        for folder, images in images_for_pdf.items():
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            for blob_name, img_data in images:
                image = Image.open(io.BytesIO(img_data))
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as temp_img:
                    image.save(temp_img.name, "JPEG")
                    c.drawImage(temp_img.name, 0, 0, width=595, height=842)
                    c.showPage()
            c.save()
            pdf_buffers[folder] = pdf_buffer.getvalue()

        # Write blobs and PDFs to ZIP
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            # Create folders and add blobs
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                blob_name = blob.name
                if blob_name.endswith('/'):
                    zf.writestr(blob_name, '')  # Create an empty folder in ZIP
                else:
                    blob_client = container_client.get_blob_client(blob=blob_name)
                    stream = blob_client.download_blob()
                    data = stream.readall()

                    folder = '/'.join(blob_name.split('/')[:-1])  # Extract the folder name from the blob name
                    if not folder:  # This means the blob is not inside any folder
                        if blob_name.lower().endswith('.jpg'):
                            zf.writestr(blob_name, data)  # Write JPGs directly to ZIP if they are not part of any folder

                    if not blob_name.lower().endswith('.jpg'):  # Skip JPGs since we converted them to PDF
                        zf.writestr(blob_name, data)

            # Add PDFs
            for folder, pdf_data in pdf_buffers.items():
                pdf_name = f"{folder}/{folder}images.pdf"
                zf.writestr(pdf_name, pdf_data)

        zip_buffer.seek(0)
        return zip_buffer.read()

    except Exception as e:
        logging.error(f"Error creating zip file: {str(e)}")
        traceback.print_exc()  # Print the full stack trace for debugging
        return None

@download_blueprint.route('/download', methods=['GET'])
def download_stream():
    try:
        zip_data = download_and_zip(blob_container_client)
        if zip_data:
            return Response(zip_data, mimetype='application/zip', headers={'Content-Disposition': 'attachment;filename=all_files.zip'})
        else:
            return "Error in creating zip", 500
    except Exception as e:
        logging.error(f"Error in download_stream: {str(e)}")
        traceback.print_exc()  # Print the full stack trace for debugging
        return "Error in download_stream", 500






