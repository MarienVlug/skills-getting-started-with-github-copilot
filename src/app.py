"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from threading import Lock

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Adding more activities to the in-memory database
activities.update({
    "Basketball": {
        "description": "Join the basketball team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer": {
        "description": "Practice soccer skills and participate in tournaments",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Painting Class": {
        "description": "Explore your creativity with painting techniques",
        "schedule": "Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": []
    },
    "Drama Club": {
        "description": "Act in plays and improve your theatrical skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": []
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    }
})

# Create a lock for each activity
activity_locks = {activity: Lock() for activity in activities}

def add_activity(activity_name: str, activity_details: dict):
    """Add a new activity and update the activity locks."""
    if activity_name in activities:
        raise HTTPException(status_code=400, detail="Activity already exists")
    activities[activity_name] = activity_details
    activity_locks[activity_name] = Lock()

# Note: Ensure that 'activity_locks' is updated dynamically if new activities are added at runtime to avoid race conditions.


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities
@app.post("/activities")
def create_activity(activity_name: str, activity_details: dict):
    """Create a new activity."""
    add_activity(activity_name, activity_details)
    return {"message": f"Activity '{activity_name}' added successfully"}

@app.post("/activities/{activity_name}/signup")

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Use the lock to ensure thread safety
    with activity_locks[activity_name]:
        # Validate student is not already signed up
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        # Add student
        activity["participants"].append(email)

    return {"message": f"Signed up {email} for {activity_name}"}
