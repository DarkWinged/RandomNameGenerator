demo-ingress.j2:

This file defines an Ingress resource in Kubernetes, which allows external traffic to be routed to the appropriate services within the cluster.
The apiVersion and kind specify the version and type of the resource being created.
The metadata section specifies metadata for the Ingress resource, including its name.
The ingressClassName specifies the class of the Ingress controller to use, in this case, "nginx".
The rules section defines routing rules based on the host.
Under each rule, you specify the host for which the Ingress will handle traffic.
The http section under each rule defines how HTTP traffic should be routed.
Inside the http section, the paths section defines the paths for which traffic should be directed.
Each path specifies a backend service (rng-app-service-dev) and port (2224) to route traffic to.
The pathType is set to Prefix, indicating that the path should be matched as a prefix.

deploy.yaml:

This file defines a Kubernetes Deployment resource, which manages the deployment and scaling of pods.
The apiVersion and kind indicate the version and type of the resource being created.
The metadata section specifies metadata for the Deployment, including its name.
The spec section defines the deployment's specifications.
The replicas field specifies that the deployment should have 3 replicas (3 identical pods).
The selector specifies how the replicas are selected. In this case, they are selected based on the label app: rng-app.
The template section defines the pod template for the deployment.
Under metadata in the template, labels are defined to identify the pods as part of the app: rng-app.
The containers section under spec defines the containers to run within the pods.
Within the containers, a container named rng-container is defined.
The image field specifies the Docker image to use for the container.
The ports section specifies the port mapping for the container, with containerPort set to 2224.

expose.yaml: 

This file defines a Kubernetes Service resource, which enables networking and access to pods.
The apiVersion and kind indicate the version and type of the resource being created.
The metadata section specifies metadata for the Service, including its name.
The spec section defines the Service's specifications.
The selector field specifies that this Service will target pods with the label app: rng-app.
The ports section defines the ports on which the Service should listen and forward traffic.
Under ports, a single port is defined with protocol TCP, port 2224, and target port 2224.
The type field is set to ClusterIP, which means the Service will get an internal IP address within the cluster.

ingress-deploy.yaml

This file sets up various Kubernetes resources for deploying and managing the NGINX Ingress Controller using Helm. It includes configurations for namespaces, service accounts, roles, role bindings, cluster roles, cluster role bindings, config maps, services, deployments, jobs, ingress classes, and webhook configurations related to the Ingress Controller. These resources are used to ensure the proper functioning and management of the NGINX Ingress Controller in the Kubernetes cluster.

ingress.yaml:

This configuration sets up an Ingress resource that directs incoming HTTP traffic with the specified host to the "rng-app-service-dev" service. The host is used to match incoming requests from the given domain. The traffic is then forwarded to the specified service and port. The path and pathType determine how the URL path of the incoming requests is matched and handled.
