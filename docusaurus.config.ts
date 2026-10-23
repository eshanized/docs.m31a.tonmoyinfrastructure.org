import {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'M31A Documentation',
  titleDelimiter: ' | ',
  tagline: 'The model proposes. The runtime decides.',
  favicon: 'img/favicon.svg',

  url: 'https://docs.m31a.tonmoyinfrastructure.org',
  baseUrl: '/',

  organizationName: 'eshanized',
  projectName: 'docs.m31a.tonmoyinfrastructure.org',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  stylesheets: [
    {
      href: 'https://fonts.googleapis.com',
      rel: 'preconnect',
    },
    {
      href: 'https://fonts.gstatic.com',
      rel: 'preconnect',
      crossOrigin: 'anonymous',
    },
    {
      href: 'https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&display=swap',
      rel: 'stylesheet',
    },
  ],

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
        searchBarShortcut: true,
        searchBarShortcutHint: true,
        searchBarPosition: 'right',
      },
    ],
  ],

  themeConfig: {
    image: 'img/social-card.svg',
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
          to: '/docs/user-guide/cli-usage',
          label: 'Guides',
          position: 'left',
        },
        {
          to: '/docs/architecture/overview',
          label: 'Architecture',
          position: 'left',
        },
        {
          to: '/docs/reference/cli',
          label: 'API Reference',
          position: 'left',
        },
        {
          href: 'https://github.com/eshanized/M31A',
          label: 'GitHub',
          position: 'right',
          className: 'header-github-link',
        },
      ],
    },
    footer: {
      links: [
        {
          title: 'Documentation',
          items: [
            { label: 'Introduction', to: '/docs/intro/overview' },
            { label: 'Installation & Quickstart', to: '/docs/getting-started/quickstart' },
            { label: 'User Manual & Guides', to: '/docs/user-guide/cli-usage' },
            { label: 'Architecture Overview', to: '/docs/architecture/overview' },
          ],
        },
        {
          title: 'Deep Reference',
          items: [
            { label: 'Codebase Reference', to: '/docs/codebase/overview' },
            { label: 'Test Suite Catalog', to: '/docs/tests/overview' },
            { label: 'Subsystem Manuals', to: '/docs/subsystems/overview' },
            { label: 'CLI & Exit Codes', to: '/docs/reference/cli' },
          ],
        },
        {
          title: 'Security & Operations',
          items: [
            { label: 'Security & Threat Model', to: '/docs/security/overview' },
            { label: 'Deployment & Channels', to: '/docs/deployment/overview' },
            { label: 'Troubleshooting & Diagnostics', to: '/docs/troubleshooting/diagnostics' },
            { label: 'Developer Handbook', to: '/docs/developer/setup' },
          ],
        },
        {
          title: 'Project & Ecosystem',
          items: [
            { label: 'Product Website', href: 'https://m31a.tonmoyinfrastructure.org/' },
            { label: 'GitHub Repository', href: 'https://github.com/eshanized/M31A' },
            { label: 'Issue Tracker', href: 'https://github.com/eshanized/M31A/issues' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} M31 Autonomous (M31A). Built for high-assurance autonomous engineering.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
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
      defaultMode: 'light',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
