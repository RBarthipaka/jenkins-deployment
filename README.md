# Dummy Deployment Test App

A minimal Streamlit app for testing your Docker + Jenkins multibranch pipeline flow.

## Files
- `app.py` — the dummy Streamlit application
- `requirements.txt` — Python dependencies
- `Dockerfile` — builds the app into a container image
- `.dockerignore` — excludes junk files from the image
- `Jenkinsfile` — multibranch pipeline: build → test → deploy via `docker run`

## Run locally (no Docker)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run with Docker
```bash
docker build -t myapp:local .
docker run -d --name myapp-local -p 8501:8501 myapp:local
```
Then open http://localhost:8501

## Push to git
```bash
git init                     # skip if repo already exists
git add .
git commit -m "Initial dummy app with Docker + Jenkins setup"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Jenkins Multibranch Pipeline
1. Jenkins → New Item → Multibranch Pipeline
2. Branch Sources → Git → add repo URL + credentials
3. Build Configuration → Script Path: `Jenkinsfile`
4. Save → Jenkins will auto-discover branches and run the pipeline

On `main`/`master`/`develop` branches, the pipeline deploys the container on port 8501
(or 8601 for other branches) via `docker run` on the Jenkins agent VM.

Make sure the `jenkins` user can run Docker:
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```
