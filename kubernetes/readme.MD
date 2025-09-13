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
