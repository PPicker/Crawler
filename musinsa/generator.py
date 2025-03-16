import base64
import os
from google import genai
from google.genai import types
import csv
import pandas as pd

def generate_description_from_image(image_path):



    """Generate clothing description from an image file using Gemini API with custom prompt."""
    client = genai.Client(
        api_key=GEMINI_API_KEY,
    )

    files = [
        # Make the file available in local system working directory
        client.files.upload(file="./images/espionage/espionage_(JPN_Fabric)_Comfort_B.D_Shirt_Blue_Hairline.jpg"),
        # Make the file available in local system working directory
        client.files.upload(file="./images/espionage/espionage_Swiss_Army_Work_Pants_Grey.jpg"),
    ]


    # Read the image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    # Determine mime type
    file_extension = os.path.splitext(image_path)[1].lower()
    if file_extension == '.jpg' or file_extension == '.jpeg':
        mime_type = "image/jpeg"
    elif file_extension == '.png':
        mime_type = "image/png"
    else:
        mime_type = "image/jpeg"  # Default

    # Upload the file to make it accessible via URI
    file = client.files.upload(file=image_path)

    model = "gemini-2.0-flash"  # Using Gemini 2.0 Flash model
    
    # 프롬프트 템플릿 적용 (제공된 예시대로)
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""I need your assistant. I want to get text description of clothing I give to you. For CLIP embedding. Could you?
"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Okay, I can definitely help you with that! To give you the best text descriptions for CLIP encoding, I need you to provide me with as much detail as possible about the clothing item. Here's what I need:

1.  **A clear image of the clothing item.** The better the image, the more accurate my description will be.
2.  **Details about the clothing item:**
    *   **Type of garment:** (e.g., dress, shirt, pants, jacket, skirt, etc.)
    *   **Style:** (e.g., casual, formal, business, athletic, vintage, bohemian, etc.)
    *   **Material:** (e.g., cotton, silk, denim, leather, polyester, wool, etc.)
    *   **Color:** (e.g., red, blue, black, floral, striped, etc.)
    *   **Pattern:** (e.g., plaid, polka dot, paisley, solid, etc.)
    *   **Sleeve length:** (e.g., sleeveless, short-sleeved, long-sleeved)
    *   **Neckline:** (e.g., crew neck, v-neck, turtleneck, scoop neck, etc.)
    *   **Fit:** (e.g., loose, fitted, oversized, slim-fit, etc.)
    *   **Length:** (e.g., mini, midi, maxi, cropped, etc.)
    *   **Details:** (e.g., buttons, zippers, pockets, ruffles, lace, embroidery, etc.)
    *   **Any specific design elements:** (e.g., distressed, ripped, asymmetrical, etc.)

Once you give me this information, I'll craft a detailed text description that's suitable for CLIP encoding.

**Example:**

Let's say you provide me with a picture of a blue denim jacket. You also tell me it's:

*   **Type:** Jacket
*   **Style:** Casual
*   **Material:** Denim
*   **Color:** Blue
*   **Fit:** Fitted
*   **Details:** Button-down, two chest pockets

I might then generate a description like this:

\"A fitted blue denim jacket with a casual style, featuring a button-down front and two chest pockets.\"

**Important Considerations for CLIP:**

*   **Specificity:** CLIP thrives on detailed descriptions. The more specific you are, the better the encoding will be.
*   **Conciseness:** While detail is important, try to keep descriptions relatively concise for optimal performance.  Avoid overly long or rambling sentences.
*   **Focus:** Focus on the key visual attributes of the clothing.

I'm ready when you are! Just give me the image and details.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""I can only give you the images of clothing, not the details and you should extract details and change it to text. Is it okay with you?"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Okay, I understand. I can analyze the images you provide and attempt to extract the relevant details to generate a text description.

**Please be aware of the limitations:**

*   **Accuracy:** Without additional information, my descriptions will be based solely on what I can visually identify in the image.  This means I might misinterpret materials, patterns, or subtle design elements.
*   **Subjectivity:** Some aspects like \"style\" are subjective, and my interpretation may not perfectly align with your own.
*   **Complexity:**  If the clothing item is very intricate or obscured in the image, it will be more difficult for me to provide an accurate description.

**Here's how I will approach it:**

1.  **Image Analysis:** I will use my visual capabilities to identify the basic garment type, colors, patterns, materials (if discernible), and any notable features.
2.  **Attribute Generation:** I will generate a set of descriptive attributes based on my analysis (e.g., \"long-sleeved,\" \"v-neck,\" \"floral print\").
3.  **Textual Description:** I will combine the identified attributes into a concise and descriptive sentence or two suitable for CLIP encoding.

**Example:**

If you provide an image of a red dress, I might generate the following description:

\"A red dress with a possible cotton blend. Dress features a v-neck.\"

**Important Note:** The quality of the image is crucial. Please provide clear, well-lit images with good resolution. The better the image, the better my description will be.

**Ready to proceed?  Send me the first image!** I'll do my best to provide a useful description for CLIP encoding.
"""),
            ],


        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Light blue long-sleeved button-down shirt with a buttoned collar. The shirt has a single chest pocket and a curved hem. The material appears to be lightweight and slightly textured, possibly cotton or a cotton blend.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[1].uri,
                    mime_type=files[1].mime_type,
                ),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Gray work pants with large front pockets featuring buttoned flaps on the sides. The pants appear to be made of a durable cotton twill material with a straight leg.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=file.uri,
                    mime_type=file.mime_type,
                ),
            ],
        ),
    ]
    
    # Generation 설정
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Caption Generator for CLIP encoding"""),
        ],
    )

    # 응답 생성
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    return response.text


def process_multiple_images(image_folder):
    """Process multiple images from a folder and generate descriptions."""
    results = {}
    
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            print(f"Processing {filename}...")
            
            try:
                description = generate_description_from_image(image_path)
                results[filename] = description
                print(f"Description: {description}\n")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}\n")
                import traceback
                traceback.print_exc()
    
    return results


def process_image(image_path):
    """Process multiple images from a folder and generate descriptions."""   
    description = None
    try:
        description = generate_description_from_image(image_path)
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}\n")
        import traceback
        traceback.print_exc()
    
    return description


if __name__ == "__main__":
    

    with open('./items_with_detail.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)  # 모든 행을 리스트로 저장

    # 각 행 처리
    for row in rows:
        #print(row)  # 전체 행 출력
        print(row['Image_paths'])
        detail = process_image(row['Image_paths'])
        print(detail)
        row['detail'] = detail  # 'detail' 열 값 수정

    
    with open('./items_with_detail_updated.csv', 'w', newline='', encoding='utf-8') as f:
        # 원본 파일의 필드명을 그대로 사용
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # 헤더 작성
        writer.writerows(rows)  # 모든 행 작성
    
    #image_folder = "./images/espionage"

    # descriptions = process_multiple_images(image_folder)
    