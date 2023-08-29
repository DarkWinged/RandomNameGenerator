#! /bin/bash

kubectl delete -f configmap.yaml
kubectl delete -f deploy.yaml
kubectl delete -f expose.yaml
kubectl delete -f ingress-deploy.yaml
kubectl delete -f ingress.yaml
rm ingress.yaml
sudo rm /etc/nginx/sites-enabled/nginx-ingress
sudo nginx -t
sudo nginx -s reload
