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

Triggering Render deploy via GitHub Actions
------------------------------------------

You can automate deploys by adding a GitHub Actions workflow that calls the Render API to trigger a deploy. Add these secrets to your repository:

- `RENDER_API_KEY` — your Render API key (api key with deploy permissions)
- `RENDER_SERVICE_ID` — the Render service id for your web service

Place the secrets in GitHub: Settings -> Secrets -> Actions and name them exactly as above.

Model downloads
---------------
If your `model/model.h5` is large and you prefer not to keep it in the repo, host it on a storage bucket (S3/GCS) and set a `MODEL_URL` environment variable in Render to point to the model file. The app will download the model on startup if it isn't present.

Legacy TensorFlow models
------------------------
If your saved `.h5` model was built with an older TensorFlow/Keras version it may not deserialize under the latest TensorFlow. To handle this, a legacy requirements file `requirements-prod-legacy.txt` is supported by the Dockerfile. If that file exists the Docker build will install its pinned packages instead of `requirements-prod.txt`.

For a quick fix to load older models, put `requirements-prod-legacy.txt` in the repo (it already exists in this repo) and redeploy. This will install TensorFlow 2.11 and compatible packages so your existing `.h5` model can be loaded.


