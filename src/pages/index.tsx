import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

function HomepageHero() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', 'hero--m31a')}>
      <div className="container">
        <span className="badge-tag">Production Engineering Documentation</span>
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle" style={{maxWidth: '750px', margin: '0 auto 1.5rem auto', color: '#94a3b8', fontSize: '1.25rem'}}>
          <strong>"The model proposes. The runtime decides."</strong><br/>
          Rust-native autonomous software engineering runtime with non-bypassable policy gates, verifiable execution, and isolated git attribution.
        </p>
        <div style={{display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap'}}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro/overview"
            style={{fontWeight: 700}}>
            Explore System Architecture
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/getting-started/quickstart">
            Quickstart Tutorial
          </Link>
          <Link
            className="button button--outline button--secondary button--lg"
            to="/docs/codebase/overview">
            Inspect Codebase (567 files)
          </Link>
        </div>
      </div>
    </header>
  );
}

const audiences = [
  {
    title: '🚀 First-Time Users',
    badge: 'Onboarding & Quickstart',
    description: 'Install M31A via standalone binaries or cargo, connect your NVIDIA NIM API key, complete workspace onboarding, and launch your first autonomous coding task.',
    links: [
      { label: 'Installation Guide', to: '/docs/getting-started/installation' },
      { label: '5-Minute Quickstart', to: '/docs/getting-started/quickstart' },
      { label: 'Interactive Setup Wizard', to: '/docs/getting-started/onboarding' },
    ],
    primaryAction: { label: 'Start Setup', to: '/docs/getting-started/installation' },
  },
  {
    title: '⚡ Experienced Operators',
    badge: 'CLI & TUI Operations',
    description: 'Master CLI automation, execution runs, session fork/resume, TUI keyboard cockpit shortcuts, custom slash commands, and profiles.',
    links: [
      { label: 'CLI Hierarchy & Flags', to: '/docs/user-guide/cli-usage' },
      { label: 'TUI Cockpit Controls', to: '/docs/user-guide/tui-cockpit' },
      { label: 'Execution Runs & Tasks', to: '/docs/user-guide/execution-lifecycle' },
    ],
    primaryAction: { label: 'Open User Manual', to: '/docs/user-guide/cli-usage' },
  },
  {
    title: '🦀 Rust Developers',
    badge: 'Codebase Reference',
    description: 'Deep-dive into every first-party Rust module across all 42 subsystems, understanding structs, traits, async runtimes, and SQLite transactions.',
    links: [
      { label: 'Complete Codebase Index', to: '/docs/codebase/overview' },
      { label: 'Local Development Setup', to: '/docs/developer/setup' },
      { label: 'Adding Tools & Agents', to: '/docs/developer/adding-tools-and-agents' },
    ],
    primaryAction: { label: 'Explore Source Tree', to: '/docs/codebase/overview' },
  },
  {
    title: '📐 Architecture Researchers',
    badge: 'L0-L9 System Architecture',
    description: 'Explore the 10-layer architectural hierarchy, downward dependency discipline, DAG scheduling, Nyquist verification gates, and crash recovery.',
    links: [
      { label: 'L0-L9 Layer Structure', to: '/docs/architecture/overview' },
      { label: 'Runtime Authority Model', to: '/docs/architecture/runtime-authority' },
      { label: 'Planning & DAG Materialization', to: '/docs/architecture/planning-dag' },
    ],
    primaryAction: { label: 'Read Architecture', to: '/docs/architecture/overview' },
  },
  {
    title: '🛡️ Security & Operations',
    badge: 'Policy & Hardening',
    description: 'Evaluate non-bypassable policy gates, process sandboxing, sensitive path controls, compile-time deployment channels, and rollback mechanics.',
    links: [
      { label: 'Security & Threat Model', to: '/docs/security/overview' },
      { label: 'Policy Gates & Approvals', to: '/docs/user-guide/policy-approvals' },
      { label: 'Deployment Channels', to: '/docs/deployment/overview' },
    ],
    primaryAction: { label: 'Review Security', to: '/docs/security/overview' },
  },
  {
    title: '🧪 Quality Engineers & Contributors',
    badge: '266-Test Verification',
    description: 'Inspect the comprehensive test suite spanning architectural invariant tests, security regression tests, parity tests, and CI qualification.',
    links: [
      { label: 'Complete Test Suite Catalog', to: '/docs/tests/overview' },
      { label: 'Live Test Partition Contract', to: '/docs/tests/categories' },
      { label: 'Contributor Guidelines', to: '/docs/developer/contributing' },
    ],
    primaryAction: { label: 'Browse Test Catalog', to: '/docs/tests/overview' },
  },
];

