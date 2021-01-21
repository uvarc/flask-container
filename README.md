![Docker Build CI](https://github.com/uvarc/flask-container/workflows/Docker%20Build%20CI/badge.svg)

# flask-container

A skeleton Python3 / Flask container template for projects.

## How To Use

- Your app logic should register back to `app.py` as Flask paths, functions, and methods.
- Add any Python3 dependencies to `requirements.txt`

## Run/Test Locally

Flask has a local web server built in for testing and debugging. To run your application:

    python3 app.py

This brings up the server locally on port 5000. Test this locally by using a browser or terminal:

    http://localhost:5000/

Edit app.py and extend your code freely. The local web server will refresh automatically as you work.

## Example Methods 

Request the base path:

    curl http://localhost:5000/

returns

    "Flask Dockerized"

-----

Request a static JSON value using GET

    curl http://localhost:5000/api/person

returns

    {"fname": "Lester", "lname": "Bangs", "year": 1982}

-----

Request a static array rendered in JSON:

    curl http://localhost:5000/api/place

returns

    {"city":"Charlottesville","lat":38.0401199,"long":-78.5025264}

-----

POST a string value and have it returned back in JSON:

    curl -X POST http://localhost:5000/api/user/<username>

returns

    {"user":"foobar"}


-----

POST or GET an integer and have it returned back in JSON:

    curl -X POST http://localhost:5000/api/post/4459

returns

    {"postid":4459}

-----

POST a GitHub user or org name and fetch basic information via their API, in JSON:

    curl -X POST http://localhost:5000/api/github/uvarc

returns

```json
{
  "avatar_url": "https://avatars.githubusercontent.com/u/54042486?v=4", 
  "bio": null, 
  "blog": "https://rc.virginia.edu/", 
  "company": null, 
  "created_at": "2019-08-12T20:10:05Z", 
  "email": null, 
  "events_url": "https://api.github.com/users/uvarc/events{/privacy}", 
  "followers": 0, 
  "followers_url": "https://api.github.com/users/uvarc/followers", 
  "following": 0, 
  "following_url": "https://api.github.com/users/uvarc/following{/other_user}", 
  "gists_url": "https://api.github.com/users/uvarc/gists{/gist_id}", 
  "gravatar_id": "", 
  "hireable": null, 
  "html_url": "https://github.com/uvarc", 
  "id": 54042486, 
  "location": "Charlottesville VA", 
  "login": "uvarc", 
  "name": "UVA Research Computing", 
  "node_id": "MDEyOk9yZ2FuaXphdGlvbjU0MDQyNDg2", 
  "organizations_url": "https://api.github.com/users/uvarc/orgs", 
  "public_gists": 0, 
  "public_repos": 36, 
  "received_events_url": "https://api.github.com/users/uvarc/received_events", 
  "repos_url": "https://api.github.com/users/uvarc/repos", 
  "site_admin": false, 
  "starred_url": "https://api.github.com/users/uvarc/starred{/owner}{/repo}", 
  "subscriptions_url": "https://api.github.com/users/uvarc/subscriptions", 
  "twitter_username": null, 
  "type": "Organization", 
  "updated_at": "2021-01-13T16:23:18Z", 
  "url": "https://api.github.com/users/uvarc"
}
```


## Build the Container

The included Dockerfile will build your Flask application into a container with a production server (nginx)
which is more robust than the built-in Flask web server. Note that nginx runs on port 80, the typical port
for production web servers.

From within your cloned and extended version of this repository, first build the container:

```
docker build -t ORG/CONTAINER:TAG .
```

Next you can run the container locally to test. Map port 80 of the container to port 8080 of your workstation:

```
docker run -d -p 8080:80 ORG/CONTAINER:TAG
```

Once that runs (check its status with `docker ps`) you can see the Flask site by visiting http://localhost:8080/ in your browser.

Finally, commit and push your code. You can also push your container image to Docker Hub or another registry:

```
docker push ORG/CONTAINER:TAG
docker push ghcr.io/ORG/CONTAINER:TAG
```

## Launching in DCOS @ UVA

1. Work with UVA Research Computing to set up your initial Flask service. This may include "production" and "dev" sites along with your `master` and `dev` branches in Git.
2. We recommend using a CI/CD tool such as GitHub Actions to build and deploy your application container with each `git push`. See the example `.github/workflows/main.yml` file for a basic build+push.
3. UVARC can integrate your build so that it is launched in DCOS as part of that build process.
