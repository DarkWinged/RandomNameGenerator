#! /bin/bash

echo finding baseurl
export BASEURL="aux1-$(hostname -d).live.alta3.com"
j2 ingress.j2  -o ingress.yaml
echo ${BASEURL}
echo applying ingress-deploy.yaml
kubectl apply -f ingress-deploy.yaml
echo building nginx-ingress
./nginx-builder.py && sudo cp ~/RandomNameGenerator/k8s/nginx-ingress /etc/nginx/sites-enabled/ && sudo nginx -t && sudo nginx -s reload
echo applying configmap.yaml
kubectl apply -f configmap.yaml
echo applying deploy.yaml
kubectl apply -f deploy.yaml
echo applying expose.yaml
kubectl apply -f expose.yaml
echo applying ingress.yaml
sleep 20 #Delay building the ingress controller while the reqired resources finish setting up
kubectl apply -f ingress.yaml
