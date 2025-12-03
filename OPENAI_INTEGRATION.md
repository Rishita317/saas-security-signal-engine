````markdown
# OpenAI Integration

## Overview

This project uses **OpenAI GPT-4o-mini** for job and conversation classification. It provides high-quality relevance classification and is available via an API key.

## Setup

### 1. Get Your OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Click "Create new key"
3. Copy your key (format: `sk-...`)

### 2. Add to Environment

Edit `.env` file:

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Notes

- When using GitHub Actions, add `OPENAI_API_KEY` as a repo secret and reference `secrets.OPENAI_API_KEY` in workflows.
- Keep your key private — do not commit it to the repository.

## Usage Examples

Use the `JobClassifier` and `ConversationClassifier` classes. They default to `openai` and will look for `OPENAI_API_KEY` in your environment.

```bash
python test_pipeline_openai.py
```
````
