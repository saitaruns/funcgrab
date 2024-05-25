from fastapi import FastAPI
from pydantic import BaseModel
import requests
import io
import zipfile
from database import engine, SessionLocal
import models
from file_parser import parse_code
from firebase import auth
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email: str
    password: str

@app.middleware("http")
async def authorize(request: Request, call_next):
    response = None
    if request.url.path.startswith('/functions'):
        try:
            token = request.headers.get("authorization").split(" ")[-1]
            user = auth.get_account_info(token)
            request.state.user = user
            response = await call_next(request)
        except Exception as e:
            response = JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    else:
        response = await call_next(request)
    return response

@app.post("/url/{github_url:path}")
def get_data(github_url: str):
    db = SessionLocal()
    repo = db.query(models.Function).filter(models.Function.repository_url == github_url).first()

    if repo:
        return {"error": "Repository already fetched."}
    
    # Extract the repository owner and name from the GitHub URL
    owner, repo = github_url.split("/")[-2:]

    # Make a GET request to the GitHub API to fetch the repository data
    api_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"

    try:
        response = requests.get(api_url)
    except:
        return {"error": f"Failed to fetch the repository from {api_url}"}

    if response.status_code == 200:
        buffer = io.BytesIO(response.content)

        # Unzip the repository contents
        with zipfile.ZipFile(buffer, 'r') as zip_ref:
            # Extract all the contents to a temporary directory
            temp_dir = "/tmp/repo"
            zip_ref.extractall(temp_dir)

            # Parse the code in the repository file by file
            for file in zip_ref.namelist():
                with zip_ref.open(file) as f:
                    code = f.read().decode("utf-8")
                    functions = parse_code(code)

                    # Save the functions in the database
                    print("Functions of file: ", file)
                    for function in functions:
                        print(function)
                        db_function = models.Function(
                            file_name=file,
                            function_name=function["name"],
                            class_name="class_name_placeholder",  # Update with actual class name if any
                            repository_url=github_url,
                            code=function["code"]
                        )
                        db.add(db_function)
                    db.commit()
        db.close()

        return {"message": "Repository fetched and processed successfully."}
    else:
        return {"error": "Failed to fetch the repository."}
    
@app.get("/functions")
def get_functions():
    db = SessionLocal()
    functions = db.query(models.Function).all()
    db.close()
    return functions

@app.get("/functions/{function_name}")
def get_function(function_name: str):
    db = SessionLocal()
    function = db.query(models.Function).filter(models.Function.function_name == function_name).first()
    db.close()
    if function:
        return function
    else:
        return {"error": "Function not found."}
    
@app.post("/signup")
def signup(user: User):
    try:
        user = auth.create_user_with_email_and_password(user.email, user.password)
        return user
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/login")
def login(user: User):
    try:
        user = auth.sign_in_with_email_and_password(user.email, user.password)
        return user
    except Exception as e:
        return {"error": str(e)}