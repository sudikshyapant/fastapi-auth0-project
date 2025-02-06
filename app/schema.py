from pydantic import BaseModel, Field, EmailStr

class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=3, max_length=50)
    class Config:
        schema_extra = {
            "post_demo" : {
                "id": 0,
                "title" : "Demo Title",
                "content" : "Demo Content"
            }
        }
    
class UserSchema(BaseModel):
    fullname: str = Field(default = None)
    email: EmailStr = Field(default = None)
    password : str = Field(default = None)
    class Config:
        the_schema = {
            "user_demo" : {
                "name" : "Demo Name",
                "email" : "demo@email.com",
                "password" : "ABC12"
            }
        }
        
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default = None)
    password : str = Field(default = None)
    class Config:
        the_schema = {
            "user_demo" : {
                "email" : "demo@email.com",
                "password" : "ABC12"
            }
        }

    