import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

/* ==========================================================================
   Icons (Restrained SVG Icons - Engineering Documentation Language)
   ========================================================================== */

function SearchIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="9" cy="9" r="6" />
      <line x1="13.5" y1="13.5" x2="18" y2="18" />
    </svg>
  );
}

function RocketIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4.5 15.5l2-2m-2 2l-1 3.5 3.5-1 4.5-4.5c2-2 3.5-4.5 4.5-7.5-3 1-5.5 2.5-7.5 4.5L4.5 15.5z" />
      <circle cx="12.5" cy="7.5" r="1.5" />
    </svg>
  );
}

function TerminalIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2.5" y="3.5" width="15" height="13" rx="2" />
      <polyline points="6 8 8.5 10 6 12" />
      <line x1="11" y1="12" x2="14" y2="12" />
    </svg>
  );
}

function LayersIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="10 2.5 17 6.5 10 10.5 3 6.5 10 2.5" />
      <polyline points="3 10.5 10 14.5 17 10.5" />
      <polyline points="3 14 10 18 17 14" />
    </svg>
  );
}

function CodeIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="13 5 18 10 13 15" />
      <polyline points="7 15 2 10 7 5" />
      <line x1="11.5" y1="3.5" x2="8.5" y2="16.5" />
    </svg>
  );
}

function ShieldIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2.5L3.5 5.5v5c0 4.5 3 7.5 6.5 8.5 3.5-1 6.5-4 6.5-8.5v-5L10 2.5z" />
      <path d="M7.5 10l2 2 4-4" />
    </svg>
  );
}

function ArrowRightIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="3" y1="8" x2="13" y2="8" />
      <polyline points="9 4 13 8 9 12" />
    </svg>
  );
}

/* ==========================================================================
   Documentation Purpose Categories
   ========================================================================== */

interface DocLink {
  label: string;
  to: string;
}

interface DocCategory {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
  links: DocLink[];
}

const docCategories: DocCategory[] = [
  {
    title: 'Getting Started',
    icon: RocketIcon,
    description: 'Initial deployment, runtime binaries, workspace onboarding, and NVIDIA NIM setup.',
    links: [
      { label: 'Installation', to: '/docs/getting-started/installation' },
      { label: 'Quickstart Tutorial', to: '/docs/getting-started/quickstart' },
      { label: 'First-Run Configuration', to: '/docs/getting-started/onboarding' },
      { label: 'Model Setup & Credentials', to: '/docs/getting-started/model-setup' },
    ],
  },
  {
    title: 'Using M31A',
    icon: TerminalIcon,
    description: 'Operator CLI workflows, interactive Ratatui cockpit, session persistence, and change reviews.',
    links: [
      { label: 'CLI Reference & Arguments', to: '/docs/user-guide/cli-usage' },
      { label: 'Interactive TUI Cockpit', to: '/docs/user-guide/tui-cockpit' },
      { label: 'Sessions and Execution Runs', to: '/docs/user-guide/execution-lifecycle' },
      { label: 'Models and Configuration', to: '/docs/reference/configuration' },
      { label: 'Reviewing Changes and Verification', to: '/docs/user-guide/artifacts-evidence' },
    ],
  },
  {
    title: 'Architecture',
    icon: LayersIcon,
    description: '10-layer L0-L9 downward dependency discipline, runtime authority, and persistence models.',
    links: [
      { label: 'System Architecture (L0-L9)', to: '/docs/architecture/overview' },
      { label: 'Execution Authority Lifecycle', to: '/docs/architecture/runtime-authority' },
      { label: 'Agent Runtime Registry', to: '/docs/subsystems/agent-registry' },
      { label: 'Tools and Security Policy', to: '/docs/architecture/security-boundaries' },
      { label: 'Persistence and Recovery', to: '/docs/architecture/persistence-design' },
    ],
  },
  {
    title: 'Developers',
    icon: CodeIcon,
    description: 'Rust development environment, crate hierarchy, module specifications, and test validation.',
    links: [
      { label: 'Development Setup', to: '/docs/developer/setup' },
      { label: 'Module Reference (567 files)', to: '/docs/codebase/overview' },
      { label: 'API Reference & Exit Codes', to: '/docs/reference/cli' },
      { label: 'Testing Guide (266 tests)', to: '/docs/developer/testing-guidelines' },
      { label: 'Contributing Guidelines', to: '/docs/developer/contributing' },
    ],
  },
  {
    title: 'Operations and Security',
    icon: ShieldIcon,
    description: 'Process sandboxing with Landlock/seccomp, compile channels, diagnostics, and deployment.',
    links: [
      { label: 'Platform Support & Invariants', to: '/docs/intro/system-requirements' },
      { label: 'Security Model & Threat Defense', to: '/docs/security/overview' },
      { label: 'Troubleshooting & Diagnostics', to: '/docs/troubleshooting/diagnostics' },
      { label: 'Deployment and Releases', to: '/docs/deployment/overview' },
    ],
  },
];

