# Gitpod and Temporal Demo w/ GPT-4

A demo using Gitpod and Temporal to demonstrate workflows

Uses GPT-4 to retrieve docs and do an embedding for development based upon [this link](https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/pinecone/GPT4_Retrieval_Augmentation.ipynb).

Can then be used to add your data / context to your prompt, adding your knowledge to what GPT-4 has as context.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/burningion/demo-gitpod-temporal)

# Running the workflow

To run the workers you'll need to run the following:

```bash
$ cd src
$ python worker.py
```

In another terminal:

```bash
$ cd src
$ python starter.py
```

Check the output by going to port `8233`.