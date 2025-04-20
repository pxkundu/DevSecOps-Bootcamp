
# EKS Cluster Status and DevSecOps Scan Script

## What is this script?

This is a bash script designed to provide a quick overview of the status and health of an Amazon Elastic Kubernetes Service (EKS) cluster. It executes a series of `kubectl` and `aws eks` commands to gather relevant information and presents it in a single report file. Additionally, it includes checks for various configurations that are relevant from a DevSecOps perspective, helping to identify potential security risks and adherence to best practices.

## Why use this script?

For DevSecOps professionals and anyone managing EKS clusters, understanding the current state of the cluster is crucial for maintaining stability, performance, and security. This script helps by:

* **Quickly assessing cluster health:** Identify unhealthy nodes, problematic pods, and recent error events.

* **Pinpointing potential issues:** Highlight areas that might be experiencing resource constraints or configuration problems.

* **Providing basic security and configuration insights:** Check for common misconfigurations, review RBAC settings, list network policies, and identify potential improper handling of sensitive data.

* **Generating a shareable report:** Create a single file containing all the gathered information for analysis, sharing, or documentation.

* **Being interactive:** Guides the user to provide necessary cluster details before execution.

This script serves as a convenient first step in diagnosing cluster issues or performing routine checks, offering a consolidated view that would otherwise require running multiple individual commands.

## How to use the script

### Prerequisites

Before running the script, ensure you have the following installed and configured on the machine where you will execute it:

* **`kubectl`**: The Kubernetes command-line tool.

* **`aws CLI`**: The Amazon Web Services command-line interface.

* **`jq`**: A lightweight and flexible command-line JSON processor.

* **AWS Credentials:** Your AWS credentials must be configured with sufficient permissions to:

  * Describe EKS clusters (`eks:DescribeCluster`).

  * Update kubeconfig (`eks:UpdateKubeconfig`).

  * Access Kubernetes resources via `kubectl` (e.g., `kubernetes:*/pods`, `kubernetes:*/nodes`, `kubernetes:*/events`, `kubernetes:*/namespaces`, `kubernetes:*/roles`, `kubernetes:*/clusterroles`, `kubernetes:*/rolebindings`, `kubernetes:*/clusterrolebindings`, `kubernetes:*/networkpolicies`, `kubernetes:*/secrets`, `kubernetes:*/configmaps`). This typically involves permissions granted through IAM roles mapped to Kubernetes RBAC.

### Installation and Setup

1. **Save the script:** Save the provided bash script code to a file (e.g., `eks_scan.sh`).

2. **Make the script executable:** Open your terminal, navigate to the directory where you saved the file, and run:

   ```bash
   chmod +x eks_scan.sh
   ```

3. **Ensure AWS credentials are configured:** Verify your AWS CLI is configured (e.g., by running `aws configure` or ensuring environment variables like `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` are set).

### Execution

Run the script from your terminal:

```bash
./eks_scan.sh
```

The script will then interactively ask you for the following information:

1. **EKS Cluster Name:** The name of the EKS cluster you want to scan.

2. **AWS Region:** The AWS region where your EKS cluster is located (e.g., `us-east-1`).

### Report Output

The script will execute the commands and save the output to a report file in the same directory. The filename will follow the format `eks_cluster_report_YYYYMMDD_HHMMSS.txt`, where `YYYYMMDD_HHMMSS` is the timestamp when the script was run.

### Interpreting the Results

The report file is structured with sections for each type of information gathered. Each section includes the raw output from the commands and an "Interpretation" section explaining what the information means and what potential issues to look for from a DevSecOps perspective. Review the report carefully, paying close attention to:

* Any errors or warnings during script execution.

* Non-`ACTIVE` cluster status.

* Nodes that are not `Ready` or show resource pressure.

* Pods that are not `Running` or have high restart counts, especially in the `kube-system` namespace.

* Recent `Warning` or `Error` events.

* Findings in the security and configuration checks related to RBAC, Network Policies, default service accounts, privileged containers, risky capabilities, `hostPath` volumes, image pull policies, and potential secrets in ConfigMaps.

## Script Features (Checks Performed)

The script performs the following checks:

* **Dependency Check:** Verifies the presence of `kubectl`, `aws`, and `jq`.

* **kubectl Configuration:** Configures `kubectl` to interact with the specified EKS cluster.

* **Cluster General Information:** Retrieves basic details about the EKS cluster, including API endpoint access configuration.

* **Node Status:** Lists all nodes and their status, age, version, and IP addresses.

* **Node Resource Utilization:** (If `kubectl-top` is installed) Shows CPU and memory usage for each node.

* **Pod Status:** Lists pods that are not in a `Running` state or have been restarted, as well as all pods in the `kube-system` namespace.

* **Recent Events:** Shows the most recent non-`Normal` cluster events (Warnings and Errors).

* **RBAC Roles and Bindings:** Lists ClusterRoles, Roles, ClusterRoleBindings, and RoleBindings to help understand defined permissions.

* **Network Policies:** Lists Network Policies in all namespaces to show how network traffic is controlled.

* **Basic Security Checks:**

  * Identifies pods potentially using the default service account without disabling token automount.

  * Lists containers running in privileged mode.

  * Identifies pods using `hostPath` volumes.

* **Enhanced Security Check:**

  * Lists containers that add potentially risky capabilities (e.g., `NET_ADMIN`, `SYS_ADMIN`).

* **Image Pull Policy Check:** Lists containers without an explicit `ImagePullPolicy: Always` set.

* **Secrets and ConfigMaps Listing:** Lists all Secrets and ConfigMaps in the cluster.

* **Potential Secrets in ConfigMaps Check:** (Heuristic) Checks ConfigMaps for values that appear to be base64 encoded, which might indicate improperly stored secrets.

## Disclaimer

This script provides a basic overview and highlights common areas of concern. It is not a substitute for comprehensive monitoring solutions, logging analysis, or dedicated Kubernetes security scanning tools. For in-depth security assessments, consider using specialized tools and services. The check for secrets in ConfigMaps is heuristic and may produce false positives.

## License

This script is released under an open-source license. Feel free to modify and distribute it.

## Contributions

Contributions are welcome! If you have suggestions for improvements or additional checks, please feel free to contribute.

---

*Prepared by {Partha Sarathi Kundu} on April 19, 2025, for the EKS Cluster Status Scanner project.*