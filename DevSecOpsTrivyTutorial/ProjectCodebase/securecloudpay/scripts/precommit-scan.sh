#!/bin/bash

echo "🛡️ Trivy Pre-commit Scan Started..."

echo "🔍 Scanning file system..."
trivy fs --scanners vuln,secret .

echo "🔧 Scanning Dockerfiles and IaC configs..."
trivy config .

echo "✅ Scan complete."
