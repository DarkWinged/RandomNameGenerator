#! /bin/bash

echo finding baseurl
export BASEURL="aux1-$(hostname -d).live.alta3.com"
j2 ingress.j2  -o ingress.yaml
echo ${BASEURL}
echo applying ingress-deploy.yaml
kubectl apply -f ingress-deploy.yaml
kubectl get service ingress-nginx-controller -n ingress-nginx -o jsonpath='{.spec.ports[*]}{"\n"}' | jq
echo EDIT THE ./nginx-ingress TO ADD THE NODE PORT
