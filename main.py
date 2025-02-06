import fastapi
from fastapi import FastAPI, Body, Depends
import uvicorn
from app.schema import  PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id" : 1,
        "title" : "Verbana",
        "text": "Verbena is a colorful flowering plant known for its vibrant blooms.",
    },
    {
        "id" : 2,
        "title" : "Alyssium",
        "text": "Alyssum's tiny flowers can be so fragrant that they are often used in gardens to create natural scented borders, making them not only visually appealing but also adding a pleasant aroma to the air.", 
    },
    {
        "id" : 3,
        "title" : "Larspur",
        "text": "Larkspur flowers, known for their vibrant hues, are toxic to pets but have been historically used in herbal medicine for their supposed pain-relieving properties.", 
    }, 
]

users = [] 

app = FastAPI()
# get for testing
@app.get("/", tags = ["test"])
def greet():
    return {"Hello, Welcome to my simple FastAPI app!"}

#1 get posts endpoint
@app.get("/posts", tags = ["posts"])
def get_posts():
    return {'data': posts}

#2 get single post {id}
@app.get("/posts/{id}", tags = ["posts"])
def get_a_post(id: int):
    if id > len(posts):
        return {"error": "Post with this ID does not exist!"}
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }
    
#3 post a blog post [a handler for creating a post]
@app.post("/posts", dependencies = [Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1 
    posts.append(post.dict())
    return {
        "info" : "Post added!"
    }
    
#4 remove a post using post id
@app.delete("/posts/{id}", tags=["posts"])
def delete_post(id: int):
    for post in posts:
        post_to_delete = True
        if post["id"] == id:
            post_to_delete = post
            break
    if not post_to_delete:
        return {
        "error" : f"Post with the ID {id} does not exist!"
            }
    posts.remove(post_to_delete)
    return {
        "info" : f"Post with ID {id} deleted successfully!"
    }
    

#5 user signup [a handler for creating a user]   
@app.post("/user/signup", tags = ["user"])
def user_signup(user: UserSchema = Body(default = None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            return False
    
#6 user login [a handler for logging in a user]
@app.post("/user/login", tags = ["user"])
def user_login(user: UserLoginSchema = Body(default = None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }
        # raise HTTPException(status_code = 400, detail = "Invalid login details!")