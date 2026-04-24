# DeepSeek V4 Benchmark Deployment

## Mapping

- GitHub repository: `gateszhangc/deepseek-v4-benchmark`
- Git branch: `main`
- Dokploy project: `n/a`
- Image repository: `registry.144.91.77.245.sslip.io/deepseek-v4-benchmark`
- K8s manifest path: `deploy/k8s/overlays/prod`
- Argo CD application: `deepseek-v4-benchmark`
- Argo platform repo: `gateszhangc/argo-platform`
- Primary domain: `deepseekv4benchmark.lol`

Release chain:

`gateszhangc/deepseek-v4-benchmark -> main -> K8s build Job -> registry.144.91.77.245.sslip.io/deepseek-v4-benchmark -> deploy/k8s/overlays/prod newTag -> Argo CD deepseek-v4-benchmark`

## GitHub Actions

Workflow: [`.github/workflows/build-and-release.yml`](/Users/a1-6/Desktop/code/deepseekv4benchmark/.github/workflows/build-and-release.yml)

Required GitHub repository secrets:

- `KUBECONFIG_B64`
- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`

Behavior:

1. GitHub Actions derives `IMAGE_TAG=$GITHUB_SHA`.
2. Actions authenticates to the cluster with `KUBECONFIG_B64`.
3. Actions creates a temporary Kubernetes Job that clones the repo and builds the image with Kaniko.
4. The image is pushed to `registry.144.91.77.245.sslip.io/deepseek-v4-benchmark:<git-sha>`.
5. Actions updates `deploy/k8s/overlays/prod/kustomization.yaml` with the new tag and pushes a `[skip ci]` commit.
6. Argo CD auto-syncs the application.

## Kubernetes And Argo CD

Application repo manifests live under:

- [`deploy/k8s/base`](/Users/a1-6/Desktop/code/deepseekv4benchmark/deploy/k8s/base)
- [`deploy/k8s/overlays/prod`](/Users/a1-6/Desktop/code/deepseekv4benchmark/deploy/k8s/overlays/prod)

Argo platform repo must contain:

- `clusters/prod/apps/10-deepseek-v4-benchmark-appproject.yaml`
- `clusters/prod/apps/20-deepseek-v4-benchmark-application.yaml`

The Argo `Application` should point to:

- `repoURL: https://github.com/gateszhangc/deepseek-v4-benchmark.git`
- `targetRevision: main`
- `path: deploy/k8s/overlays/prod`

## DNS And GSC

Cloudflare is the DNS authority for `deepseekv4benchmark.lol`.

Expected records:

- apex `A` -> `89.167.61.228`
- `www` `CNAME` -> `deepseekv4benchmark.lol`

GSC scope:

- property type: `Domain`
- property: `sc-domain:deepseekv4benchmark.lol`
- required sitemap: `https://deepseekv4benchmark.lol/sitemap.xml`

This project intentionally skips GA4 and Clarity. Release-time flags should stay:

- `SKIP_GSC=false`
- `SKIP_GA4=true`
- `SKIP_CLARITY=true`

## Verification

Local:

```bash
npm test
docker build -t deepseek-v4-benchmark .
docker run --rm -p 3000:3000 deepseek-v4-benchmark
curl http://127.0.0.1:3000/healthz
```

Production:

```bash
curl -I https://deepseekv4benchmark.lol/
curl -I https://deepseekv4benchmark.lol/robots.txt
curl -I https://deepseekv4benchmark.lol/sitemap.xml
argocd app get deepseek-v4-benchmark
```

GSC checks:

```bash
export PRIMARY_URL="https://deepseekv4benchmark.lol"
export GSC_PROPERTY_TYPE="domain"
export GSC_SITE_URL="sc-domain:deepseekv4benchmark.lol"
export GSC_SITEMAP_URL="https://deepseekv4benchmark.lol/sitemap.xml"
bash "$HOME/.codex/skills/webapp-launch-analytics/scripts/check-gsc-property.sh"
```

## Rollback

1. Revert the `newTag` change in `deploy/k8s/overlays/prod/kustomization.yaml`.
2. Push the revert to `main`.
3. Wait for Argo CD to auto-sync back to the previous image.
4. Re-run the production verification commands.
