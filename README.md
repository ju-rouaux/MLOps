# Streamlining Machine Learning: A Simple MLOps Pipeline in Action
A School Project to Get Hands-On Experience with MLOps Technology.

## Run
**HIGHLY RECOMMENDED BEFORE RUNNING THE APPLICATION** \
To accelerate data acquisition from GitHub, create a ``.env``  file at the root of the repository containing the following line. See: [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

```
GITHUB_TOKEN=github_pat_XXXXXXXXX
```

### Launch everything at once
Downloading the images may take some time initially.
```
docker compose up --build
```

### Changing the location of application data
By default, the application will create a ``.temp`` directory at the root of the repository. To change the location, simply add the following line to the ``.env`` file.
```
WORKING_DIRECTORY=/absolute/path/to/any/location
```

## Usage


### Application
Main application demo.
1. Navigate to ``http://localhost:8000/``
2. Copy and paste any README file content into the text field
3. Click **Predict**
4. Enjoy the prediction ✨

**Note:** The application will not start and will continuously restart if no model is available. Refer to the MLFlow section to register a model.

### MLFlow
View and register new models.

#### Create a new model
1. Optionally run the dev container (Visual Studio Code recommended)
2. Through the notebook ``Model-from-Mongo.ipynb``, train a model and push it to MLFlow

#### Register a model
1. Navigate to ``http://localhost:8090/``
2. Select your preferred run
3. Register the model under the name ``ApplicationModel``

#### Deploy a model to production
4. Add an alias ``prod`` to the version you want to push to production (the model under the name ``ApplicationModel``)
5. Restart the ``front-app`` container to reload the model

### Grafana
Real-time database visualization dashboard.
1. Navigate to ``http://localhost:3000/``
2. Login: ``admin`` \
Password: ``admin``
3. Go to Dashboard > Database Visualization

### MongoDB
MongoDB Compass is recommended to explore and edit the database. \
To connect, use the default configuration. No login required.
