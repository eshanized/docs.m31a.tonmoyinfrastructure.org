import {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'M31A Documentation',
  tagline: 'The model proposes. The runtime decides.',
  favicon: 'img/logo.svg',

  url: 'https://docs.m31a.tonmoyinfrastructure.org',
  baseUrl: '/',

  organizationName: 'eshanized',
  projectName: 'M31A',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          editUrl: 'https://github.com/eshanized/M31A/tree/master/',
          showLastUpdateAuthor: false,
          showLastUpdateTime: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        indexDocs: true,
        indexBlog: false,
        indexPages: true,
        docsRouteBasePath: '/docs',
      },
    ],
  ],

  themeConfig: {
    image: 'img/logo.svg',
    navbar: {
      title: 'M31A',
      logo: {
        alt: 'M31 Autonomous Logo',
        src: 'img/logo.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          to: '/docs/architecture/overview',
          label: 'Architecture',
          position: 'left',
        },
        {
          to: '/docs/subsystems/overview',
          label: 'Subsystems',
          position: 'left',
        },
        {
          to: '/docs/codebase/overview',
          label: 'Codebase (567 files)',
          position: 'left',
        },
        {
          to: '/docs/tests/overview',
          label: 'Tests (266 files)',
          position: 'left',
        },
        {
          to: '/docs/reference/cli',
          label: 'CLI & Config',
          position: 'left',
        },
        {
          href: 'https://m31a.tonmoyinfrastructure.org/',
          label: 'Product Site',
          position: 'right',
        },
        {
          href: 'https://github.com/eshanized/M31A',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            { label: 'Introduction', to: '/docs/intro/overview' },
            { label: 'Installation & Quickstart', to: '/docs/getting-started/quickstart' },
            { label: 'User Manual', to: '/docs/user-guide/cli-usage' },
            { label: 'Architecture Overview', to: '/docs/architecture/overview' },
          ],
        },
        {
          title: 'Deep Reference',
          items: [
            { label: 'Codebase Reference (567 Rust Files)', to: '/docs/codebase/overview' },
            { label: 'Test Suite Catalog (266 Test Files)', to: '/docs/tests/overview' },
            { label: 'Subsystem Manuals', to: '/docs/subsystems/overview' },
            { label: 'CLI & Exit Codes', to: '/docs/reference/cli' },
          ],
        },
        {
          title: 'Security & Operations',
          items: [
            { label: 'Security & Threat Model', to: '/docs/security/overview' },
            { label: 'Deployment & Channels', to: '/docs/deployment/overview' },
            { label: 'Troubleshooting & FAQ', to: '/docs/troubleshooting/diagnostics' },
            { label: 'Developer Handbook', to: '/docs/developer/setup' },
          ],
        },
        {
          title: 'Project & Ecosystem',
          items: [
            { label: 'Main Website', href: 'https://m31a.tonmoyinfrastructure.org/' },
            { label: 'GitHub Repository', href: 'https://github.com/eshanized/M31A' },
            { label: 'Issue Tracker', href: 'https://github.com/eshanized/M31A/issues' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} M31 Autonomous (M31A). Built with Docusaurus for high-assurance autonomous engineering.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
      additionalLanguages: [
        'rust',
        'toml',
        'bash',
        'json',
        'yaml',
        'sql',
        'diff',
        'markdown',
      ],
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
