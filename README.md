# Déploiement de l'application Flask sur Kubernetes

## Prérequis

- Kubernetes installé (Minikube recommandé)
- Docker installé

## Étapes pour déployer l'application

1. **Démarrer Minikube avec 3 nœuds :**

   ```bash
   minikube start --nodes 3 --driver=docker
   ```

2. **Appliquer les fichiers de manifeste :**

   ```bash
   kubectl apply -f k8s/
   ```

3. **Vérifier le déploiement :**

   ```bash
   kubectl get deployments
   kubectl get services
   ```

4. **Accéder à l'application :**
   Utilisez l'IP de Minikube et le NodePort pour accéder à l'application.
   ```bash
   minikube service flask-api
   ```

## Endpoints de santé

- **Readiness Probe:** `/health/ready`
- **Liveness Probe:** `/health/live`
