from flask import Blueprint, request, jsonify
from flask_cors import CORS
import numpy as np
import easyocr
import traceback
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
from KRAFT.SearchResults import search_and_store_coordinates, print_stored_coordinates
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import azure_credentials


# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(azure_credentials.CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client("generator-1120sk1")

craft_blueprint = Blueprint('craft', __name__)
CORS(craft_blueprint)

@craft_blueprint.route('/craft', methods=['POST'])
def process_ocr():
    try:
        reader = easyocr.Reader(['en'])
        print("EasyOCR is working correctly.")
    except Exception as e:
        print(f"Failed to initialize EasyOCR: {e}")

    # List of PDFs from Azure Blob
    blob_list = blob_container_client.list_blobs()
    azure_pdfs = [blob.name for blob in blob_list if blob.name.endswith('.pdf')]
    print(f"Number of PDF files recognized in the Azure container: {len(azure_pdfs)}")

    # Convert PDFs to images
    for pdf_name in azure_pdfs:
        try:
            blob_client = blob_container_client.get_blob_client(pdf_name)
            pdf_stream = blob_client.download_blob()
            pdf_bytes = pdf_stream.readall()

            # Convert PDF to images using pdf2image
            images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=20)

            for i, image in enumerate(images):
                img = image.convert('RGB')
                img_np = np.array(img)
                ocr_result = reader.readtext(img_np, detail=1)
                
                search_and_store_coordinates(ocr_result)
                print_stored_coordinates()
                
                # Convert the modified PIL Image back to byte array
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                img_byte_arr = buffer.getvalue()

                # Upload the modified image back to Azure Blob
                new_blob_name = f"modified_{pdf_name.split('.')[0]}_{i}.jpg"
                new_blob_client = blob_container_client.get_blob_client(new_blob_name)
                new_blob_client.upload_blob(img_byte_arr, overwrite=True)

                # Print bounding box, text detected, and confidence score
                for result in ocr_result:
                    bounding_box, text, confidence_score = result
                    print(f"Bounding box: {bounding_box}, Detected text: '{text}', Confidence score: {confidence_score}")

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"Error processing PDF {pdf_name}: {str(e)}"}), 500

    return jsonify({"message": "OCR process completed successfully!"}), 200