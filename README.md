# Memory Copilot

Memory Copilot wishes to be your external storage and personal assistant for your memory.
You can store any information you are interested in (webpage, articles, pdf, ...) through natural language. Memory Copilot will help to summarize and organize them. At the same time, you can recall this information just by using a few keywords.

The project aims to explore how to build an LLM-Agent based application. It's currently in its ealy stage. All feedbacks and discussions are welcome.

## Demos

## Getting Started

### Prerequisites

Export your openai api key as an environment variable:
```bash
export OPENAI_API_KEY=<your key here>
```

### Installation

Install using pip:
```bash
pip install git+ssh://git@github.com:Smilexuhc/memory_copilot.git
```

Install by cloning the repo:
```bash
git clone https://github.com/Smilexuhc/memory_copilot.git
cd memory_copilot
pip install -e .
```

Cli Usage:

```
copilot --help

Usage: copilot [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  chat
  clear
  delete
  dump
  show
```

Example:

```bash
copilot chat 'Help me mark the article from https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices'
```


## Roadmap

- Better UI (WebUI/GUI)
- Support more complex retreive strategies
- Support visual information like images and videos
- ...
