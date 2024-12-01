# Job Search Assistant AI (Or Interview Assist)
Job Search Assistant AI repository is to provide the backend API, which consists basic authentication, uploading the Resume with Job Description and writing the responses for the questions generated by AI to assess the user functionalities.

## Getting Started
This document consists of live url to the web API and also steps to run the application locally and test it. The app is to have basic authentication functionality and enables authenticated user to upload resume along with job description, then the AI generates questions based on the resume and job description. Those responses will be saved to db, later can be assessed.

### Live URL
Click <a href="https://job-search-assistant-ai-301168553259.us-central1.run.app/auth/validate" target="_blank">**Job Search Assistant**</a> to validate auth live demo of the API which is deployed in Google Cloud Console, as the token is not present, you will anyway see the no token response.

### Pre-requisites
Below are the required softwares to run this frontend and backend applications:
```
1. VS Code (Any IDE of your choice).
2. Node - to create or update packges from the app.
3. Python 3.12 - 3.12 is being accepted by almost all cloud platforms.
4. Browser which supports latest features (i.e., chrome, mozilla).
```

### Tech Stack
Below are the technologies used in this application:
```
Frontend Tech:
- Next JS
- React
- Typescript
- Tailwind CSS

Backend Tech:
- Python-Flask
- Huggingface
- Langchain
- Mongo DB

Deployment Stack:
- Vercel - Frontend
- GCM - Backend
```

### Steps to run the app in local
* Clone the repository.
* Open API app folder in VS Code or any IDE of your choice.
* Open terminal which by default should open the root folder `job-search-assistant-ai`.
* Create a virtual environment with command `python -m venv .venv` and then activate it by the command `.venv\scripts\activate`
* Run `pip install -r requirements.txt` in the terminal after activating, to download all the required packages needed for the API.
* See below section to [create](https://github.com/Surya51/job-search-assistant-ai/tree/main?tab=readme-ov-file#create-env) the `.env` file, which is needed for all the functionality.
* Run `waitress-serve --host 127.0.0.1 main:app` to serve the application at `http://127.0.0.1:8080`
* Open the above url to check the health of the API.

Frontend git url: [**Job Search Assistant UI**](https://github.com/Surya51/job-search-assistant-ui) 

### Create .env
Add `.env` file at the root level and create below variables.
```
1. HF_ACCESS_TOKEN='token'    - this token should be created at huggingface.
2. SECRET_KEY='secret'        - this secret should be created by you to handle the authentication encryption.
3. MONGO_URI='uri'            - this uri is the mongo db connection string url.
4. EXPIRATION_MINUES=60       - this being 60 is better, can be changed accordingly. This is for the JWT expiration.
```

### Output

![image](https://github.com/user-attachments/assets/0bcda66a-b45a-40b4-9c5f-4085abb342a3)
![image](https://github.com/user-attachments/assets/7140c5b2-0e59-449b-b7e8-f5d7fc4242f1)
![image](https://github.com/user-attachments/assets/580cbe52-b2d6-4aeb-9832-8beef6a72cbf)
![image](https://github.com/user-attachments/assets/28e0d6a2-f617-470d-8140-b36b1b7f7921)
![image](https://github.com/user-attachments/assets/ce552fb2-46fc-48e2-a94c-e8e0de413995)

### Nice to haves
- User feedback after assessment is not implemented. This will provide more value. Currently, saving all the responses.
- Success toast messages are not implemented. This can be user friendly. Most of the errors are being shown.

### Author

* **Surya Teja Vinukonda**

### Acknowledgements

* Thanks for providing me a task to work with all the tech stacks including AI.
