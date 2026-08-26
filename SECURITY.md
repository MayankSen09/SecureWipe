# Security Policy

## Supported Versions

The following versions of SecureWipe currently receive security updates:

| Version | Supported |
|:--------|:---------:|
| `main` branch | ✅ |
| Older releases | ❌ |

---

## 🛡️ Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in SecureWipe, **please do NOT open a public GitHub issue**.

Instead, report it responsibly by:

1. **Email**: Send a detailed report to the repository maintainer via GitHub's [private security advisory](https://github.com/MayankSen09/SecureWipe/security/advisories/new) feature.
2. **Include in your report:**
   - A clear description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact and severity assessment
   - Any suggested mitigation or fix

We will acknowledge your report within **72 hours** and aim to provide a fix within **14 days** for critical vulnerabilities.

---

## 🔐 Security Architecture

SecureWipe's core trust model relies on:

- Cryptographic signatures generated on audit certificates.
- SHA-256 block-chain ledger entries recorded in `trust/chain.json`.
- Strict boundaries preventing modifications to system drive partitions.

### Out-of-Scope Security Considerations

- **Physical access** to the machine running SecureWipe is assumed to be controlled by the operator
- **Certificate PDFs** are tamper-evident via blockchain anchoring but are not digitally signed with a PKI certificate (planned feature)
- **The local blockchain ledger** (`trust/chain.json`) should be stored on a write-protected or access-controlled system in production deployments

---

## 🌐 Live Portal Security

The live demo at [https://secure-wipe-eta.vercel.app/](https://secure-wipe-eta.vercel.app/) is a **read-only verification portal**. It does not accept uploads, does not store user data, and does not process live wipe operations.
