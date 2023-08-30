
# RandomNameGenerator
Alta3 devops final project

## Description
A web application that generates a list of fantasy names when given criteria such as ancestry, gender, and the number of names the user would like. It also has options for adding prefixes and suffixes.

## Installation
In an Alta3 environment, run the following commands:
```bash
cd ~
git clone https://github.com/DarkWinged/RandomNameGenerator.git
cd RandomNameGenerator/k8s
./setup.sh
```

## Contributing
When updating the image, run the following commands:
```bash
cd ~/RandomNameGenerator
export image_name=rng-app
export image_version=<new version>
export dockerfile=<path to the docker file>
export project_repo=randomnamegenerator
export project_group=darkwinged
cd ~/RandomNameGenerator/app
docker build -t ${image_name}:${image_version} -f ${dockerfile} .
```
Test the image with:
```bash
cd ~/RandomNameGenerator/app
docker  run -p 0.0.0.0:2224:2224 ghcr.io/${project_group}/${project_repo}/${image_name}:${image_version}
curl 0.0.0.0:2224
```
Push the image to GH with the following:
```bash
cd ~/RandomNameGenerator/app
docker tag ${image_name}:${image_version} ghcr.io/${project_group}/${project_repo}/${image_name}:${image_version}
docker push ghcr.io/${project_group}/${project_repo}/${image_name}:${image_version}
```

### Authors
#### James L. Rogers | github.com/DarkWinged
#### Derek J. Beerhorst | github.com/Dbeerhorst
#### Maria L. Lis | github.com/crazyzoo143
