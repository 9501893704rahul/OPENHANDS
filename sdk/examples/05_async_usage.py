#!/usr/bin/env python3
"""
OpenHands SDK - Async Usage Example

This example shows how to use OpenHands SDK with async/await
for better performance and concurrent operations.
"""
import sys
import asyncio
sys.path.append('..')

from openhands_client import OpenHandsClient

async def main():
    print("=" * 60)
    print("OpenHands SDK - Async Usage Example")
    print("=" * 60)
    
    # Create async client
    client = OpenHandsClient(provider="deepseek_local")
    await client.start()
    
    try:
        # Example 1: Run multiple commands concurrently
        print("\n📌 Example 1: Concurrent command execution")
        print("-" * 40)
        
        commands = [
            "echo 'Task 1' && sleep 1 && echo 'Done 1'",
            "echo 'Task 2' && sleep 1 && echo 'Done 2'",
            "echo 'Task 3' && sleep 1 && echo 'Done 3'",
        ]
        
        # Run all commands concurrently
        results = await asyncio.gather(*[
            client.run_command(cmd) for cmd in commands
        ])
        
        for i, result in enumerate(results, 1):
            print(f"Result {i}: {result.strip()}")
        
        # Example 2: Parallel file operations
        print("\n📌 Example 2: Parallel file operations")
        print("-" * 40)
        
        files_to_create = {
            "file1.txt": "Content for file 1",
            "file2.txt": "Content for file 2",
            "file3.txt": "Content for file 3",
        }
        
        # Write all files concurrently
        await asyncio.gather(*[
            client.write_file(name, content)
            for name, content in files_to_create.items()
        ])
        
        print("Created files concurrently!")
        
        # Read all files concurrently
        contents = await asyncio.gather(*[
            client.read_file(name)
            for name in files_to_create.keys()
        ])
        
        for name, content in zip(files_to_create.keys(), contents):
            print(f"{name}: {content.strip()}")
        
        # Example 3: Async AI task
        print("\n📌 Example 3: Async AI task")
        print("-" * 40)
        
        state = await client.ask(
            "Create a simple Python script that prints the Fibonacci sequence up to 100",
            max_iterations=5
        )
        print("AI task completed!")
        
        # Example 4: Browse multiple URLs
        print("\n📌 Example 4: Browse multiple URLs concurrently")
        print("-" * 40)
        
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/ip",
            "https://httpbin.org/user-agent",
        ]
        
        results = await asyncio.gather(*[
            client.browse_url(url) for url in urls
        ])
        
        for url, result in zip(urls, results):
            print(f"{url}: {len(result.get('content', ''))} chars")
        
    finally:
        await client.stop()

    print("\n" + "=" * 60)
    print("✅ Async examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