/* ==========================================================================
   Curated Key References (Continue Learning)
   ========================================================================== */

interface KeyReference {
  tag: string;
  title: string;
  summary: string;
  linkText: string;
  to: string;
}

const keyReferences: KeyReference[] = [
  {
    tag: 'INV-01 // AUTHORITY',
    title: 'Runtime Authority Model',
    summary: 'The model proposes; the runtime decides. The LLM never writes to disk or executes shell commands directly without policy verification.',
    linkText: 'Inspect Authority Invariants',
    to: '/docs/architecture/runtime-authority',
  },
  {
    tag: 'INV-02 // LIFECYCLE',
    title: 'ExecutionRun Architecture',
    summary: 'Single canonical execution unit under task DAG scheduling, two-phase checkpointing, and complete state persistence across crashes.',
    linkText: 'View Execution Lifecycle',
    to: '/docs/user-guide/execution-lifecycle',
  },
  {
    tag: 'INV-03 // INFERENCE',
    title: 'NVIDIA NIM Provider Integration',
    summary: 'Dedicated enterprise production inference wired exclusively to NVIDIA NIM (integrate.api.nvidia.com/v1) with token compaction.',
    linkText: 'Configure Model Provider',
    to: '/docs/getting-started/model-setup',
  },
  {
    tag: 'INV-04 // DETERMINISM',
    title: 'Deterministic Nyquist Verification',
    summary: '7-tier verification hierarchy blocking task completion on model self-report, requiring cryptographic artifact snapshot matching.',
    linkText: 'Read Verification Manual',
    to: '/docs/subsystems/verification-nyquist',
  },
];

/* ==========================================================================
   Terminal Window Showcase Component
   ========================================================================== */

function TerminalShowcase() {
  const [copied, setCopied] = useState(false);
  const command = 'curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash';

  const handleCopy = () => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(command);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="m31a-terminal-showcase">
      <div className="m31a-terminal-header">
        <div className="m31a-terminal-dots">
          <span className="m31a-dot m31a-dot-red" />
          <span className="m31a-dot m31a-dot-yellow" />
          <span className="m31a-dot m31a-dot-green" />
        </div>
        <span className="m31a-terminal-title">m31a-runtime — x86_64-linux</span>
        <button
          type="button"
          className="m31a-terminal-copy-btn"
          onClick={handleCopy}
          aria-label="Copy install command"
        >
          {copied ? '✓ Copied' : 'Copy'}
        </button>
      </div>
      <div className="m31a-terminal-body">
        <div className="m31a-terminal-line">
          <span className="m31a-prompt">$</span>
          <span className="m31a-cmd">{command}</span>
        </div>
        <div className="m31a-terminal-line m31a-log-dim">
          <span>[m31a] validating rust toolchain (1.85.0+)...</span>
        </div>
        <div className="m31a-terminal-line">
          <span className="m31a-success-tick">✓</span>
          <span>Landlock ABI v3 sandboxing confirmed</span>
        </div>
        <div className="m31a-terminal-line">
          <span className="m31a-success-tick">✓</span>
          <span>NVIDIA NIM inference provider endpoint active</span>
        </div>
        <div className="m31a-terminal-line">
          <span className="m31a-prompt">&gt;</span>
          <span className="m31a-cmd">m31a ready. Run `m31a --help` or `m31a cockpit` to begin.</span>
        </div>
      </div>
    </div>
  );
}

/* ==========================================================================
   Homepage Component
   ========================================================================== */

