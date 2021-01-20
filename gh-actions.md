# GitHub Actions to build a container

The steps below will generate automated builds for a container repository, including scheduled builds.

## Setup

- Your github action (GHA) logic resides in a YAML file located in `.github/workflows/*`.
- Container images need to be pushed to a container registry for consumption by your application. We recommend using either Docker Hub or GitHub Packages.
- GHA documentation and syntax can be found [here](https://docs.github.com/en/actions).

### Repository secrets

Your action needs to log into Docker Hub or GitHub on your behalf. Since authentication involves sensitive information, usernames and passwords (or tokens) should never be
committed in code. Instead, set up secrets for either Docker or GitHub and rotate them periodically:

**Docker Hub**

1. Use a Docker Account username and [access token](https://docs.docker.com/docker-hub/access-tokens/) for CLI authentication.
2. In the SETTINGS for your GitHub repository, create two repository secrets:
  - `DOCKER_USERNAME` - with the Docker username.
  - `DOCKER_TOKEN` - with the Docker access token.

**GitHub Packages**

1. Use a GitHub Account username and [PAT](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) (personal access token) for CLI authentication.
2. In the SETTINGS for your GitHub repository, create two repository secrets:
  - `GH_USER` - with the GitHub username.
  - `GH_PAT` - with the GitHub PAT.

## Build your container on `git push`

For any branch you can trigger a container build. You may want additional logic for each branch, so that
a `dev` branch might create a `:latest` container image, while the `main` branch creates a `:prod` image, etc.

The following action is triggered to run for pushes to the `main` branch and contains two parallel jobs:
one to build and push the container to Docker Hub, and another to build and push to GitHub Packages. These
two jobs are independent of one another.

```
name: Container Build CI

on:
  push:
    branches:
    - 'main'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v1
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      - 
        name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}
      -
        name: Build and push
        id: docker_build
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: ORG/CONTAINER:LABEL
      -
        name: Image digest
        run: echo ${{ steps.docker_build.outputs.digest }}

  publish:
    runs-on: ubuntu-latest
    steps:
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v1
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      -
        name: Login to GHCR
        uses: docker/login-action@v1
        with:
          registry: ghcr.io
          username: ${{ secrets.GH_USER }}
          password: ${{ secrets.GH_PAT }}
      -
        name: Build and push
        id: docker_build
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: ghcr.io/ORG/CONTAINER:LABEL
      -
        name: Image digest
        run: echo ${{ steps.docker_build.outputs.digest }}
```

Note that container images pushed to GitHub Packages will be listed, but may be marked "private" by default.
You can change that at any time within the Package settings.

## Build your container on a schedule

Setting a build schedule is simple. Just add the following conditions to your `on:` statement, using
`cron` based scheduling (times are in UTC):

```
name: Container Build CI

on:
  push:
    branches:
    - 'main'
  schedule:
    - cron: '0 8 * * *'

  . . .

```

Note that GitHub actions only builds your default branch on a schedule.

## Use your Container image

To pull an image from Docker Hub:

    docker pull ORG/CONTAINER:TAG

To pull an image from GitHub Packages:

    docker pull ghcr.io/ORG/CONTAINER:TAG


## Integration with DCOS @ UVA

If your container is running as a DCOS service, it is possible to refresh the container image automatically
using an additional step in your GitHub Action. Contact UVARC for more details.
