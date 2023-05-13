import asyncio
from uuid import uuid4

from temporalio.client import Client

from tasks import FileProcessing

# let's populate pinecone with the docs
urls = [
    "https://www.gitpod.io/docs/references/gitpod-yml",
    "https://www.gitpod.io/docs/introduction",
    "https://www.gitpod.io/docs/introduction/getting-started",
    "https://www.gitpod.io/docs/introduction/languages/javascript",
    "https://www.gitpod.io/docs/introduction/languages/python",
    "https://www.gitpod.io/docs/introduction/languages/java",
    "https://www.gitpod.io/docs/introduction/languages/go",
    "https://www.gitpod.io/docs/configure/workspaces",
    "https://www.gitpod.io/docs/configure/user-settings",
    "https://www.gitpod.io/docs/configure/projects",
    "https://www.gitpod.io/docs/configure/orgs",
    "https://www.gitpod.io/docs/configure/authentication",
    "https://www.gitpod.io/docs/configure/self-hosted/latest",
    "https://www.gitpod.io/docs/configure/billing",
    "https://www.gitpod.io/docs/references/gitpod-cli",
    "https://www.gitpod.io/docs/help/troubleshooting"
]

async def main():
    # Connect client
    client = await Client.connect("localhost:7233")

    # Start 10 concurrent workflows
    futures = []
    for idx in range(len(urls)):
        result = client.execute_workflow(
            FileProcessing.run,
            urls[idx],
            id=f"activity_sticky_queue-workflow-id-{idx}",
            task_queue="activity_sticky_queue-distribution-queue",
        )
        await asyncio.sleep(0.1)
        futures.append(result)

    checksums = await asyncio.gather(*futures)
    print("\n".join([f"Output checksums:"] + checksums))


if __name__ == "__main__":
    asyncio.run(main())