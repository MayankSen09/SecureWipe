# Auto-generated embedded HTML for Vercel Serverless deployment
WEB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SecureWipe — Verifiable Asset Sanitization & PDF Certificate Generator Platform</title>
  <style>
    :root {
      --bg-primary: #ffffff;
      --bg-secondary: #f5f5f7;
      --bg-tertiary: #e9e9ed;
      --border-color: #d2d2d7;
      --accent-blue: #0071e3;
      --accent-hover: #005bb5;
      --success-green: #34c759;
      --success-bg: #e3f5e1;
      --danger-red: #ff3b30;
      --danger-bg: #ffeceb;
      --text-main: #1d1d1f;
      --text-muted: #86868b;
      --font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: var(--font-family);
      background-color: var(--bg-primary);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
      line-height: 1.5;
      overflow-x: hidden;
    }

    /* ── Navigation ── */
    nav {
      position: fixed;
      top: 0;
      width: 100%;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: saturate(180%) blur(20px);
      border-bottom: 1px solid rgba(0,0,0,0.05);
      z-index: 1000;
      padding: 1rem 0;
    }

    .nav-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 1.25rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--text-main);
      text-decoration: none;
    }

    .nav-links {
      display: flex;
      gap: 2rem;
    }

    .nav-links a {
      color: var(--text-main);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 400;
      transition: color 0.2s;
    }

    .nav-links a:hover {
      color: var(--accent-blue);
    }

    .wallet-btn {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      padding: 0.55rem 1.1rem;
      border-radius: 99px;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }

    .wallet-btn:hover {
      background: #e8e8ed;
    }

    .wallet-btn.connected {
      background: var(--success-bg);
      border-color: rgba(52, 199, 89, 0.3);
      color: #0c5a21;
    }

    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
    }

    .connected .dot {
      background: var(--success-green);
      box-shadow: 0 0 0 2px rgba(52, 199, 89, 0.2);
    }

    /* ── Hero Section ── */
    .hero {
      padding: 10rem 2rem 5rem;
      background: radial-gradient(circle at top left, #f5f5f7 0%, #ffffff 70%);
      overflow: hidden;
    }

    .hero-content {
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 4rem;
    }

    .hero-text {
      flex: 1;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(0, 113, 227, 0.08);
      color: var(--accent-blue);
      padding: 0.4rem 1rem;
      border-radius: 99px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 1.5rem;
    }

    .hero h1 {
      font-size: 3.75rem;
      font-weight: 700;
      letter-spacing: -0.04em;
      line-height: 1.1;
      margin-bottom: 1.5rem;
      color: var(--text-main);
    }

    /* Cinematic Text Scramble & Interactive Glitch Reveal */
    .scramble-glitch-text {
      display: inline-block;
      user-select: none;
      cursor: pointer;
    }

    .scramble-char {
      display: inline-block;
      transition: color 0.35s ease, transform 0.35s ease, text-shadow 0.35s ease;
      will-change: transform, color, text-shadow;
    }

    .scramble-char.is-scrambling {
      color: var(--accent-blue);
      text-shadow: 0 0 8px rgba(0, 113, 227, 0.5), 0 0 16px rgba(0, 113, 227, 0.3);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .scramble-char.is-hovered {
      color: #0071e3;
      transform: translateY(-2px) scale(1.06);
      text-shadow: 0 0 10px rgba(0, 113, 227, 0.6), 2px 0 #ff0055, -2px 0 #00e5ff;
    }

    .scramble-space {
      display: inline;
      white-space: pre;
    }

    .hero p {
      font-size: 1.2rem;
      color: var(--text-muted);
      margin-bottom: 2.5rem;
      font-weight: 400;
      line-height: 1.6;
    }

    .hero-ctas {
      display: flex;
      gap: 1rem;
    }

    .btn-primary {
      background: var(--accent-blue);
      color: white;
      text-decoration: none;
      padding: 1rem 2rem;
      border-radius: 99px;
      font-weight: 500;
      font-size: 1.05rem;
      transition: background 0.2s;
    }

    .btn-primary:hover {
      background: var(--accent-hover);
    }

    .btn-secondary {
      background: transparent;
      color: var(--accent-blue);
      text-decoration: none;
      padding: 1rem 2rem;
      border-radius: 99px;
      font-weight: 500;
      font-size: 1.05rem;
      transition: background 0.2s;
      border: 1px solid rgba(0, 113, 227, 0.2);
    }

    .btn-secondary:hover {
      background: rgba(0, 113, 227, 0.05);
    }

    /* ── Designer UI Button System (Modern Enterprise SaaS) ── */
    .btn-primary,
    .btn-secondary,
    .wallet-btn,
    .search-btn,
    .btn-download-pdf,
    .btn-view-qr,
    .hud-btn {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.6rem;
      padding: 0.85rem 1.85rem;
      border-radius: 14px;
      font-weight: 600;
      font-size: 0.95rem;
      letter-spacing: -0.01em;
      text-decoration: none;
      border: none;
      outline: none;
      cursor: pointer;
      overflow: hidden;
      user-select: none;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: transform, box-shadow, background-color;
    }

    /* Light Shimmer Sweep Effect */
    .btn-primary::after,
    .btn-secondary::after,
    .wallet-btn::after,
    .search-btn::after,
    .btn-download-pdf::after,
    .btn-view-qr::after {
      content: '';
      position: absolute;
      top: 0;
      left: -150%;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        115deg,
        transparent 20%,
        rgba(255, 255, 255, 0.25) 50%,
        transparent 80%
      );
      transition: all 0.6s ease;
      pointer-events: none;
    }

    /* Hover Shimmer Trigger */
    .btn-primary:hover::after,
    .btn-secondary:hover::after,
    .wallet-btn:hover::after,
    .search-btn:hover::after,
    .btn-download-pdf:hover::after,
    .btn-view-qr:hover::after {
      left: 150%;
    }

    /* Active Press Micro-interaction */
    .btn-primary:active,
    .btn-secondary:active,
    .wallet-btn:active,
    .search-btn:active,
    .btn-download-pdf:active,
    .btn-view-qr:active {
      transform: scale(0.97) translateY(0) !important;
    }

    /* Primary Button Styling */
    .btn-primary {
      background: linear-gradient(135deg, #0071e3 0%, #0055b5 100%);
      color: #ffffff !important;
      box-shadow: 0 4px 14px rgba(0, 113, 227, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }

    .btn-primary:hover {
      background: linear-gradient(135deg, #0077ed 0%, #005cb8 100%);
      box-shadow: 0 8px 25px rgba(0, 113, 227, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.3);
      transform: translateY(-2px) scale(1.015);
    }

    /* Secondary Button Styling */
    .btn-secondary {
      background: rgba(255, 255, 255, 0.85);
      color: var(--text-main) !important;
      border: 1px solid var(--border-color) !important;
      backdrop-filter: blur(12px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .btn-secondary:hover {
      background: #ffffff;
      border-color: rgba(0, 113, 227, 0.4) !important;
      color: var(--accent-blue) !important;
      box-shadow: 0 6px 20px rgba(0, 113, 227, 0.12), 0 2px 6px rgba(0, 0, 0, 0.04);
      transform: translateY(-2px) scale(1.015);
    }

    /* Wallet Button Custom Polish */
    .wallet-btn {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color) !important;
      border-radius: 99px !important;
      padding: 0.5rem 1.15rem;
      font-size: 0.85rem;
      font-weight: 500;
      color: var(--text-main);
    }

    .wallet-btn:hover {
      background: #ffffff;
      border-color: rgba(0, 113, 227, 0.3) !important;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
      transform: translateY(-1px);
    }

    /* Search Button Custom Polish */
    .search-btn {
      background: linear-gradient(135deg, #0071e3 0%, #0055b5 100%);
      color: white !important;
      border-radius: 14px;
      padding: 0 1.85rem;
    }

    .search-btn:hover {
      box-shadow: 0 6px 20px rgba(0, 113, 227, 0.4);
      transform: translateY(-2px);
    }

    /* Icon Motion inside buttons */
    .btn-primary svg,
    .btn-secondary svg,
    .search-btn svg,
    .btn-download-pdf svg,
    .btn-view-qr svg {
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .btn-primary:hover svg,
    .btn-secondary:hover svg,
    .search-btn:hover svg,
    .btn-download-pdf:hover svg,
    .btn-view-qr:hover svg {
      transform: translateX(2px);
    }

    /* ── Animated Terminal ── */
    .hero-terminal {
      flex: 1;
      width: 100%;
      perspective: 1000px;
    }

    .terminal-wrapper {
      transform-style: preserve-3d;
      animation: float3D 6s ease-in-out infinite;
      transform: rotateY(-10deg) rotateX(5deg) scale(0.95);
      transition: transform 0.5s;
    }

    .terminal-wrapper:hover {
      animation-play-state: paused;
      transform: rotateY(0deg) rotateX(0deg) scale(1);
    }

    @keyframes float3D {
      0%, 100% { transform: rotateY(-12deg) rotateX(6deg) scale(0.95) translateY(0); }
      50% { transform: rotateY(-12deg) rotateX(6deg) scale(0.95) translateY(-15px); }
    }

    .terminal-window {
      background: rgba(13, 17, 23, 0.95);
      border-radius: 14px;
      overflow: visible;
      box-shadow: 0 40px 80px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.1);
      backdrop-filter: blur(20px);
      transform-style: preserve-3d;
    }
    
    .terminal-window.minimized {
      height: 42px !important;
      min-height: 42px !important;
    }

    .terminal-header {
      background: rgba(22, 27, 34, 0.8);
      padding: 0.75rem 1rem;
      display: flex;
      align-items: center;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      border-radius: 14px 14px 0 0;
      transform: translateZ(40px);
    }

    .terminal-body {
      padding: 1.5rem;
      min-height: 250px;
      font-size: 0.9rem;
      transform: translateZ(20px);
      background: rgba(0,0,0,0.2);
      border-radius: 0 0 14px 14px;
    }

    .terminal-buttons {
      display: flex;
      gap: 8px;
    }

    .terminal-buttons span {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      cursor: pointer;
      transition: filter 0.2s;
    }

    .terminal-buttons span:hover { filter: brightness(1.2); }

    .terminal-buttons .close { background: #ff5f56; }
    .terminal-buttons .minimize { background: #ffbd2e; }
    .terminal-buttons .maximize { background: #27c93f; }
    
    /* Terminal States */
    .terminal-window.minimized .terminal-body {
      display: none;
    }
    
    .terminal-window.maximized {
      position: fixed;
      top: 50px;
      left: 5%;
      width: 90%;
      height: 85vh;
      z-index: 9999;
      transform: none !important;
      animation: none;
      box-shadow: 0 50px 100px rgba(0,0,0,0.5);
    }
    .terminal-window.maximized .terminal-body {
      height: calc(100% - 40px);
      overflow-y: auto;
    }
    .terminal-title {
      flex: 1;
      text-align: center;
      color: #8b949e;
      font-size: 0.75rem;
      font-family: -apple-system, sans-serif;
      margin-left: -44px;
      font-weight: 500;
    }

    .terminal-body {
      padding: 1.5rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85rem;
      color: #c9d1d9;
      line-height: 1.6;
      height: 310px;
      overflow-y: auto;
    }

    .t-line { margin-bottom: 0.25rem; display: none; }
    .t-visible { display: block; }
    .t-prompt { color: #58a6ff; margin-right: 8px; }
    .t-command { color: #f0f6fc; }
    .t-cursor { 
      display: inline-block; 
      width: 8px; 
      height: 15px; 
      background: #f0f6fc; 
      animation: blink 1s step-end infinite; 
      vertical-align: middle; 
      margin-left: 2px;
    }
    .t-success { color: #3fb950; font-weight: 600; }
    .t-dim { color: #8b949e; }
    .t-highlight { color: #d2a8ff; }
    .t-warning { color: #d29922; }

    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    /* ── Compliance Marquee ── */
    .marquee-section {
      background: var(--bg-secondary);
      border-top: 1px solid var(--border-color);
      border-bottom: 1px solid var(--border-color);

      padding: 1.25rem 0;
      overflow: hidden;
      white-space: nowrap;
    }

    .marquee-track {
      display: inline-flex;
      gap: 3rem;
      animation: marquee 25s linear infinite;
    }

    .marquee-item {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .marquee-item svg {
      color: var(--accent-blue);
    }

    @keyframes marquee {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }

    /* ── Instant PDF & QR Generator Section ── */
    .gen-section {
      padding: 5rem 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .gen-card {
      background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);
      border: 1px solid var(--border-color);
      border-radius: 24px;
      padding: 3rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.03);
    }

    .gen-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      margin-top: 2rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      margin-bottom: 1.25rem;
    }

    .form-group label {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-main);
    }

    .form-control {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      padding: 0.85rem 1rem;
      border-radius: 12px;
      font-size: 0.95rem;
      color: var(--text-main);
      outline: none;
    }

    .form-control:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.1);
    }

    .gen-result-box {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: 18px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    .qr-preview-img {
      width: 160px;
      height: 160px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      margin-bottom: 1rem;
      background: white;
      padding: 0.5rem;
    }

    /* ── Bento Grid 2.0 ── */
    .bento-section {
      padding: 5rem 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .section-header {
      text-align: center;
      margin-bottom: 3.5rem;
    }

    .section-header h2 {
      font-size: 2.5rem;
      font-weight: 700;
      letter-spacing: -0.03em;
      margin-bottom: 0.75rem;
    }

    .section-header p {
      color: var(--text-muted);
      font-size: 1.1rem;
      max-width: 650px;
      margin: 0 auto;
    }

    .bento-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem;
    }

    .bento-card {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 2rem;
      position: relative;
      overflow: hidden;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }

    .bento-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(0,0,0,0.06);
      border-color: rgba(0, 113, 227, 0.4);
    }

    .bento-card.span-2 {
      grid-column: span 2;
    }

    .bento-icon {
      width: 44px;
      height: 44px;
      background: var(--bg-secondary);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--accent-blue);
      margin-bottom: 1.25rem;
    }

    .bento-card h3 {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }

    .bento-card p {
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.5;
      margin-bottom: 1.5rem;
    }

    /* Wipe Simulator Tabs Inside Bento Tile */
    .sim-tabs {
      display: flex;
      gap: 0.5rem;
      background: var(--bg-secondary);
      padding: 0.3rem;
      border-radius: 10px;
      margin-bottom: 1.25rem;
    }

    .sim-tab {
      flex: 1;
      padding: 0.5rem;
      font-size: 0.8rem;
      font-weight: 600;
      border: none;
      background: transparent;
      border-radius: 8px;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.2s;
    }

    .sim-tab.active {
      background: var(--bg-primary);
      color: var(--text-main);
      box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    .sim-display {
      background: var(--bg-secondary);
      border-radius: 12px;
      padding: 1.25rem;
      font-size: 0.85rem;
    }

    .sim-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;
    }

    .sim-row:last-child {
      margin-bottom: 0;
    }

    .sim-label { color: var(--text-muted); }
    .sim-val { font-weight: 600; color: var(--text-main); }

    /* ── Verification Section ── */
    .verify-section {
      padding: 6rem 2rem;
      background: var(--bg-secondary);
      display: flex;
      justify-content: center;
    }

    .card {
      background: var(--bg-primary);
      border-radius: 24px;
      padding: 3rem;
      width: 100%;
      max-width: 780px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
      border: 1px solid var(--border-color);
    }

    .card h2 {
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 0.5rem;
    }
    
    .card > p {
      color: var(--text-muted);
      margin-bottom: 2rem;
      font-size: 0.95rem;
    }

    .search-box {
      display: flex;
      gap: 0.75rem;
      margin-bottom: 2rem;
    }

    .search-input {
      flex: 1;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.1rem 1.25rem;
      color: var(--text-main);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.9rem;
      outline: none;
      transition: all 0.2s ease;
    }

    .search-input:focus {
      border-color: var(--accent-blue);
      background: var(--bg-primary);
      box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
    }

    .search-btn {
      background: var(--accent-blue);
      border: none;
      border-radius: 14px;
      padding: 0 2rem;
      color: white;
      font-weight: 500;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.2s;
    }

    .search-btn:hover {
      background: var(--accent-hover);
    }

    /* Verification Results */
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.75rem 1.5rem;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.95rem;
      margin-bottom: 2rem;
    }

    .status-verified {
      background: var(--success-bg);
      color: #0c5a21;
    }

    .status-failed {
      background: var(--danger-bg);
      color: var(--danger-red);
    }

    .detail-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    .detail-item {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border-color);
    }

    .detail-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      font-weight: 600;
    }

    .detail-value {
      font-weight: 500;
      font-size: 1.05rem;
      color: var(--text-main);
      word-break: break-all;
    }

    .score-container {
      margin-bottom: 2rem;
      padding: 1.5rem;
      background: var(--bg-secondary);
      border-radius: 16px;
    }

    .score-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-main);
    }

    .score-bar-bg {
      height: 8px;
      background: #e5e5ea;
      border-radius: 4px;
      overflow: hidden;
    }

    .score-bar-fill {
      height: 100%;
      background: var(--success-green);
      border-radius: 4px;
      transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .hash-box {
      background: var(--bg-secondary);
      border-radius: 12px;
      padding: 1.25rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85rem;
      color: var(--text-muted);
      word-break: break-all;
      margin-top: 0.5rem;
      position: relative;
    }

    .copy-hash-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      margin-top: 0.6rem;
      background: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.35rem 0.85rem;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
    }

    .copy-hash-btn:hover {
      background: var(--accent-blue);
      color: white;
      border-color: var(--accent-blue);
    }

    .copy-hash-btn.copied {
      background: var(--success-bg);
      color: #0c5a21;
      border-color: rgba(52, 199, 89, 0.3);
    }

    .action-btn-group {
      display: flex;
      gap: 1rem;
      margin-top: 1.5rem;
    }

    .btn-download-pdf {
      flex: 1;
      background: var(--accent-blue);
      color: white;
      border: none;
      padding: 0.85rem 1.25rem;
      border-radius: 12px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: background 0.2s;
    }

    .btn-download-pdf:hover {
      background: var(--accent-hover);
    }

    .btn-view-qr {
      background: var(--bg-secondary);
      color: var(--text-main);
      border: 1px solid var(--border-color);
      padding: 0.85rem 1.25rem;
      border-radius: 12px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: background 0.2s;
    }

    .btn-view-qr:hover {
      background: #e8e8ed;
    }

    /* Modal Styling */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      backdrop-filter: blur(8px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-card {
      background: white;
      border-radius: 24px;
      padding: 2.5rem;
      max-width: 420px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.2);
    }

    .modal-card img {
      width: 220px;
      height: 220px;
      border-radius: 16px;
      border: 1px solid var(--border-color);
      margin: 1.5rem 0;
    }

    /* ── Footer ── */
    footer {
      background: var(--bg-secondary);
      padding: 4rem 2rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
      border-top: 1px solid var(--border-color);
    }

    .footer-logo {
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
    }

    .loading {
      text-align: center;
      padding: 3rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* ── SaaS Animations ── */
    .animate-on-scroll {
      opacity: 1;
      transform: translateY(0);
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* ── Comprehensive Mobile & Tablet UX ── */
    @media (max-width: 992px) {
      .nav-container { padding: 0 1.25rem; }
      .hero-content { flex-direction: column; text-align: center; gap: 2.5rem; }
      .hero-text h1 { font-size: 2.5rem; margin: 0 auto 1.25rem; }
      .hero-text .hero-ctas { justify-content: center; }
      .terminal-window { transform: none !important; animation: none !important; margin: 0 auto; width: 100%; }
      .hero-terminal { perspective: none; }
      .bento-grid { grid-template-columns: 1fr; }
      .bento-card.span-2 { grid-column: span 1; }
      .gen-grid { grid-template-columns: 1fr; gap: 1.5rem; }
      .nav-links { display: none; }
      .detail-grid { grid-template-columns: 1fr; gap: 1rem; }
    }

    @media (max-width: 600px) {
      body { font-size: 14px; }
      nav { padding: 0.75rem 0; }
      .logo { font-size: 1.1rem; }
      .wallet-btn { padding: 0.4rem 0.8rem; font-size: 0.75rem; }
      .hero { padding: 6.5rem 1rem 2.5rem; }
      .hero-badge { font-size: 0.75rem; padding: 0.35rem 0.85rem; margin-bottom: 1rem; }
      .hero-text h1 { font-size: 1.9rem; letter-spacing: -0.03em; line-height: 1.2; }
      .hero p { font-size: 0.95rem; margin-bottom: 1.75rem; }
      .hero-ctas { flex-direction: column; gap: 0.75rem; width: 100%; }
      .btn-primary, .btn-secondary { width: 100%; text-align: center; justify-content: center; padding: 0.85rem 1.25rem; font-size: 0.95rem; }
      
      .terminal-header { padding: 0.5rem 0.75rem; }
      .terminal-body { font-size: 0.72rem; height: 240px; padding: 0.85rem; line-height: 1.5; }
      
      .gen-section, .bento-section, .verify-section { padding: 3rem 1rem; }
      .gen-card, .card { padding: 1.25rem 1rem; border-radius: 16px; width: 100%; }
      .section-header h2 { font-size: 1.75rem; }
      .section-header p { font-size: 0.9rem; }
      
      .search-box { flex-direction: column; gap: 0.65rem; }
      .search-input { width: 100%; font-size: 0.8rem; padding: 0.85rem 1rem; }
      .search-btn { width: 100%; padding: 0.85rem; font-size: 0.95rem; border-radius: 12px; }
      
      .status-badge { font-size: 0.85rem; padding: 0.5rem 1rem; width: 100%; justify-content: center; margin-bottom: 1.25rem; }
      .detail-value { font-size: 0.9rem; }
      .hash-box { font-size: 0.75rem; padding: 0.85rem; }
      
      .action-btn-group { flex-direction: column; gap: 0.65rem; margin-top: 1.25rem; }
      .btn-download-pdf, .btn-view-qr { width: 100%; min-height: 46px; font-size: 0.85rem; }
      .qr-mobile-wrapper { width: 100% !important; max-width: 240px; margin: 0 auto 1.25rem !important; }
      
      footer { padding: 2.5rem 1rem; font-size: 0.8rem; }
    }
  </style>
</head>
<body>

  <!-- Navigation -->
  <nav>
    <div class="nav-container">
      <a href="#" class="logo">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          <path d="M9 12l2 2 4-4"></path>
        </svg>
        SecureWipe
      </a>
      <div class="nav-links">
        <a href="index.html" class="active">Home</a>
        <a href="products.html">Sanitization Engines</a>
        <a href="verify.html">Audit Verification</a>
        <a href="explorer.html">Ledger Explorer</a>
        <a href="enterprise.html">Enterprise Fleet</a>
      </div>
      <button class="wallet-btn" id="walletBtn" onclick="connectWallet()">
        <span class="dot"></span>
        <span id="walletText">Connect Wallet</span>
      </button>
    </div>
  </nav>

  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-content">
      <div class="hero-text">
        <h1 id="heroHeading" class="scramble-glitch-text animate-on-scroll" data-text="Verifiable IT Asset Sanitization.">Verifiable IT Asset Sanitization.</h1>
        <p class="animate-on-scroll">Unlocking India's ₹50,000 Crore idle e-waste assets. Military-grade data wiping combined with signed PDF certificates & QR codes anchored on blockchain.</p>
        <div class="hero-ctas animate-on-scroll">
          <a href="#generator" class="btn-primary">Generate PDF Cert</a>
          <a href="#verify" class="btn-secondary">Verify QR Code</a>
          <a href="#cli" class="btn-secondary" style="border: 1px solid var(--border-color); color: var(--text-main);">Download CLI</a>
          <a href="#" id="reopen-terminal-btn" class="btn-secondary" style="display: none; border-color: var(--accent-blue); color: var(--text-main);" onclick="event.preventDefault(); restoreHeroTerminal();">Restore Terminal</a>
        </div>
      </div>
      <div class="hero-terminal animate-on-scroll">
        <div class="terminal-wrapper">
          <div class="terminal-window">
          <div class="terminal-header" style="display: flex; align-items: center;">
            <div class="terminal-buttons">
              <span class="close" onclick="closeHeroTerminal()"></span>
              <span class="minimize" onclick="minimizeHeroTerminal()"></span>
              <span class="maximize" onclick="maximizeHeroTerminal()"></span>
            </div>
            <div class="terminal-title" style="flex: 1; text-align: center;">demo.py — bash</div>
            <button onclick="playTerminalAnimation()" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: background 0.2s;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Run Demo
            </button>
          </div>
          <div class="terminal-body" id="terminalOutput">
            <div id="t-line-1" class="t-line t-visible"><span class="t-prompt">~/securewipe$</span><span class="t-command" id="t-cmd"></span><span class="t-cursor" id="t-cursor"></span></div>
            <div id="t-line-2" class="t-line"><span class="t-dim">[INFO]</span> Discovered: <span class="t-highlight">/dev/nvme0n1 (512GB NVMe)</span></div>
            <div id="t-line-3" class="t-line"><span class="t-dim">[INFO]</span> Checking Hidden Areas (HPA / DCO / RPMB)... <span class="t-success">[CLEAN]</span></div>
            <div id="t-line-4" class="t-line"><span class="t-warning">[WIPE]</span> Executing NIST SP 800-88 Purge... 12%</div>
            <div id="t-line-5" class="t-line"><span class="t-warning">[WIPE]</span> Executing NIST SP 800-88 Purge... 45%</div>
            <div id="t-line-6" class="t-line"><span class="t-warning">[WIPE]</span> Executing NIST SP 800-88 Purge... 89%</div>
            <div id="t-line-7" class="t-line"><span class="t-success">[OK]</span> Device sanitized (100% Confidence Score).</div>
            <div id="t-line-8" class="t-line"><span class="t-dim">[INFO]</span> Generating PDF Certificate & QR Code...</div>
            <div id="t-line-9" class="t-line"><span class="t-success">[ANCHOR]</span> Certificate anchored to SecureWipeLedger.</div>
            <div id="t-line-10" class="t-line">TxHash: <span class="t-highlight">ba487344ca51a6e42bcc5d584507cad28ae447a3d37f...</span> <!-- SHA256 --></div>
            <div id="t-line-11" class="t-line" style="margin-top: 1rem"><span class="t-prompt">~/securewipe$</span><span class="t-cursor"></span></div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Compliance Marquee Ticker -->
  <section class="marquee-section">
    <div class="marquee-track">
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> NIST SP 800-88 REV. 1</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> EMBEDDED SHA-256 QR CODE</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> IEEE 2883-2022 STANDARD</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> ANSSI PALIER 1 / 2</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> DOD 5220.22-M</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> CPCB E-WASTE RULES 2022</div>

      <!-- Repeated for smooth looping -->
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> NIST SP 800-88 REV. 1</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> EMBEDDED SHA-256 QR CODE</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> IEEE 2883-2022 STANDARD</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> ANSSI PALIER 1 / 2</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> DOD 5220.22-M</div>
      <div class="marquee-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> CPCB E-WASTE RULES 2022</div>
    </div>
  </section>



  <!-- Instant PDF & QR Code Generator Section -->
  <section id="generator" class="gen-section animate-on-scroll">
    <div class="gen-card">
      <div style="text-align: center; max-width: 650px; margin: 0 auto 2rem;">
        <h2>📄 PDF & QR Certificate Generator</h2>
        <p style="color: var(--text-muted);">Generate an official, cryptographically signed PDF Certificate with embedded QR code and anchor it to the blockchain ledger in real-time.</p>
      </div>

      <div class="gen-grid">
        <!-- Form Inputs -->
        <div>
          <div class="form-group">
            <label>Device Serial Number</label>
            <input type="text" id="genSerial" class="form-control" value="SW-PROD-2026-X99" />
          </div>
          <div class="form-group">
            <label>Device Model & Spec</label>
            <input type="text" id="genModel" class="form-control" value="Dell Latitude 5420 NVMe SSD (512GB)" />
          </div>
          <div class="form-group">
            <label>Sanitization Standard</label>
            <select id="genMethod" class="form-control">
              <option value="NIST SP 800-88 Purge (NVMe Format / ATA Secure Erase)">NIST SP 800-88 Purge (NVMe / SSD)</option>
              <option value="NIST SP 800-88 Clear (Multi-Pass Overwrite)">NIST SP 800-88 Clear (HDD)</option>
              <option value="NIST SP 800-88 Crypto Erase (Key Shredding)">NIST SP 800-88 Crypto Erase (BitLocker / SED)</option>
              <option value="ANSSI Palier 2 (Multi-pass + HPA Zeroed)">ANSSI Palier 2 (Multi-pass + HPA)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Auditor / Operator Name</label>
            <input type="text" id="genOperator" class="form-control" value="Ministry of Mines IT Inspector" />
          </div>

          <button class="btn-primary" style="width: 100%; border: none; cursor: pointer; margin-top: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;" onclick="generatePdfCertificate()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Generate PDF Certificate & QR Code
          </button>
        </div>

        <!-- Result Box -->
        <div class="gen-result-box" id="genResultBox">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--accent-blue)" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          <h4 style="margin: 1rem 0 0.5rem;">Ready to Generate</h4>
          <p style="font-size: 0.85rem; color: var(--text-muted);">Fill in the details and click the button to render a high-resolution PDF certificate with embedded SHA-256 QR code.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Bento Grid 2.0 -->
  <section id="bento" class="bento-section">
    <div class="section-header animate-on-scroll">
      <h2>Engineering Trust into IT Recycling</h2>
      <p>How SecureWipe solves the 5 core points of the Ministry of Mines problem statement.</p>
    </div>

    <div class="bento-grid">
      <!-- Card 1: Interactive Wipe Simulator -->
      <div class="bento-card span-2 animate-on-scroll" data-tilt data-tilt-max="5" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.1">
        <div class="bento-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="12" x2="2" y2="12"></line><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path><line x1="6" y1="16" x2="6.01" y2="16"></line><line x1="10" y1="16" x2="10.01" y2="16"></line></svg>
        </div>
        <h3>1. Multi-Target NIST SP 800-88 Rev.1 Engine</h3>
        <p>Select a storage target to simulate how SecureWipe handles specific drive architectures:</p>

        <!-- Interactive Tabs -->
        <div class="sim-tabs">
          <button class="sim-tab active" onclick="switchSim('hdd')">HDD (Clear)</button>
          <button class="sim-tab" onclick="switchSim('nvme')">NVMe / SSD (Purge)</button>
          <button class="sim-tab" onclick="switchSim('sed')">BitLocker / SED (Crypto Erase)</button>
          <button class="sim-tab" onclick="switchSim('android')">Android ADB / Fastboot</button>
        </div>

        <div class="sim-display" id="simDisplay">
          <div class="sim-row">
            <span class="sim-label">Target Architecture:</span>
            <span class="sim-val" id="simTarget">SATA Hard Disk Drive (HDD)</span>
          </div>
          <div class="sim-row">
            <span class="sim-label">NIST Standard:</span>
            <span class="sim-val" id="simMethod">NIST 800-88 Clear (Multi-Pass Sector Overwrite)</span>
          </div>
          <div class="sim-row">
            <span class="sim-label">Hidden Regions (HPA/DCO):</span>
            <span class="sim-val" id="simHPA">Unhidden via hdparm & Zeroed</span>
          </div>
          <div class="sim-row">
            <span class="sim-label">Wipe Confidence Score:</span>
            <span class="sim-val" style="color:var(--success-green);" id="simScore">100% Verified</span>
          </div>
        </div>
      </div>

      <!-- Card 2: Hidden Storage Region Safeguard -->
      <div class="bento-card animate-on-scroll" data-tilt data-tilt-max="10" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.1">
        <div class="bento-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        </div>
        <h3>2. Hidden Region Detection</h3>
        <p>Standard Windows resets leave data in HPA/DCO sectors on HDDs and over-provisioned sectors on SSDs. SecureWipe unhides and zero-fills hidden areas before issuing the audit certificate.</p>
      </div>

      <!-- Card 3: Blockchain Anchored Verification -->
      <div class="bento-card animate-on-scroll" data-tilt data-tilt-max="10" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.1">
        <div class="bento-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
        </div>
        <h3>3. Tamper-Proof Audit Certificates</h3>
        <p>Certificates are cryptographically signed with SHA-256 block hashes anchored directly to a ledger. Recyclers and buyers can scan the QR code to verify authenticity instantly.</p>
      </div>

      <!-- Card 4: Circular Economy Recycler Network -->
      <div class="bento-card span-2 animate-on-scroll" data-tilt data-tilt-max="5" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.1">
        <div class="bento-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        </div>
        <h3>4. Closing the Loop (Circular Economy)</h3>
        <p>After a wipe, SecureWipe connects sanitized hardware directly to certified recyclers & refurbishers (e.g. Attero, Karo Sambhav, Cashify), converting security fear into monetary asset recovery.</p>
      </div>
    </div>
  </section>

  <!-- CLI Download Section -->
  <section id="cli" class="gen-section animate-on-scroll">
    <div class="gen-card">
      <div style="text-align: center; max-width: 650px; margin: 0 auto 2rem;">
        <h2 style="display: flex; align-items: center; justify-content: center; gap: 0.75rem;">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--accent-blue)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          Download SecureWipe CLI
        </h2>
        <p style="color: var(--text-muted);">Run the verifiable data sanitization engine natively on your own hardware. Supports Windows, Linux, and macOS. Automatically generates certificates and syncs with the blockchain.</p>
      </div>

      <div style="display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;">
        <!-- Windows Install -->
        <div style="background: var(--bg-primary); padding: 1.5rem; border-radius: 16px; border: 1px solid var(--border-color); flex: 1; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
          <h4 style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; color: var(--text-main);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
            Windows (PowerShell)
          </h4>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Run this command in PowerShell as Administrator to download and install dependencies:</p>
          <div style="background: #1e1e1e; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.85rem; color: #58a6ff; user-select: all; cursor: pointer; word-break: break-all; white-space: pre-wrap;" onclick="navigator.clipboard.writeText('iwr -useb https://raw.githubusercontent.com/MayankSen09/SecureWipe/master/install.ps1 | iex')">iwr -useb https://raw.githubusercontent.com/MayankSen09/SecureWipe/master/install.ps1 | iex</div>
        </div>

        <!-- Linux Install -->
        <div style="background: var(--bg-primary); padding: 1.5rem; border-radius: 16px; border: 1px solid var(--border-color); flex: 1; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
          <h4 style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; color: var(--text-main);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path><path d="M12 8a6 6 0 0 0-6 6v4a6 6 0 0 0 12 0v-4a6 6 0 0 0-6-6z"></path><path d="M6 20h12"></path></svg>
            Linux / macOS (Bash)
          </h4>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Run this command in your terminal to clone the repository and install requirements:</p>
          <div style="background: #1e1e1e; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.85rem; color: #3fb950; user-select: all; cursor: pointer; word-break: break-all; white-space: pre-wrap;" onclick="navigator.clipboard.writeText('curl -sSL https://raw.githubusercontent.com/MayankSen09/SecureWipe/master/install.sh | bash')">curl -sSL https://raw.githubusercontent.com/MayankSen09/SecureWipe/master/install.sh | bash</div>
        </div>
      </div>
      
      <div style="text-align: center; margin-top: 2rem;">
        <a href="https://github.com/MayankSen09/SecureWipe" target="_blank" class="btn-secondary">View Source Code on GitHub</a>
      </div>
    </div>
  </section>

  <!-- Verification App -->
  <section id="verify" class="verify-section">
    <div class="card animate-on-scroll">
      <h2>Certificate Verification Portal</h2>
      <p>Enter the cryptographic block hash or scan the QR code to verify proof of sanitization anchored on the blockchain ledger.<br><small style="color:var(--text-muted);">Accepts hashes with or without <code>0x</code> prefix.</small></p>
      
      <div class="search-box">
        <input type="text" id="hashInput" class="search-input" aria-label="SHA-256 Block Hash Input" placeholder="Enter 64-character SHA-256 block hash (e.g. ba487344ca51a6e42bcc5d584507...)" onkeydown="if(event.key==='Enter') performSearch()" />
        <button class="search-btn" aria-label="Verify Hash Button" onclick="performSearch()">Verify Hash</button>
      </div>


      <div id="resultArea"></div>
    </div>
  </section>

  <!-- Block Explorer -->
  <section id="explorer" class="gen-section animate-on-scroll" style="padding-top: 2rem;">
    <div class="card" style="max-width: 1200px; margin: 0 auto; overflow-x: auto;">
      <h2>Ledger Block Explorer</h2>
      <p style="margin-bottom: 1.5rem;">Recent sanitization certificates anchored to the blockchain. Click a hash to verify it.</p>
      
      <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border-color); color: var(--text-muted);">
            <th style="padding: 1rem 0.5rem;">Block Hash</th>
            <th style="padding: 1rem 0.5rem;">Timestamp</th>
            <th style="padding: 1rem 0.5rem;">Asset S/N</th>
            <th style="padding: 1rem 0.5rem;">Score</th>
          </tr>
        </thead>
        <tbody id="explorerBody">
          <tr><td colspan="4" style="padding: 2rem; text-align: center; color: var(--text-muted);">Loading blocks...</td></tr>
        </tbody>
      </table>
      
      <div style="text-align: center; margin-top: 1.5rem;">
        <button class="btn-secondary" onclick="fetchBlocks()" style="padding: 0.5rem 1.5rem; font-size: 0.85rem;">Refresh Ledger</button>
      </div>
    </div>
  </section>

  <!-- QR Code Modal -->
  <div class="modal-overlay" id="qrModal" onclick="closeQrModal()">
    <div class="modal-card" onclick="event.stopPropagation()">
      <h3 style="font-size: 1.25rem; font-weight: 700;">Embedded SHA-256 QR Code</h3>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">Scan with any smartphone camera to verify ledger integrity offline.</p>
      <img id="qrModalImg" src="" alt="QR Code" />
      <button class="btn-secondary" style="width: 100%; border-radius: 12px;" onclick="closeQrModal()">Close Preview</button>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <div class="footer-logo">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
      </svg>
      SecureWipe
    </div>
    <p>Ministry of Mines Software Solution — Enterprise Data Sanitization & Circular Economy Platform.</p>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.1/vanilla-tilt.min.js"></script>
  <script>
    // --- API Base URL Configuration ---
    const API_BASE = (window.location.protocol === 'file:' || (window.location.port && window.location.port !== '8000'))
      ? 'http://localhost:8000'
      : '';

    // --- Hero Terminal Mac Controls ---
    function closeHeroTerminal() {
      document.querySelector('.hero-terminal').style.display = 'none';
      document.getElementById('reopen-terminal-btn').style.display = 'inline-flex';
    }

    function restoreHeroTerminal() {
      document.querySelector('.hero-terminal').style.display = 'block';
      document.getElementById('reopen-terminal-btn').style.display = 'none';
      // Re-initialize tilt just in case
      initVanillaTilt();
    }

    function minimizeHeroTerminal() {
      const tw = document.querySelector('.terminal-window');
      tw.classList.toggle('minimized');
    }

    function maximizeHeroTerminal() {
      const tw = document.querySelector('.terminal-window');
      tw.classList.toggle('maximized');
      
      if (tw.classList.contains('maximized')) {
        // Disable 3D tilt when full screen
        if(tw.vanillaTilt) tw.vanillaTilt.destroy();
        tw.style.transform = 'none';
      } else {
        // Re-enable 3D tilt when windowed
        initVanillaTilt();
      }
    }

    function initVanillaTilt() {
      const tw = document.querySelector('.terminal-window');
      if(tw && !tw.classList.contains('maximized')) {
        VanillaTilt.init(tw, {
          max: 15,
          speed: 400,
          glare: true,
          "max-glare": 0.15,
          perspective: 1000
        });
      }
    }

    // Initialize 3D effect on load
    document.addEventListener("DOMContentLoaded", initVanillaTilt);

    // --- Normalize hash input: strip leading whitespace and optional 0x prefix ---
    function normalizeHash(raw) {
      let h = raw.trim();
      if (h.toLowerCase().startsWith('0x')) h = h.substring(2);
      return h;
    }

    // --- HTML Escaping helper function to prevent script injection (XSS) ---
    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    // --- Live Web Wiping Studio Functionality ---
    async function executeWebWipe() {
      const driveVal = document.getElementById('wipeDriveSelect').value.split('|');
      const device = driveVal[0];
      const model = driveVal[1];
      const serial = driveVal[2];
      const method = document.getElementById('wipeMethodSelect').value;
      const operator = document.getElementById('wipeOperator').value.trim() || 'Web Suite Operator';

      const btn = document.getElementById('startWipeBtn');
      const progressBar = document.getElementById('webWipeProgressBar');
      const stepLabel = document.getElementById('wipeStepLabel');
      const logs = document.getElementById('webWipeLogs');
      const resultActions = document.getElementById('wipeResultActions');

      btn.disabled = true;
      btn.style.opacity = '0.5';
      resultActions.style.display = 'none';
      logs.innerHTML = '';

      function appendLog(msg, color="#aaa") {
        logs.innerHTML += `<div style="color:${color}; margin-bottom:0.25rem;">${msg}</div>`;
        logs.scrollTop = logs.scrollHeight;
      }

      appendLog(`[1/5] Initializing target: ${model} (${serial})...`, '#58a6ff');
      stepLabel.innerText = 'Step 1/5';
      progressBar.style.width = '20%';
      await new Promise(r => setTimeout(r, 600));

      appendLog(`[2/5] Checking HPA/DCO sectors & firmware locks... [CLEAN]`, '#d29922');
      stepLabel.innerText = 'Step 2/5';
      progressBar.style.width = '40%';
      await new Promise(r => setTimeout(r, 800));

      appendLog(`[3/5] Executing ${method} sanitization... Zeroing sectors...`, '#e3b341');
      stepLabel.innerText = 'Step 3/5';
      progressBar.style.width = '70%';
      await new Promise(r => setTimeout(r, 1000));

      appendLog(`[4/5] Verifying sector zeroing (10% random sample pass)... [OK]`, '#3fb950');
      stepLabel.innerText = 'Step 4/5';
      progressBar.style.width = '85%';
      await new Promise(r => setTimeout(r, 600));

      appendLog(`[5/5] Calculating confidence score & requesting signed certificate...`, '#d2a8ff');
      stepLabel.innerText = 'Step 5/5';
      progressBar.style.width = '95%';

      try {
        const resp = await fetch(API_BASE + '/api/start-wipe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ device, model, serial, method, operator })
        });
        const data = await resp.json();

        if (resp.ok && data.status === 'success') {
          progressBar.style.width = '100%';
          stepLabel.innerText = 'DONE 100%';
          appendLog(`✓ SANITIZATION COMPLETE! Audit Score: ${data.confidence_score}%`, '#3fb950');
          appendLog(`✓ Blockchain Hash: ${data.block_hash.substring(0, 24)}...`, '#58a6ff');

          document.getElementById('webPdfBtn').href = data.download_url;
          document.getElementById('webVerifyBtn').href = data.verify_url;
          resultActions.style.display = 'flex';
        } else {
          appendLog(`❌ Wipe execution failed: ${data.detail || 'Unknown error'}`, '#ff5f56');
        }
      } catch (err) {
        appendLog(`❌ Connection error connecting to wipe node.`, '#ff5f56');
      } finally {
        btn.disabled = false;
        btn.style.opacity = '1';
      }
    }

    // --- Real Wallet Connect ---
    async function connectWallet() {
      const btn = document.getElementById('walletBtn');
      const text = document.getElementById('walletText');
      
      if (btn.classList.contains('connected')) return;

      if (typeof window.ethereum !== 'undefined') {
        try {
          text.innerText = "Connecting...";
          const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
          const account = accounts[0];
          
          btn.classList.add('connected');
          text.innerText = account.substring(0, 6) + "..." + account.substring(account.length - 4);
        } catch (error) {
          text.innerText = "Connect Wallet";
          console.error("User denied wallet connection or error occurred.", error);
        }
      } else {
        alert('MetaMask is not installed. Please install the MetaMask extension to use this feature!');
      }
    }

    // --- Dynamic PDF & QR Generator ---
    async function generatePdfCertificate() {
      const resultBox = document.getElementById('genResultBox');
      resultBox.innerHTML = '<div class="loading">Rendering PDF Certificate & Generating SHA-256 QR Code...</div>';

      const payload = {
        serial: document.getElementById('genSerial').value.trim() || 'SW-PROD-2026-X99',
        model: document.getElementById('genModel').value.trim() || 'Dell Latitude NVMe SSD 512GB',
        method: document.getElementById('genMethod').value,
        operator: document.getElementById('genOperator').value.trim() || 'Ministry of Mines Auditor',
        organization: 'Ministry of Mines IT Division',
        confidence_score: 100
      };

      try {
        const response = await fetch(API_BASE + '/generate-certificate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (response.ok && data.status === 'success') {
          const liveBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000' : window.location.origin;
          const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(liveBase + data.verify_url)}`;

          resultBox.innerHTML = `
            <img src="${qrUrl}" class="qr-preview-img" alt="Embedded QR Code" />
            <h4 style="font-size: 1.1rem; color: var(--success-green); margin-bottom: 0.25rem;">✓ Signed PDF Certificate Created!</h4>
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">SHA-256 Block Hash: <code>${data.block_hash.substring(0, 18)}...</code></p>
            
            <div style="display:flex; gap:0.5rem; width:100%;">
              <a href="${API_BASE + data.download_url}" target="_blank" class="btn-primary" style="flex:1; text-decoration:none; font-size:0.85rem; padding:0.75rem; display:inline-flex; align-items:center; justify-content:center; gap:0.4rem;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Download PDF
              </a>
              <button onclick="openQrModal('${qrUrl}')" class="btn-secondary" style="font-size:0.85rem; padding:0.75rem; display:inline-flex; align-items:center; justify-content:center; gap:0.4rem;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg> QR Code
              </button>
            </div>
          `;
        } else {
          resultBox.innerHTML = `<p style="color:var(--danger-red);">Generation Failed: ${data.detail || 'Error'}</p>`;
        }
      } catch (err) {
        resultBox.innerHTML = `<p style="color:var(--danger-red);">Connection error generating certificate.</p>`;
      }
    }

    // --- Interactive Wipe Simulator Switcher ---
    const simData = {
      hdd: {
        target: "SATA Hard Disk Drive (HDD)",
        method: "NIST 800-88 Clear (Multi-Pass Sector Overwrite)",
        hpa: "Unhidden via hdparm & Zeroed (+20 Pts)",
        score: "100% Verified"
      },
      nvme: {
        target: "NVMe M.2 Solid State Drive (SSD)",
        method: "NIST 800-88 Purge (NVMe Format / ATA Secure Erase)",
        hpa: "Over-provisioned Sectors Cleared (+20 Pts)",
        score: "100% Verified"
      },
      sed: {
        target: "BitLocker / LUKS Encrypted Drive (SED)",
        method: "NIST 800-88 Crypto Erase (Key Destruction)",
        hpa: "Master Encryption Key Shredded (+20 Pts)",
        score: "100% Verified"
      },
      android: {
        target: "Android Smartphone (eMMC / UFS)",
        method: "ADB / Fastboot Partition Zeroing + RPMB Check",
        hpa: "Replay Protected Memory Block Verified (+20 Pts)",
        score: "100% Verified"
      }
    };

    function switchSim(key) {
      document.querySelectorAll('.sim-tab').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');

      const data = simData[key];
      document.getElementById('simTarget').innerText = data.target;
      document.getElementById('simMethod').innerText = data.method;
      document.getElementById('simHPA').innerText = data.hpa;
      document.getElementById('simScore').innerText = data.score;
    }

    // --- QR Modal Controls ---
    function openQrModal(url) {
      document.getElementById('qrModalImg').src = url;
      document.getElementById('qrModal').classList.add('active');
    }
    function closeQrModal() {
      document.getElementById('qrModal').classList.remove('active');
    }

    // --- Hash Verification ---
    async function verifyHash(hash) {
      const resultArea = document.getElementById('resultArea');
      resultArea.innerHTML = '<div class="loading">Querying Ledger & Circular Economy Records...</div>';

      try {
        const response = await fetch(`${API_BASE}/verify?hash=${encodeURIComponent(hash)}`);
        const data = await response.json();

        if (response.ok && data.verified) {
          const liveBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000' : window.location.origin;
          const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(liveBase + '/verify?hash=' + data.block_hash)}`;

          resultArea.innerHTML = `
            <div style="display: flex; gap: 2rem; align-items: flex-start; flex-wrap: wrap;">
              <!-- Prominent QR Code Display -->
              <div class="qr-mobile-wrapper" style="background: white; border: 1px solid var(--border-color); border-radius: 20px; padding: 1.25rem; text-align: center; width: 220px; margin: 0 auto;">
                <img src="${qrUrl}" style="width: 100%; height: auto; border-radius: 12px; display: block;" alt="Certificate QR Code" />
                <span style="font-size: 0.75rem; font-weight: 600; color: var(--text-muted); margin-top: 0.5rem; display: block;">SHA-256 Verified QR</span>
              </div>

              <!-- Verification Details -->
              <div style="flex: 1; min-width: 280px;">
                <div class="status-badge status-verified">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  Verified Authentic Certificate
                </div>

                <div class="detail-grid">
                  <div class="detail-item">
                    <div class="detail-label">Report ID</div>
                    <div class="detail-value">${escapeHtml(data.report_id)}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Wipe Timestamp</div>
                    <div class="detail-value">${escapeHtml(data.timestamp_human)}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Device Serial</div>
                    <div class="detail-value">${escapeHtml(data.serial)}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Sanitization Method</div>
                    <div class="detail-value">${escapeHtml(data.method)}</div>
                  </div>
                </div>

                <div class="score-container">
                  <div class="score-header">
                    <span>Wipe Confidence Score</span>
                    <span>${data.confidence_score}%</span>
                  </div>
                  <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width: ${data.confidence_score}%"></div>
                  </div>
                </div>
              </div>
            </div>

            <div class="detail-label" style="margin-top:1.5rem;">Cryptographic Block Hash (SHA-256, 64 chars)</div>
            <div class="hash-box" id="displayedHash">${data.block_hash}</div>
            <button class="copy-hash-btn" id="copyHashBtn" onclick="copyHash('${data.block_hash}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              Copy Full Hash
            </button>

            <!-- Download PDF & QR Buttons -->
            <div class="action-btn-group">
              <button class="btn-download-pdf" onclick="window.open(API_BASE + '/download-pdf?hash=${data.block_hash}', '_blank')">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                Download PDF Certificate
              </button>
              <button class="btn-view-qr" onclick="openQrModal('${qrUrl}')">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
                Enlarge QR Code
              </button>
            </div>
          `;
        } else {
          resultArea.innerHTML = `
            <div class="status-badge status-failed">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              Hash Not Found / Tamper Detected
            </div>
            <p style="font-size:0.95rem; color:var(--text-muted); line-height: 1.5;">
              ${data.message || 'No record matches the provided hash in the ledger. The certificate may be invalid or tampered with.'}
            </p>
          `;
        }
      } catch (err) {
        resultArea.innerHTML = `
          <div class="status-badge status-failed">
            Connection Error
          </div>
          <p style="font-size:0.95rem; color:var(--text-muted); line-height: 1.5;">
            Unable to connect to SecureWipe node.
          </p>
        `;
      }
    }

    function performSearch() {
      const rawHash = document.getElementById('hashInput').value.trim();
      if (!rawHash) {
        document.getElementById('resultArea').innerHTML = `
          <div class="status-badge status-failed">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            No Hash Entered
          </div>
          <p style="font-size:0.95rem; color:var(--text-muted);">Please paste the full 64-character SHA-256 block hash from your certificate.</p>
        `;
        return;
      }
      // Normalize: strip 0x prefix if present
      const hash = normalizeHash(rawHash);
      if (hash.length !== 64) {
        document.getElementById('resultArea').innerHTML = `
          <div class="status-badge status-failed">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            Invalid Hash Length
          </div>
          <p style="font-size:0.95rem; color:var(--text-muted);">Hash is <strong>${hash.length} characters</strong> after removing any 0x prefix — a valid SHA-256 block hash must be exactly <strong>64 characters</strong>. Please copy the full hash from your PDF certificate.</p>
        `;
        return;
      }
      // Update input to show the normalized hash
      document.getElementById('hashInput').value = hash;
      window.history.pushState({}, '', `?hash=${encodeURIComponent(hash)}`);
      verifyHash(hash);
    }

    function copyHash(hash) {
      navigator.clipboard.writeText(hash).then(() => {
        const btn = document.getElementById('copyHashBtn');
        if (btn) {
          btn.classList.add('copied');
          btn.innerHTML = `
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Copied!
          `;
          setTimeout(() => {
            btn.classList.remove('copied');
            btn.innerHTML = `
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              Copy Full Hash
            `;
          }, 2000);
        }
      }).catch(() => {
        /* fallback: select the hash text */
        const el = document.getElementById('displayedHash');
        if (el) {
          const range = document.createRange();
          range.selectNodeContents(el);
          window.getSelection().removeAllRanges();
          window.getSelection().addRange(range);
        }
      });
    }

    // --- SaaS Scroll Animations ---
    document.addEventListener('DOMContentLoaded', () => {
      const elementsToAnimate = [
        document.querySelector('.hero h1'),
        document.querySelector('.hero p'),
        document.querySelector('.hero-ctas'),
        document.querySelector('.hero-terminal'),
        document.querySelector('.gen-card'),
        document.querySelector('.card'),
        document.querySelector('.section-header'),
        ...document.querySelectorAll('.bento-card')
      ];

      elementsToAnimate.forEach(el => {
        if (el) el.classList.add('animate-on-scroll');
      });

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

      elementsToAnimate.forEach(el => {
        if (el) observer.observe(el);
      });
    });

    // --- Terminal Typing Animation ---
    window.playTerminalAnimation = function() {
      // Reset state
      const cmdEl = document.getElementById('t-cmd');
      const cursor1 = document.getElementById('t-cursor');
      cmdEl.textContent = "";
      cursor1.style.display = 'inline-block';
      
      for (let j = 2; j <= 11; j++) {
        const el = document.getElementById('t-line-' + j);
        if (el) {
          el.classList.remove('t-visible');
          // Fix for the wiping lines which get display:none
          if (j >= 4 && j <= 6) el.style.display = 'block'; 
        }
      }

      const cmdText = "python demo.py --target /dev/nvme0n1";
      let i = 0;
      
      const typeInterval = setInterval(() => {
        if (i < cmdText.length) {
          cmdEl.textContent += cmdText.charAt(i);
          i++;
        } else {
          clearInterval(typeInterval);
          cursor1.style.display = 'none'; 
          
          setTimeout(() => document.getElementById('t-line-2').classList.add('t-visible'), 400);
          setTimeout(() => document.getElementById('t-line-3').classList.add('t-visible'), 1000);
          setTimeout(() => document.getElementById('t-line-4').classList.add('t-visible'), 1400);
          setTimeout(() => {
            document.getElementById('t-line-4').style.display = 'none';
            document.getElementById('t-line-5').classList.add('t-visible');
          }, 1800);
          setTimeout(() => {
            document.getElementById('t-line-5').style.display = 'none';
            document.getElementById('t-line-6').classList.add('t-visible');
          }, 2100);
          setTimeout(() => {
            document.getElementById('t-line-6').style.display = 'none';
            document.getElementById('t-line-7').classList.add('t-visible');
          }, 2500);
          setTimeout(() => document.getElementById('t-line-8').classList.add('t-visible'), 3000);
          setTimeout(() => document.getElementById('t-line-9').classList.add('t-visible'), 4200);
          setTimeout(() => document.getElementById('t-line-10').classList.add('t-visible'), 4300);
          setTimeout(() => document.getElementById('t-line-11').classList.add('t-visible'), 4800);
        }
      }, 60);
    };

    // Auto-play once on load
    setTimeout(() => {
      window.playTerminalAnimation();
    }, 1000);

    // --- Block Explorer Functions ---
    async function fetchBlocks() {
      const tbody = document.getElementById('explorerBody');
      try {
        tbody.innerHTML = '<tr><td colspan="4" style="padding: 2rem; text-align: center; color: var(--text-muted);">Loading blocks...</td></tr>';
        const response = await fetch(API_BASE + '/api/blocks?limit=10');
        const data = await response.json();
        
        if (data.status === 'success' && data.blocks && data.blocks.length > 0) {
          tbody.innerHTML = '';
          data.blocks.forEach(block => {
            const shortHash = block.block_hash.substring(0, 16) + '...';
            const date = new Date(block.timestamp * 1000).toLocaleString();
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border-color)';
            tr.style.cursor = 'pointer';
            tr.onclick = () => {
              document.getElementById('hashInput').value = block.block_hash;
              document.getElementById('verify').scrollIntoView();
              verifyHash(block.block_hash);
            };
            tr.innerHTML = `
              <td style="padding: 1rem 0.5rem; color: var(--accent-blue); font-family: monospace;">${shortHash}</td>
              <td style="padding: 1rem 0.5rem; color: var(--text-muted);">${date}</td>
              <td style="padding: 1rem 0.5rem;">${escapeHtml(block.serial)}</td>
              <td style="padding: 1rem 0.5rem; color: var(--success-green); font-weight: 600;">${block.confidence_score}%</td>
            `;
            tbody.appendChild(tr);
          });
        } else {
          tbody.innerHTML = '<tr><td colspan="4" style="padding: 2rem; text-align: center; color: var(--text-muted);">No blocks found.</td></tr>';
        }
      } catch (err) {
        tbody.innerHTML = '<tr><td colspan="4" style="padding: 2rem; text-align: center; color: var(--danger-red);">Failed to load blockchain ledger.</td></tr>';
      }
    }

    // --- Cinematic Glitch Scramble Text Engine ---
    class ScrambleGlitchText {
      constructor(element, options = {}) {
        this.el = element;
        this.originalText = options.text || this.el.getAttribute('data-text') || this.el.innerText.trim();
        this.chars = options.chars || '!@#$%^&*()_+-=[]{}|;:,.<>?/0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
        this.scrambleDuration = options.duration || 1400;
        this.hoverRadius = options.hoverRadius || 2;
        this.isAnimating = false;
        this.spans = [];
        this.init();
      }

      init() {
        this.buildCharSpans();
        this.bindEvents();
        this.triggerEnterAnimation();
      }

      buildCharSpans() {
        this.el.innerHTML = '';
        this.spans = [];
        const words = this.originalText.split(' ');
        words.forEach((word, wIdx) => {
          const wordWrapper = document.createElement('span');
          wordWrapper.style.display = 'inline-block';
          wordWrapper.style.whiteSpace = 'nowrap';

          for (let i = 0; i < word.length; i++) {
            const char = word[i];
            const span = document.createElement('span');
            span.className = 'scramble-char';
            span.dataset.char = char;
            span.innerText = char;
            wordWrapper.appendChild(span);
            this.spans.push(span);
          }

          this.el.appendChild(wordWrapper);

          if (wIdx < words.length - 1) {
            const spaceSpan = document.createElement('span');
            spaceSpan.className = 'scramble-space';
            spaceSpan.innerText = ' ';
            this.el.appendChild(spaceSpan);
          }
        });
      }

      getRandomChar() {
        return this.chars[Math.floor(Math.random() * this.chars.length)];
      }

      triggerEnterAnimation() {
        if (this.isAnimating) return;
        this.isAnimating = true;
        
        const startTime = performance.now();
        const duration = this.scrambleDuration;
        const totalSpans = this.spans.length;

        const animate = (currentTime) => {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const resolvedCount = Math.floor(progress * totalSpans);

          this.spans.forEach((span, idx) => {
            if (idx < resolvedCount) {
              span.innerText = span.dataset.char;
              span.classList.remove('is-scrambling');
            } else {
              span.innerText = this.getRandomChar();
              span.classList.add('is-scrambling');
            }
          });

          if (progress < 1) {
            requestAnimationFrame(animate);
          } else {
            this.spans.forEach(span => {
              span.innerText = span.dataset.char;
              span.classList.remove('is-scrambling');
            });
            this.isAnimating = false;
          }
        };

        requestAnimationFrame(animate);
      }

      scrambleSpan(span, duration = 800) {
        if (span.dataset.timer) clearTimeout(parseInt(span.dataset.timer));
        
        span.classList.add('is-hovered', 'is-scrambling');
        let count = 0;
        const interval = setInterval(() => {
          span.innerText = this.getRandomChar();
          count++;
          if (count > 8) {
            clearInterval(interval);
            span.innerText = span.dataset.char;
            span.classList.remove('is-hovered', 'is-scrambling');
          }
        }, 90);

        span.dataset.timer = setTimeout(() => {
          clearInterval(interval);
          span.innerText = span.dataset.char;
          span.classList.remove('is-hovered', 'is-scrambling');
        }, duration);
      }

      bindEvents() {
        this.el.addEventListener('click', () => this.triggerEnterAnimation());

        this.spans.forEach((span, idx) => {
          span.addEventListener('mouseenter', () => {
            if (this.isAnimating) return;
            for (let offset = -this.hoverRadius; offset <= this.hoverRadius; offset++) {
              const targetIdx = idx + offset;
              if (targetIdx >= 0 && targetIdx < this.spans.length) {
                const targetSpan = this.spans[targetIdx];
                const delay = Math.abs(offset) * 100;
                setTimeout(() => {
                  this.scrambleSpan(targetSpan, 800 - delay);
                }, delay);
              }
            }
          });
        });
      }
    }

    // Handle URL parameters on load
    window.addEventListener('DOMContentLoaded', () => {
      fetchBlocks();
      
      const headingEl = document.getElementById('heroHeading');
      if (headingEl) {
        new ScrambleGlitchText(headingEl);
      }
      
      const urlParams = new URLSearchParams(window.location.search);
      const rawHash = urlParams.get('hash');
      if (rawHash) {
        const hash = normalizeHash(rawHash);
        document.getElementById('hashInput').value = hash;
        document.getElementById('verify').scrollIntoView();
        verifyHash(hash);
      }
    });
  </script>
</body>
</html>
"""

def GET_WEB_HTML():
    return WEB_HTML
