# demo-battery-health

Battery-health scoring. It combines remaining capacity, internal resistance and cycle count into a 0–100 score and band, using weights from `config/scoring.yaml`. **Synthetic demo repository.** All weights and data are fictional sample material for a security-remediation demo.

**Owner:** `@demo-org/energy-storage-team` (see `.github/CODEOWNERS`)

## Develop

Requires Python 3.11.

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## Security scanning

CI runs `pip-audit` (dependencies), `osv-scanner` (SARIF) and `bandit` (code patterns) in the `security-scan` job. Reports are uploaded as artifacts, and the SARIF goes to GitHub code scanning.

## Licence

MIT
