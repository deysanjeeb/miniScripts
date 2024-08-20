from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import os
from io import BytesIO

app = FastAPI()

@app.post("/convert-to-webp/")
async def convert_to_webp(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        image = Image.open(BytesIO(await file.read()))
        
        # Create a BytesIO object to save the WebP image
        webp_image_io = BytesIO()
        
        # Save the image in WebP format to the BytesIO object
        image.save(webp_image_io, format='WEBP')
        
        # Seek to the beginning of the BytesIO object
        webp_image_io.seek(0)
        
        # Create a temporary file path to save the WebP image
        webp_image_path = f"/tmp/{os.path.splitext(file.filename)[0]}.webp"
        
        # Save the WebP image to the temporary file path
        with open(webp_image_path, "wb") as f:
            f.write(webp_image_io.getbuffer())
        
        # Return the WebP image as a file response
        return FileResponse(webp_image_path, media_type="image/webp", filename=f"{os.path.splitext(file.filename)[0]}.webp")
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)