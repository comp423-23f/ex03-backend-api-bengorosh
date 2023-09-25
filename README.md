# EX03 - Check-in API and Remote

## Setup

Open the project in a VSCode DevContainer.

### Back-end Setup

1. Open a new terminal, change the working directory to `backend` and run `python3 -m pip install -r requirements.txt`
2. Run `uvicorn main:app --reload` to begin the back-end development server.

### Mock Data

If you navigate to `http://localhost:8080/docs` you will see the FastAPI docs for the provided starter code. Notice the `POST` route for `/api/reset`. This corresponds to the route in `backend/main.py#reset`, which creates a simple dummy user in the backend system. Try executing this route via the FastAPI docs system. You should see a response of `"OK"`. Next, try using the docs UI to execute the `GET /api/registrations` endpoint. Notice the response includes a single dummy user.

If you've made it this far, congratulations your setup is complete! You are now ready to dig into a guided code review to understand the makeup of the project. For this, refer to Gradescope.