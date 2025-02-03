from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import uuid
import os

router = APIRouter()

class Blog(BaseModel):
    title: str
    content: str

class ResponseMessage(BaseModel):
    message: str

import uuid

@router.post("/write_blog", response_model=ResponseMessage)
async def write_blog(blog: Blog):
    blog_data = blog.dict()
    blog_data["id"] = str(uuid.uuid4())
    try:
        if os.path.exists("data") == False:
            os.mkdir("data")
        with open("data/blogs.json", "r+") as file:
            blogs = json.load(file)
            blogs.append(blog_data)
            file.seek(0)
            json.dump(blogs, file, indent=4)
            return {"message": "Blog written successfully"}
    except FileNotFoundError:
        with open("data/blogs.json", "w") as file:
            json.dump([blog_data], file, indent=4)
            return {"message": "Blog written successfully"}
    except json.JSONDecodeError:
        with open("data/blogs.json", "w") as file:
            json.dump([blog_data], file, indent=4)
            return {"message": "Blog written successfully"}

@router.get("/get_blogs")
async def get_blogs():
    try:
        with open("data/blogs.json", "r") as file:
            blogs = json.load(file)
            return blogs
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

@router.get("/get_blog/{blog_id}")
async def get_blog(blog_id: uuid.UUID):
    try:
        with open("data/blogs.json", "r") as file:
            blogs = json.load(file)
            for blog in blogs:
                if blog["id"] == str(blog_id):
                    return blog
            raise HTTPException(status_code=404, detail="Blog not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Blog not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.delete("/delete_blog/{blog_id}", response_model=ResponseMessage)
async def delete_blog(blog_id: int):
    try:
        with open("data/blogs.json", "r+") as file:
            blogs = json.load(file)
            if blog_id < 0 or blog_id >= len(blogs):
                raise HTTPException(status_code=404, detail="Blog not found")
            del blogs[blog_id]
            file.seek(0)
            file.truncate()
            json.dump(blogs, file, indent=4)
            return {"message": "Blog deleted successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Blog not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail="Blog not found")

