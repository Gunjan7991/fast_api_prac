from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth


# Creates all the table in database based on the models.
models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Posts",
        "description": "Manage Posts. So _fancy_ they have their own docs.",
    },
    {
        "name": "Authentication",
        "description": "Manage Login.",
    },

]
# Starter Code for Fastapi
app = FastAPI(title="FAST_API_PRAC",
              summary="Introducing the Lite Social Media App – Your Swift Path to Social Connection! Inspired by Twitter, this Python-powered sensation harnesses the power of FastAPI for lightning-fast performance. Simplify your social experience with concise 'tweets', engaging interactions, and a user-friendly design. Stay connected, share your thoughts, and discover trending topics effortlessly. Embrace the Lite Social Media App and experience social networking at its finest!",
              description="The Lite Social Media Application is a Python-based project built on FastAPI, drawing inspiration from the popular platform Twitter. The application aims to provide users with a streamlined and efficient social media experience, emphasizing simplicity and ease of use.Users can create accounts, set up profiles, and start sharing their thoughts, updates, and media content with their followers. Similar to Twitter, the Lite Social Media Application allows users to post short messages or \"tweets\" containing up to a certain character limit, encouraging concise and engaging communication.The application's minimalist design and fast performance make it ideal for users who prefer a straightforward social media experience without overwhelming features. It prioritizes the core functionalities of social networking, enabling users to follow others, be followed, and engage in conversations through likes, comments, and retweets.Built on the FastAPI framework, the application ensures rapid response times and efficient handling of user requests. With its user-friendly interface and intuitive navigation, the Lite Social Media Application seeks to cater to users seeking a simplified yet engaging platform to connect with others, share their ideas, and stay updated on the latest trends and news.",
              version="1.0",
              openapi_tags=tags_metadata
              )


@app.get("/")
def status():
    return {"message": "Server running..."}


# include all the routes
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
