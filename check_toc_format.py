from src.extractor import PDFExtractor
from pathlib import Path

e = PDFExtractor('assets/USB_PD_R3_2 V1.1 2024-10.pdf', Path('outputs'), True, 20)
pages = e.extract_content()

for p in pages:
    if p.page >= 13 and p.page <= 16:
        print(f'\n=== PAGE {p.page} ===')
        try:
            text = p.text.encode('ascii', 'ignore').decode('ascii')
            print(text[:1000])
        except:
            print("[Encoding error]")
        print("="*50)