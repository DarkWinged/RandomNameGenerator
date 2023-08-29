#! /bin/bash

sudo cp ~/RandomNameGenerator/k8s/nginx-ingress /etc/nginx/sites-enabled/
sudo nginx -t
sudo nginx -s reload
echo applying configmap.yaml
kubectl apply -f configmap.yaml
echo applying deploy.yaml
kubectl apply -f deploy.yaml
echo applying expose.yaml
kubectl apply -f expose.yaml
echo applying ingress.yaml
kubectl apply -f ingress.yaml
