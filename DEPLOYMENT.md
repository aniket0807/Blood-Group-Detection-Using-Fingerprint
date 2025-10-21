Deploying to Render (recommended)
---------------------------------

1. Sign in to https://render.com and create a new Web Service connected to this GitHub repository.

2. Set the following fields when creating the service:
   - Environment: Python 3 (select 3.10)
   - Build Command: pip install -r requirements-prod.txt
   - Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1

3. Ensure your `model/model.h5` is present in the repo. If the file is large, consider hosting it in cloud storage and downloading it at server startup.

Notes
- If any package needs compilation (Rust/Cargo), Render's build environment can install toolchains or you can add a build command to install rustup first.
- Use `requirements-prod.txt` for production installs — it contains only the packages needed to run the app.

Using Netlify
---------------
Netlify is intended for static sites and serverless functions. It cannot run a long-lived Flask web server directly. Recommended approach: host the Flask backend on Render and use Netlify for a static frontend if desired.
