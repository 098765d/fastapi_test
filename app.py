from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

# Configuration
SECRET_KEY = "techteam123"
BASE_DIR = "./report"  # Directory where files are stored


@app.get("/get_file")
async def get_file(
    program: str = Query(..., description="Program code, e.g., A5B059"),
    file_type: str = Query(..., description="'report' or 'excel'"),
    keyword: str = Query(..., description="API keyword for access"),
):
    # Validate the keyword
    if keyword != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid keyword")

    # Map file type to extensions
    file_extensions = {"report": "html", "excel": "xlsx"}
    if file_type not in file_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Use 'report' or 'excel'.")

    # Construct file name
    if file_type == "report":
        file_name = f"{program}_report.{file_extensions[file_type]}"
    else:
        file_name = f"{program}_predictions.{file_extensions[file_type]}"

    file_path = os.path.join(BASE_DIR, file_name)

    # Check if file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    # Return the file as a response
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
