# Dictionary to store the bounding box coordinates for each target string
bounding_boxes = {
    "Employee SSN": [],
    "Employer EIN": [],
    "Employer Name": [],
    "Address NW 7 ST, City, State, ZIP": [],
    "dint-1,000": [],
    "First and Initial": [],
    "Only Last": [],
    "Boxl": [],
    "Box 2-8": [],
    "Box 10 & 11": [],
    "XYZ": []
}

def search_and_store_coordinates(ocr_results):
    """
    Search for target strings in OCR results and store their bounding box coordinates.

    Parameters:
    ocr_results (list): List of tuples containing bounding box, detected text, and confidence score.

    Returns:
    None
    """
    for result in ocr_results:
        bounding_box, text, _ = result
        # Check if the detected text matches any target string
        for target_string in bounding_boxes.keys():
            if target_string.lower() in text.lower():
                bounding_boxes[target_string].append(bounding_box)

def print_stored_coordinates():
    """
    Print each keyword and its associated list of matched bounding box coordinates.

    Returns:
    None
    """
    for keyword, boxes in bounding_boxes.items():
        print(f"Keyword: {keyword}")
        print(f"Bounding Boxes: {boxes}")