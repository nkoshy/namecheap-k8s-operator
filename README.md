# Namecheap k8s operator
Kubernetes operator that automatically manages Namecheap DNS records based on custom resources definitions(CRDs), enabling dynamic DNS management for Kubernetes-hosted applications.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Namecheap DNS Operator is a Kubernetes operator designed to simplify and automate the management of DNS records for domains hosted on Namecheap. It allows you to create, update, and delete DNS records directly from your Kubernetes cluster using custom resources.

## Features

- Automatically create, update, and delete DNS records on Namecheap
- Supports multiple record types (A, CNAME, MX, TXT)
- Kubernetes-native approach using Custom Resource Definitions (CRDs)
- Easy integration with existing Kubernetes workflows
- Preserves existing DNS records not managed by the operator

## Prerequisites

- Kubernetes cluster (version 1.16+)
- `kubectl` command-line tool
- Namecheap account with API access enabled
- Namecheap API key and credentials

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/nkoshy/namecheap-k8s-operator.git
   cd namecheap-k8s-operator
   ```

2. Install the Custom Resource Definition (CRD):
   ```
   kubectl apply -f config/crd/namecheap_v1_nameacheapdnsrecord.yaml
   ```

3. Create a secret with your Namecheap API credentials:
   ```
   kubectl create secret generic namecheap-credentials \
     --from-literal=api-user=your_api_user \
     --from-literal=api-key=your_api_key \
     --from-literal=username=your_username \
     --from-literal=client-ip=your_client_ip \
     -n namecheap-system
   ```

4. Deploy the operator:
   ```
   kubectl apply -f config/deploy/operator.yaml
   ```

## Usage

To manage a DNS record, create a `NamecheapDNSRecord` custom resource:

```yaml
apiVersion: namecheap.com/v1
kind: NamecheapDNSRecord
metadata:
  name: example-record
spec:
  domain: example.com
  subdomain: www
  recordType: A
  value: 203.0.113.1
  ttl: 3600
```

Apply this resource to your cluster:

```
kubectl apply -f example-record.yaml
```

The operator will automatically create or update the specified DNS record on Namecheap.

To delete a record, simply delete the custom resource:

```
kubectl delete nameacheapdnsrecord example-record
```

## Configuration

The operator can be configured using the following environment variables:

- `NAMECHEAP_API_USER`: Namecheap API username
- `NAMECHEAP_API_KEY`: Namecheap API key
- `NAMECHEAP_USERNAME`: Namecheap account username
- `NAMECHEAP_CLIENT_IP`: Client IP address for API access

These should be set in the operator's deployment, referencing the secret created during installation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