export default function Home(): React.JSX.Element {
  return (
    <Layout
      title="Production Documentation"
      description="Authoritative documentation platform for M31 Autonomous (M31A) - Rust-native autonomous coding runtime.">
      <HomepageHero />
      <main className="container" style={{paddingTop: '3rem', paddingBottom: '5rem'}}>
        <section>
          <div style={{textAlign: 'center', marginBottom: '2.5rem'}}>
            <h2 style={{fontSize: '2rem', marginBottom: '0.5rem'}}>Choose Your Learning Path</h2>
            <p style={{color: '#94a3b8', fontSize: '1.1rem'}}>
              Comprehensive documentation built directly from the M31A source code, tests, and database migrations.
            </p>
          </div>

          <div className="card-grid">
            {audiences.map((aud, idx) => (
              <div key={idx} className="audience-card">
                <span style={{fontSize: '0.75rem', fontWeight: 600, color: 'var(--ifm-color-primary)', textTransform: 'uppercase', marginBottom: '0.5rem', letterSpacing: '0.05em'}}>
                  {aud.badge}
                </span>
                <h3>{aud.title}</h3>
                <p>{aud.description}</p>
                <ul style={{listStyle: 'none', paddingLeft: 0, margin: '1rem 0', fontSize: '0.9rem'}}>
                  {aud.links.map((link, lidx) => (
                    <li key={lidx} style={{marginBottom: '0.4rem'}}>
                      <Link to={link.to} style={{textDecoration: 'none'}}>
                        → {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
                <Link className="card-btn" to={aud.primaryAction.to}>
                  {aud.primaryAction.label}
                </Link>
              </div>
            ))}
          </div>
        </section>

        <section style={{marginTop: '4rem'}}>
          <div className="feature-box">
            <h3 style={{marginTop: 0, color: 'var(--ifm-color-primary)'}}>Key Architectural Reality & Invariants</h3>
            <p style={{marginBottom: '0.5rem'}}>
              M31A is an autonomous engineering platform built on strict high-assurance invariants:
            </p>
            <ul style={{paddingLeft: '1.25rem', marginBottom: 0}}>
              <li><strong>The model proposes. The runtime decides:</strong> The LLM never directly executes shell commands, writes to databases, or marks work complete.</li>
              <li><strong>ExecutionRun Consolidation:</strong> Canonical execution authority is held by <code>ExecutionRun</code> (migrations 030-032). Legacy missions are backward-compatibility adapters.</li>
              <li><strong>Sole Production Provider:</strong> Production model invocation is strictly wired to NVIDIA NIM (<code>integrate.api.nvidia.com/v1</code>). All other providers fail closed with clear diagnostics.</li>
              <li><strong>Compile-Time Deployment Channels:</strong> <code>production</code> (default) and <code>development</code> (isolated <code>m31a-dev</code> state) are mutually exclusive compile-time channels.</li>
              <li><strong>Deterministic Verification:</strong> 7-tier verification hierarchy blocks task success on model self-report alone, requiring cryptographic artifact snapshot matching.</li>
            </ul>
          </div>
        </section>
      </main>
    </Layout>
  );
}
