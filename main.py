from telnetlib import STATUS
from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional

app = FastAPI()

@app.get('/')
def index():
    return 'Hello World'

# Order matters: This will be intercepted by below method if it comes after it.
# We also demonstrate some path parameters
@app.get(
    '/blog/all',
    tags=['blog'],
    summary='Retrieve all blogs',
    description='This API call sumulates fetching all blogs',
    response_description="List of available blogs"
)
def get_all_blogs(page = 1, page_size: Optional[int] = None):
    return {'message': f'All {page_size} blogs on page {page}'}

# Usage: http://localhost:8000/blog/4
# Also we demonstrate status code on here too
@app.get('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blog'])
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message': f'Blog with id {id}'}


# Predefined values for path parameters. Just use python's Enum class
class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}', tags=['blog'])
def get_blog_type(type: BlogType):
    return {'message': f'Blog type {type}'}


# Mix of both path and query parameters
@app.get('/blog/{id}/comments/{comment_id}', tags=['blog', 'comments'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Simulates retrieving a comment of a blog
    """
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}






# Start with uvicorn main:app --reload