export default function Home(): React.JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const [searchQuery, setSearchQuery] = useState('');
  const [isMac, setIsMac] = useState(false);

  useEffect(() => {
    if (typeof navigator !== 'undefined') {
      setIsMac(/(Mac|iPhone|iPod|iPad)/i.test(navigator.platform));
    }
  }, []);

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const query = searchQuery.trim();
    if (query) {
      window.location.href = `/search?q=${encodeURIComponent(query)}`;
    } else {
      const navInput = document.querySelector('.navbar__search-input') as HTMLInputElement | null;
      if (navInput) {
        navInput.focus();
      }
    }
  };

  return (
    <Layout
      title="Engineering Documentation"
      description="Authoritative systems documentation for M31 Autonomous (M31A) - Rust-native autonomous software engineering runtime.">
      <div className="m31a-home">
        {/* Section A: Compact Introductory Section */}
        <section className="m31a-hero" aria-labelledby="hero-heading">
          <div className="m31a-badge-pill">
            <span className="m31a-pulse-dot" />
            <span>M31 Autonomous Runtime</span>
            <span className="m31a-badge-sep">•</span>
            <span>v0.1.12 Architecture</span>
          </div>

          <h1 id="hero-heading" className="m31a-hero__title">
            <span className="m31a-title-gradient">M31A</span> Documentation
          </h1>

          <p className="m31a-hero__subtitle">
            <span className="m31a-tagline-quote">"The model proposes. The runtime decides."</span>
            Rust-native autonomous software engineering runtime with non-bypassable policy gates, verifiable execution, and isolated git attribution.
          </p>

          <div className="m31a-hero__actions">
            <Link className="m31a-btn-glow" to="/docs/getting-started/quickstart">
              <RocketIcon />
              <span>Get Started</span>
            </Link>
            <Link className="m31a-btn-secondary" to="/docs/architecture/overview">
              <LayersIcon />
              <span>Explore Architecture</span>
            </Link>
          </div>

          {/* Interactive Live Terminal Showcase */}
          <TerminalShowcase />
        </section>

        {/* Section B: Prominent Documentation Search */}
        <section className="m31a-search-container" aria-label="Documentation Search">
          <form className="m31a-search-form" onSubmit={handleSearchSubmit} role="search">
            <SearchIcon className="m31a-search-icon" />
            <input
              type="search"
              name="q"
              className="m31a-search-input"
              placeholder="Search documentation (e.g., policy, DAG, CLI, kernel, verification)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              aria-label="Search documentation"
              autoComplete="off"
            />
            <div className="m31a-search-shortcut" aria-hidden="true">
              <kbd className="m31a-kbd">{isMac ? '⌘' : 'Ctrl'}</kbd>
              <kbd className="m31a-kbd">K</kbd>
            </div>
          </form>

          <div className="m31a-search-chips">
            <span>Common topics:</span>
            <Link className="m31a-chip" to="/docs/getting-started/quickstart">Quickstart</Link>
            <Link className="m31a-chip" to="/docs/architecture/overview">Architecture</Link>
            <Link className="m31a-chip" to="/docs/user-guide/cli-usage">CLI</Link>
            <Link className="m31a-chip" to="/docs/architecture/runtime-authority">Authority</Link>
            <Link className="m31a-chip" to="/docs/codebase/overview">Codebase</Link>
            <Link className="m31a-chip" to="/docs/subsystems/verification-nyquist">Verification</Link>
          </div>
        </section>

        {/* Telemetry Stat Ribbon */}
        <section className="m31a-telemetry-ribbon" aria-label="Runtime Telemetry and Coverage Statistics">
          <div className="m31a-stat-grid">
            <div className="m31a-stat-item">
              <div className="m31a-stat-value">567</div>
              <div className="m31a-stat-label">First-Party Rust Files</div>
            </div>
            <div className="m31a-stat-item">
              <div className="m31a-stat-value">266</div>
              <div className="m31a-stat-label">Verified Test Cases</div>
            </div>
            <div className="m31a-stat-item">
              <div className="m31a-stat-value">42</div>
              <div className="m31a-stat-label">Modular Subsystems</div>
            </div>
            <div className="m31a-stat-item">
              <div className="m31a-stat-value">0</div>
              <div className="m31a-stat-label">Bypassable Policy Gates</div>
            </div>
          </div>
        </section>

        {/* Section C: Browse Documentation by Purpose */}
        <section className="m31a-categories-section" aria-labelledby="browse-heading">
          <div className="m31a-section-header">
            <h2 id="browse-heading" className="m31a-section-title">
              Browse by Purpose
            </h2>
            <p className="m31a-section-desc">
              Organized reference manuals and engineering guides for operators, developers, and researchers.
            </p>
          </div>

          <div className="m31a-category-grid">
            {docCategories.map((cat, idx) => {
              const IconComp = cat.icon;
              return (
                <article key={idx} className="m31a-category-card">
                  <div className="m31a-card-head">
                    <div className="m31a-icon-badge">
                      <IconComp />
                    </div>
                    <h3 className="m31a-card-title">{cat.title}</h3>
                  </div>
                  <p className="m31a-card-desc">{cat.description}</p>
                  <ul className="m31a-link-list">
                    {cat.links.map((link, lidx) => (
                      <li key={lidx}>
                        <Link className="m31a-link-row" to={link.to}>
                          <span>{link.label}</span>
                          <ArrowRightIcon className="m31a-link-arrow" />
                        </Link>
                      </li>
                    ))}
                  </ul>
                </article>
              );
            })}
          </div>
        </section>

        {/* Section D: Continue Learning / Key Engineering References */}
        <section className="m31a-invariants-section" aria-labelledby="invariants-heading">
          <div className="m31a-section-header">
            <h2 id="invariants-heading" className="m31a-section-title">
              Curated Key References
            </h2>
            <p className="m31a-section-desc">
              Foundational architectural invariants and operational guarantees governing the M31A runtime.
            </p>
          </div>

          <div className="m31a-invariants-grid">
            {keyReferences.map((ref, idx) => (
              <div key={idx} className="m31a-invariant-item">
                <span className="m31a-inv-tag">{ref.tag}</span>
                <h4>{ref.title}</h4>
                <p>{ref.summary}</p>
                <Link className="m31a-invariant-link" to={ref.to}>
                  <span>{ref.linkText}</span>
                  <ArrowRightIcon className="m31a-link-arrow" />
                </Link>
              </div>
            ))}
          </div>
        </section>
      </div>
    </Layout>
  );
}
