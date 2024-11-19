# 1 - GUIDE TO DEPLOY GOOGLE CLOUD APP
Here’s a step-by-step guide to configure a GitHub Actions workflow that builds and deploys your application to Google Cloud Run using the provided YAML configuration.

### Step 1: Enable Required Google Cloud APIs

1. Go to the Google Cloud Console.
2. Navigate to **APIs & Services** > **Library**.
3. Search for and enable the following APIs:
   - **Artifact Registry API** (`artifactregistry.googleapis.com`)
   - **Cloud Run API** (`run.googleapis.com`)
   - **IAM Credentials API** (`iamcredentials.googleapis.com`)

### Step 2: Create and Configure Workload Identity Provider

1. In the **Google Cloud Console**, navigate to **IAM & Admin** > **Workload Identity Federation**.
2. Click on **Create Workload Identity Pool**.
3. Fill in the required fields (e.g., name, description).
4. After creating the pool, click on it and then create a **Provider**.
5. Choose **GitHub** as the provider type and follow the instructions to set it up.
6. Make sure to note down the **Provider ID**.

### Step 3: Grant IAM Permissions

1. Go to **IAM & Admin** > **IAM** in the Google Cloud Console.
2. Find the service account that will be used for deployment or create a new one.
3. Assign the following roles to the service account:
   - **Artifact Registry Administrator** (`roles/artifactregistry.admin`)
   - **Cloud Run Developer** (`roles/run.developer`)
4. If you created a Workload Identity Provider, ensure that the service account is linked to the provider with the necessary permissions.

### Step 4: Store Service Account Key in GitHub Secrets

1. In the Google Cloud Console, go to **IAM & Admin** > **Service Accounts**.
2. Select the service account you are using and click on **Keys**.
3. Click on **Add Key** > **JSON** to download the key file.
4. Go to your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions**.
5. Click on **New repository secret** and add a secret named `GCP_SA_KEY`. Paste the contents of the JSON key file into the value field.

### Step 5: Update the Workflow Configuration

Make sure the values in the `env` block of your workflow YAML match your project settings:

```yaml
env:
  PROJECT_ID: 'your-gcp-project-id'  # Replace with your GCP Project ID
  REGION: 'your-region'                # e.g., 'asia-southeast1'
  SERVICE: 'your-cloud-run-service'    # Name of your Cloud Run service
  REPO_NAME: 'your-repo-name'          # Name of your Artifact Registry repository
```

### Step 6: Commit the Workflow File

1. Create a new file in your repository under `.github/workflows/deploy.yml`.
2. Copy and paste the entire workflow YAML configuration you provided into this file.
3. Commit the changes to the `cloudrun` branch.

### Step 7: Trigger the Deployment

1. Push a commit to the `cloudrun` branch of your repository.
2. This should trigger the GitHub Actions workflow, which will build the Docker container, push it to Google Artifact Registry, and deploy it to Cloud Run.

### Step 8: Verify Deployment

1. After the workflow completes, check the output logs in the GitHub Actions tab to see if the deployment was successful.
2. You can also verify the deployment by going to the **Cloud Run** section in the Google Cloud Console and checking the service URL.


# 2 - GUIDE TO DEPLOY GOOGLE CLOUD FUNCTIONS
Here’s a step-by-step guide to configure the GitHub Actions workflow for deploying your app to Google Cloud Functions when a commit is pushed to the "main" branch.

### Step 1: Set Up Your Google Cloud Project

1. Go to Google Cloud Console:
   - Visit [Google Cloud Console](https://console.cloud.google.com/).

2. Create a New Project:
   - Click on the project dropdown and select "New Project".
   - Enter a name for your project and note down the project ID (e.g., `vt-gcp-sandbox`).

3. Enable Cloud Functions API:
   - In the left sidebar, navigate to "APIs & Services" > "Library".
   - Search for "Cloud Functions API" and enable it.

### Step 2: Create a Service Account

1. Navigate to IAM & Admin:
   - In the left sidebar, go to "IAM & Admin" > "Service Accounts".

2. Create a Service Account:
   - Click on "Create Service Account".
   - Provide a name and description, then click "Create".

3. Grant Permissions:
   - Assign the role `Cloud Functions Admin` and `Viewer`.
   - Click "Continue" and then "Done".

4. Generate a Key:
   - Find the service account you just created, click on it, and go to the "Keys" tab.
   - Click "Add Key" > "JSON". This will download a JSON file containing your service account key.

### Step 3: Add Service Account Key to GitHub Secrets

1. Go to Your GitHub Repository:
   - Navigate to your repository on GitHub.

2. Access Settings:
   - Click on the "Settings" tab.

3. Add a New Secret:
   - In the left sidebar, click on "Secrets and variables" > "Actions".
   - Click on "New repository secret".
   - Name the secret `GCP_SA_KEY` and paste the contents of the downloaded JSON file.

### Step 4: Create the GitHub Actions Workflow

1. Create a Workflow File**:
   - In your project repository, create a directory called `.github/workflows`.
   - Inside this directory, create a file named `deploy-to-gcloud-function.yml`.

2. Add the Workflow Configuration:
   - Copy and paste the following YAML configuration into `deploy-to-gcloud-function.yml`:


# 3 - DEPLOY FIREBASE
​Here’s a step-by-step guide to configure the GitHub Actions workflow for deploying your app to Firebase Hosting when a commit is pushed to the "frontend" branch.

### Step 1: Create Your Firebase Project

1. **Go to Firebase Console**:
   - Visit [Firebase Console](https://console.firebase.google.com/).

2. **Create a New Project**:
   - Click on "Add project" and follow the prompts to create a new Firebase project.
   - Note down the project ID (e.g., `learn-git-action`).

### Step 2: Set Up Firebase Hosting

1. **Initialize Firebase in Your Project**:
   - Open your terminal and navigate to your project directory.
   - Run the command: `firebase init hosting`
   - Follow the prompts to set up Firebase Hosting, selecting your newly created project.

### Step 3: Generate Firebase Token

1. **Install Firebase CLI**:
   - If you haven't already, install Firebase CLI globally:
     `npm install -g firebase-tools`

2. **Login to Firebase**:
   - Run the command: `firebase login`

3. **Generate a Token**:
   - After logging in, generate a token with: `firebase login:ci`
   - Copy the generated token; you will need it for GitHub Secrets.

### Step 4: Add Firebase Token to GitHub Secrets

1. **Go to Your GitHub Repository**:
   - Navigate to your repository on GitHub.

2. **Access Settings**:
   - Click on the "Settings" tab.

3. **Add a New Secret**:
   - In the left sidebar, click on "Secrets and variables" > "Actions".
   - Click on "New repository secret".
   - Name the secret `FIREBASE_TOKEN` and paste the token you copied earlier.

### Step 5: Create the GitHub Actions Workflow

1. **Create a Workflow File**:
   - In your project repository, create a directory called `.github/workflows`.
   - Inside this directory, create a file named `deploy-to-firebase.yml`.

2. **Add the Workflow Configuration**:
   - Copy and paste the following YAML configuration into `deploy-to-firebase.yml`: