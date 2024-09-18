#!/bin/bash

# Namespace
NAMESPACE="wash-and-dry"

# Get the pod name
POD_NAME=$(kubectl get pods -n $NAMESPACE -l app=waterfall-app -o jsonpath="{.items[0].metadata.name}")

# Check if the pod name was found
if [ -z "$POD_NAME" ]; then
  echo "Waterfall app pod not found in namespace $NAMESPACE"
  exit 1
fi

# Open a shell session in the pod and navigate to the waterfall directory
kubectl exec -it $POD_NAME -n $NAMESPACE -- /bin/sh -c "cd /var/log/waterfall && ls && cat waterfall-view.txt"
