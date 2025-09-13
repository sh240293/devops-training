# Kubernetes Installation on CentOS 7 with Calico

This guide explains how to install a Kubernetes cluster on **CentOS 7** using **kubeadm** and **Calico** as the CNI plugin.  
We will use the pod network **10.244.0.0/16**.

---

## 📋 Prerequisites

- CentOS 7 (minimal installation recommended)
- At least 2 GB RAM per node
- Internet connectivity
- `root` or `sudo` access

---

## ⚙️ 1. System Preparation (All Nodes)

```bash
# Disable SELinux
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

# Disable swap
sudo swapoff -a
sudo sed -i '/swap/d' /etc/fstab

# Enable required kernel module
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF
sudo modprobe br_netfilter

# Configure sysctl
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```
---

## 🔥 2. Configure Firewall Rules
Master Node
```
sudo firewall-cmd --permanent --add-port=6443/tcp        # API Server
sudo firewall-cmd --permanent --add-port=2379-2380/tcp   # etcd
sudo firewall-cmd --permanent --add-port=10251/tcp       # Scheduler
sudo firewall-cmd --permanent --add-port=10252/tcp       # Controller Manager
sudo firewall-cmd --permanent --add-port=10250/tcp       # Kubelet
```
Worker Nodes
```
sudo firewall-cmd --permanent --add-port=10250/tcp       # Kubelet
sudo firewall-cmd --permanent --add-port=30000-32767/tcp # NodePort range
```
All Nodes (for Calico)
```
sudo firewall-cmd --permanent --add-port=179/tcp         # BGP
sudo firewall-cmd --permanent --add-protocol=4           # IP-in-IP
```
Apply changes:
```
sudo firewall-cmd --reload
```
---
## 🐳 3. Install Container Runtime (Docker)
```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker
```
---
## 📦 4. Install Kubernetes Components
```
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.30/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.30/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

## 🖥️ 5. Initialize Control Plane (Master Only)
```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```
Configure kubectl for the current user:
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
---
## 🌐 6. Install Calico Network Plugin
```
curl -O https://docs.projectcalico.org/manifests/calico.yaml
sed -i 's?192.168.0.0/16?10.244.0.0/16?g' calico.yaml
kubectl apply -f calico.yaml
```
Verify Calico pods:
```
kubectl get pods -n kube-system
```
---
## 👷 7. Join Worker Nodes
On each worker node, run the join command provided by kubeadm init, for example:
```
sudo kubeadm join <MASTER_IP>:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>
```
---
## ✅ 8. Verification
On the master node:
```
kubectl get nodes -o wide
kubectl get pods -A -o wide
```
---
