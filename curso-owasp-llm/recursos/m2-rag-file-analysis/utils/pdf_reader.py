from pypdf import PdfReader
import io
from PIL import Image
import fitz  # PyMuPDF for better PDF handling

def extract_pdf_text(path):
    """Extract text from PDF file with multiple fallback methods"""
    try:
        # Method 1: Try PyMuPDF first (better for handling various PDFs)
        print(f"  [Method 1] Trying PyMuPDF extraction...")
        text_content = []
        try:
            doc = fitz.open(path)
            print(f"  PDF Pages Found: {len(doc)}")
            
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                if page_text.strip():
                    text_content.append(page_text)
                    print(f"    Page {page_num+1}: {len(page_text)} chars extracted")
                else:
                    print(f"    Page {page_num+1}: No text (might be image-based)")
            
            doc.close()
            
            full_text = "\n".join(text_content)
            if full_text.strip():
                print(f"  [OK] [Method 1] Success: {len(full_text)} chars extracted")
                return full_text
        except Exception as e:
            print(f"  [ERROR] [Method 1] Failed: {e}")
        
        # Method 2: Try pypdf as fallback
        print(f"  [Method 2] Trying pypdf extraction...")
        try:
            reader = PdfReader(path)
            print(f"  PDF Pages Found: {len(reader.pages)}")
            
            text_content = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                    print(f"    Page {i+1}: {len(page_text)} chars extracted")
                else:
                    print(f"    Page {i+1}: No text extracted")
            
            full_text = "\n".join(text_content)
            if full_text.strip():
                print(f"  [OK] [Method 2] Success: {len(full_text)} chars extracted")
                return full_text
        except Exception as e:
            print(f"  [ERROR] [Method 2] Failed: {e}")
        
        # Method 3: Try EasyOCR as last resort (works for scanned PDFs)
        print(f"  [Method 3] Trying EasyOCR extraction...")
        try:
            import easyocr
            
            # Initialize EasyOCR reader (first time may download models - be patient)
            print(f"    Initializing OCR reader (downloading models on first run)...")
            reader = easyocr.Reader(['en'], gpu=False)
            
            ocr_text = []
            doc = fitz.open(path)
            
            for page_num, page in enumerate(doc):
                # Convert PDF page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                
                # Save temp image for EasyOCR
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    img.save(tmp.name)
                    temp_path = tmp.name
                
                # Run OCR
                try:
                    results = reader.readtext(temp_path)
                    page_text = '\n'.join([text[1] for text in results])
                    if page_text.strip():
                        ocr_text.append(page_text)
                        print(f"    Page {page_num+1} [OCR]: {len(page_text)} chars extracted")
                finally:
                    import os
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
            
            doc.close()
            
            full_text = "\n".join(ocr_text)
            if full_text.strip():
                print(f"  [OK] [Method 3] Success: {len(full_text)} chars extracted via OCR")
                return full_text
        except ImportError:
            print(f"  [INFO] [Method 3] Skipped: easyocr not installed")
        except Exception as e:
            print(f"  [ERROR] [Method 3] Failed: {e}")
        
        # All methods failed
        print(f"  [WARNING] No readable text found in PDF!")
        raise ValueError("PDF is empty or unreadable. It may be encrypted, scanned without OCR, or corrupted.")
        
    except Exception as e:
        print(f"  [ERROR] Error extracting PDF: {e}")
        raise
