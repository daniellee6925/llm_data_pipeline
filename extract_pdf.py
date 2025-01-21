import os
import json
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a single PDF file using PyMuPDF (fitz).
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None


def save_text_to_file(text, output_folder, filename):
    """
    Saves extracted text to a .txt file in the specified folder.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist
        txt_file_path = os.path.join(output_folder, f"{filename}.txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
    except Exception as e:
        print(f"Error saving text to {filename}.txt: {e}")


def process_pdf_folder(folder_path, output_json_path, txt_output_folder):
    """
    Processes all PDF files in a folder, extracts text, and saves it as JSON and individual TXT files.
    """
    pdf_data = []  # List to store extracted text and metadata

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):  # Check for PDF files
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {pdf_path}")

            # Extract text
            text = extract_text_from_pdf(pdf_path)
            if text:
                # Append to JSON data structure
                pdf_data.append({"filename": filename, "content": text})

                # Save individual .txt file
                txt_filename = os.path.splitext(filename)[0]  # Remove .pdf extension
                save_text_to_file(text, txt_output_folder, txt_filename)

    # Save all extracted data to JSON
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(pdf_data, json_file, indent=4, ensure_ascii=False)

    print(f"Data successfully saved to {output_json_path} and {txt_output_folder}.")


if __name__ == "__main__":
    # Define paths
    pdf_folder = "pdf_file"  # Folder containing PDFs
    output_json = "extracted_data.json"  # Output JSON file
    txt_output_folder = "extracted_txt_files"  # Folder for individual TXT files

    # Ensure folder exists
    if not os.path.exists(pdf_folder):
        print(f"Folder '{pdf_folder}' does not exist. Please check the path.")
    else:
        # Process the folder
        process_pdf_folder(pdf_folder, output_json, txt_output_folder)
