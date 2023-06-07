from pathlib import Path
from typing import Any
from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pytube import YouTube
from fastapi.responses import FileResponse
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

directory_path = Path("./audio")

# Check if the directory already exists
if not directory_path.exists():
    # Create the directory
    directory_path.mkdir(parents=True)
    print("Directory created successfully.")
else:
    print("Directory already exists.")

templates = Jinja2Templates(directory="templates")
class data(BaseModel):
    search:str



@app.get("/api/files")
async def list_files() -> dict[str, list[str]]:
    directory = Path("./audio")  # Replace with the actual directory path
    files = [file.name for file in directory.iterdir() if file.is_file()]
    return {"files": files}

@app.get("/download/{file_path}")
async def download_file(file_path: str):
    directory = Path("./audio")  # Replace with the actual directory path
    file_location = directory / file_path
    return FileResponse(file_location, filename=file_path)

@app.post("/api/search")
async def search(search:str = Form(),response_model=data):
    print(search)
    
    if "youtube" in search:
        yt = YouTube(search)
        audio_stream = yt.streams.get_audio_only()
        video_tile = yt.title
        output_path = f"./audio/"

        audio_stream.download(output_path=output_path,filename=f"{video_tile}.mp3")
        return f"downloading {video_tile}"
    
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})