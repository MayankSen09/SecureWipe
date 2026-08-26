# Changelog

All notable changes to SecureWipe are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- PKI-signed PDF certificates (X.509 digital signatures)
- Multi-language web portal (FR, HI)
- Ethereum mainnet / Polygon ledger anchoring
- Scheduled batch wipe jobs via API

---

## [1.2.0] — 2026-08-25

### Added
- **Professional README** with live demo link, badges, feature table, sanitization modes comparison, and compliance standards table
- **CONTRIBUTING.md** — full contributor guide with development setup, commit conventions, and PR guidelines
- **SECURITY.md** — responsible vulnerability disclosure policy and security architecture overview
- **CHANGELOG.md** — this file, tracking all notable project changes

### Changed
- Improved `.gitignore` with `.env` protection, Vercel artifact exclusions, and English section headers

---

## [1.1.0] — 2026-08-07

### Added
- **3D Hero Terminal** — interactive terminal in the web UI with VanillaTilt parallax and 3D Bento cards
- **Replay button** on the hero terminal animation
- **Block Explorer** section in the web UI
- **CLI download section** in the web portal
- **Mac-style window controls** on the terminal widget (functional close/minimize/maximize)

### Changed
- Improved CLI theme and terminal color scheme

---

## [1.0.0] — 2026-08-06

### Added
- **Core wipe engine** implementing NIST SP 800-88 (Clear / Purge / Crypto Erase) and ANSSI Palier 1 / 2
- **Audit confidence score engine** (0–100 scale)
- **SHA-256 local blockchain ledger** for tamper-proof certificate anchoring
- **PDF certificate generator** with embedded QR codes (FPDF2)
- **FastAPI REST backend** for certificate verification and PDF downloads
- **Tkinter dark-themed GUI wizard** with multi-step flow
- **Interactive CLI interface** (Rich + Argparse)
- **Android ADB/Fastboot wipe agent**
- **Windows drive enumeration** (WMI + Diskpart)
- **Linux drive detection** with `hdparm` HPA/DCO analysis
- **BitLocker & TCG Opal SED encryption scanner**
- **Internationalization support** (EN / FR / HI)
- **Web verification portal** deployed on Vercel: [https://secure-wipe-omega.vercel.app/](https://secure-wipe-omega.vercel.app/)
- **Mock mode** for safe demonstration without hardware
- Unit test suite for the confidence scoring engine

---

[Unreleased]: https://github.com/MayankSen09/SecureWipe/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/MayankSen09/SecureWipe/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/MayankSen09/SecureWipe/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/MayankSen09/SecureWipe/releases/tag/v1.0.0
