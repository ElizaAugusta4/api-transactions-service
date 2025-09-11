#!/bin/bash
set -e


if ! command -v kubectl &> /dev/null; then
  echo "Instalando kubectl..."
  curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
fi


if [ -z "$KUBE_CONFIG_DATA" ]; then
  echo "KUBE_CONFIG_DATA não definido!"
  exit 1
fi

echo "$KUBE_CONFIG_DATA" | base64 --decode > kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig


kubectl apply -f K8s-manifests/


for DEPLOY in accounts-service transactions-service balance-service; do
  kubectl rollout status deployment/$DEPLOY
done


sleep 10


for SVC in accounts-service transactions-service balance-service; do
  APP_SERVICE=$(kubectl get svc $SVC -o jsonpath='{.spec.clusterIP}')
  APP_PORT=$(kubectl get svc $SVC -o jsonpath='{.spec.ports[0].port}')
  echo "Health check: $SVC"
  curl --fail http://$APP_SERVICE:$APP_PORT/health || {
    echo "Health check falhou para $SVC!"
    exit 1
  }
done

echo "Deploy validado com sucesso para todos os serviços!"