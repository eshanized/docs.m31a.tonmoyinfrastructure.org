# Documentation Website Hosting

Deployment guide for this Docusaurus documentation website at `https://docs.m31a.tonmoyinfrastructure.org/`.

## Hosting Infrastructure

- **Domain**: `docs.m31a.tonmoyinfrastructure.org`
- **Engine**: Docusaurus v3 (Static HTML/JS generation)
- **Base URL**: `/`
- **Output Directory**: `build/`

## Production Build

```bash
cd /home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org
npm run build
```

The resulting `build/` directory is completely self-contained and ready for deployment to any static hosting provider (Cloudflare Pages, Vercel, Netlify, Nginx, or AWS S3 + CloudFront).
