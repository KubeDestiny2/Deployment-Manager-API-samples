# Deployment-Manager-samples


# Overview
This is a Google Cloud Deployment Manager template which deploys a GKE cluster and a Deployment Manager type. The type can be used by other deployments to deploy Kubernetes resources into the cluster.

# Getting started
Using Deployment Manager to deploy Kubernetes resources into a new GKE cluster is a two step process, as described below.

# Deploy a cluster
Using cluster.yaml, deploy a GKE cluster to use for deploying the solution later. Fill in the following information before deploying:

zone in which to run the cluster
basicauth username and password for authenticating access to the cluster
When ready, deploy with the following command:

gcloud deployment-manager deployments create gke-cluster --config cluster.yaml
This will result in two resources:

a GKE cluster named gke-cluster-my-cluster
a Deployment Manager type named gke-cluster-my-cluster-type
