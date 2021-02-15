https://kompose.io/

# Linux
curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-linux-amd64 -o kompose

# macOS
curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-darwin-amd64 -o kompose

chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose

cd infra/kubernetes
cd backend
kompose convert
kubectl apply -f *.yaml

cd ../frontend
kompose convert
kubectl apply -f *.yaml

kubectl get po
