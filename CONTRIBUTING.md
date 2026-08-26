# Contributing to SecureWipe

Thank you for your interest in contributing to SecureWipe! We welcome contributions of all kinds — bug fixes, new features, documentation improvements, and more.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Reporting Issues](#reporting-issues)

---

## 🤝 Code of Conduct

By participating in this project, you agree to be respectful, inclusive, and constructive in all interactions. We are committed to providing a welcoming environment for everyone.

---

## 🚀 Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```powershell
   git clone https://github.com/<your-username>/SecureWipe.git
   cd SecureWipe
   ```
3. **Add the upstream remote:**
   ```powershell
   git remote add upstream https://github.com/MayankSen09/SecureWipe.git
   ```

---

## 🛠️ Development Setup

```powershell
# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux / macOS

# Install all dependencies
pip install -r requirements.txt

# Run the demo to verify your setup
.\venv\Scripts\python.exe demo.py
```

---

## 🔄 How to Contribute

### Bug Fixes

1. Check the [Issues](https://github.com/MayankSen09/SecureWipe/issues) tab to see if the bug is already reported
2. If not, open a new issue describing the bug before starting work
3. Create a branch: `git checkout -b fix/description-of-bug`
4. Write a failing test that demonstrates the bug (if possible)
5. Fix the bug and ensure all tests pass
6. Submit a Pull Request

### New Features

1. Open an issue first to discuss the proposed feature
2. Wait for approval/feedback before investing significant time
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Implement the feature with appropriate tests
5. Update documentation if needed
6. Submit a Pull Request

### Documentation

Documentation improvements are always welcome and can be submitted directly as a Pull Request without prior issue discussion.

---

## ✍️ Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|:-----|:------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `style` | Code style changes (formatting, whitespace) |
| `refactor` | Code refactoring without feature changes |
| `test` | Adding or updating tests |
| `chore` | Build process, tooling, or dependency updates |
| `perf` | Performance improvements |

### Examples

```
feat(core): add NVMe secure erase via nvme-cli
fix(cert): handle missing QR code library gracefully
docs: update README with Vercel deployment link
test(confidence): add edge case tests for zero-byte drives
```

---

## 📥 Pull Request Guidelines

Before submitting a PR:

- [ ] Run the test suite: `.\venv\Scripts\python.exe -m unittest discover tests`
- [ ] Ensure the demo script still works: `.\venv\Scripts\python.exe demo.py`
- [ ] Update `README.md` if you changed user-facing functionality
- [ ] Add entries to the changelog (if maintained)
- [ ] Reference any related issues in your PR description using `Closes #123`

### PR Title Format

Follow the same Conventional Commits format as commit messages.

---

## 🐛 Reporting Issues

When opening an issue, please include:

- **Python version** (`python --version`)
- **Operating system** (Windows 10/11, Ubuntu 22.04, etc.)
- **Steps to reproduce** the issue
- **Expected behavior** vs. **actual behavior**
- **Relevant logs or error output**

---

## 🙏 Thank You

Every contribution, no matter how small, is valued and appreciated. Together we can make data sanitization more trustworthy and accessible for everyone.

**[🌐 Live Demo](https://secure-wipe-omega.vercel.app/) · [📖 README](README.md) · [🔗 Issues](https://github.com/MayankSen09/SecureWipe/issues)**
