# Security Policy

## Supported Versions

We actively support the following versions of the Job Application Assistant:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do NOT** create a public issue

Please do not report security vulnerabilities through public GitHub issues.

### 2. Report privately

Send an email to: **security@job-assistant.local** (or create a private security advisory)

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if you have them)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (see below)

### 4. Severity Levels

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Remote code execution, privilege escalation | 24-48 hours |
| **High** | Authentication bypass, data exposure | 3-7 days |
| **Medium** | Limited data exposure, DoS | 1-2 weeks |
| **Low** | Information disclosure | 2-4 weeks |

## Security Considerations

### Local-First Design

The Job Application Assistant is designed with privacy in mind:

- **No cloud dependencies** - All processing happens locally
- **No data transmission** - Your documents and data never leave your machine
- **Local LLM models** - Uses Ollama for complete local inference
- **Minimal permissions** - Runs with standard user privileges

### Potential Security Areas

While the application is designed to be secure, please be aware of:

1. **File Processing**: The app processes uploaded documents (PDF, DOCX, etc.)
2. **Local Web Server**: Streamlit runs a local web server
3. **LLM Interactions**: Communication with local Ollama instance
4. **Configuration**: Environment variables and configuration files

### Best Practices for Users

1. **Keep software updated**: Always use the latest version
2. **Secure your system**: Ensure your OS and Python environment are up to date
3. **Network security**: The local web server should only be accessible locally
4. **File handling**: Only upload documents you trust
5. **Environment variables**: Protect your `.env` files and don't commit them

## Disclosure Policy

- We will acknowledge receipt of your vulnerability report
- We will provide regular updates on our progress
- We will notify you when the vulnerability is fixed
- We will publicly disclose the vulnerability in a responsible manner after a fix is released
- We may acknowledge your contribution (with your permission)

## Bug Bounty

Currently, we do not offer a paid bug bounty program, but we will:
- Acknowledge your contribution in our security credits
- Provide attribution in release notes (if desired)
- Consider featuring your contribution in project documentation

## Contact

For security-related questions or concerns:
- **Email**: security@job-assistant.local
- **GitHub**: Create a private security advisory
- **General Support**: Use GitHub issues for non-security questions

Thank you for helping keep the Job Application Assistant secure!
