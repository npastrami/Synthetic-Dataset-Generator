import json
from text_generation_factory import TextGeneratorFactory
from image_processor import create_and_modify_copy
from azure.storage.blob import BlobServiceClient
import azure_credentials

class FormGenerator:
    def __init__(self, form_type):
        self.form_type = form_type
        self.blob_service_client = BlobServiceClient.from_connection_string(azure_credentials.CONNECTION_STRING)
        self.blob_container_client = self.blob_service_client.get_container_client(f"generator-{form_type}")
        self.text_generator_factory = TextGeneratorFactory()
        self.fonts_folder_path = "/home/npastrami/SDG/Fonts"
        self.NUM_COPIES = 3

        # Load the configuration for the specified form type
        with open(f'./form_configs/config_{form_type}.json', 'r+') as file:
            self.config = json.load(file)
        print(f'config_{form_type}.json', 'r')
        
    def generate_text_for_keyword(self, keyword):
        generator = self.text_generator_factory.get_generator(self.form_type, keyword)
        return generator(keyword)

    def create_and_modify_form(self, blob_name, copy_index):
        # Download the original PDF
        blob_client = self.blob_container_client.get_blob_client(blob_name)
        pdf_stream = blob_client.download_blob()
        pdf_bytes = pdf_stream.readall()

        # Process the PDF, modify it, and upload the modified copy
        create_and_modify_copy(
            pdf_bytes, 
            copy_index, 
            self.config[f"bounding_boxes_{self.form_type}"], 
            self.generate_text_for_keyword, 
            self.fonts_folder_path, 
            self.blob_container_client, 
            blob_name
        )

    def generate_forms(self):
        try:
            # Assuming there's only one PDF, grab the first one
            blob_list = self.blob_container_client.list_blobs()
            template_pdf_name = next(blob.name for blob in blob_list if blob.name.endswith('.pdf'))

            # Create and modify each copy
            for i in range(self.NUM_COPIES):
                self.create_and_modify_form(template_pdf_name, i + 1)

            return {"message": f"{self.form_type} Copies Made"}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}