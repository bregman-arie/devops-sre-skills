---
id: triage-eks-node-notready
name: Triage EKS Node NotReady
description: Diagnose EKS worker nodes in NotReady and determine safe remediation.
tags: [aws, eks, kubernetes, nodes, triage]
maturity: draft
inputs:
  cluster: string
  node: string?
outputs:
  - suspected_cause
  - safe_next_steps
tools_allowed:
  - k8s.get
  - k8s.describe
  - aws.ec2_describe
  - aws.eks_describe
safety:
  default_mode: read_only
  forbidden: [aws.autoscaling_terminate, k8s.drain]
  requires_confirmation_for: [k8s.drain, aws.autoscaling_terminate]
---

## When to use

Use when EKS nodes show `NotReady`, `Unknown`, or pods cannot schedule due to node health.

## Preconditions

- You can access Kubernetes node status and AWS instance health.

## Procedure

1. Confirm which nodes are affected and whether it is a single nodegroup/az.
2. Inspect node conditions and kubelet-related events.
3. Identify whether the node is reachable and if CNI is failing.
4. Check EC2 instance status checks and recent scaling events.
5. Decide between waiting, draining, or replacing the node.

## Decision points

- Single node failure: drain/replace after confirming workloads can move.
- Many nodes in same nodegroup/az: suspect networking, IAM, AMI, or a rollout.
- CNI failure symptoms: verify VPC CNI health and ENI/IP exhaustion.

## Verification

- Nodes return to `Ready` or are replaced and the new nodes are `Ready`.
- Pending pods schedule and workload health stabilizes.

## Rollback / undo

- Revert recent nodegroup/AMI/config changes if correlated.
- If replacement worsens impact, pause nodegroup rollouts.

## Escalation

- Platform team for cluster-wide networking/CNI issues.
- AWS support if underlying EC2 issues persist.

## Examples

```bash
kubectl get nodes
kubectl describe node <node>
```
