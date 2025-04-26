from pathlib import Path
from typing import Any
from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import FileResponse
import yt_dlp
import shutil


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


def download_youtube_music(url, output_path):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "merge_output_format": "mp3",
            "outtmpl": "%(title)s.%(ext)s",
        }
        info_dict = {"'title': 'Unknown Title'"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

            print(f"Title: {info_dict.get('title', 'Unknown Title')}")
            print(
                f"Download completed! File saved as {info_dict.get('title', 'Unknown Title')}.{info_dict.get('ext', 'mp3')}"
            )
            if "ext" in info_dict and "title" in info_dict:
                currentFile = Path(
                    f"{info_dict.get('title', 'Unknown Title')}.{info_dict.get('ext', 'mp3')}"
                )
                print(currentFile.cwd())
        return info_dict
    except Exception as e:
        print(f"An error occurred: {e}")


class data(BaseModel):
    search: str


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
async def search(search: str = Form(), response_model=data):
    print(search)

    if "youtube" in search or "youtu.be" in search:
        output_path = f"./audio/"
        video_title = download_youtube_music(url=search, output_path=output_path)

        return f"downloading {video_title.title}"


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
