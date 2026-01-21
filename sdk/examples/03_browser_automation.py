#!/usr/bin/env python3
"""
OpenHands SDK - Browser Automation Example

This example shows how to use OpenHands SDK for web browsing
and automation tasks.
"""
import sys
sys.path.append('..')

from openhands_client import create_client

def main():
    print("=" * 60)
    print("OpenHands SDK - Browser Automation Example")
    print("=" * 60)
    
    with create_client(provider="deepseek_local") as client:
        
        # Example 1: Browse a URL and extract content
        print("\n📌 Example 1: Browse and extract content")
        print("-" * 40)
        result = client.browse_url("https://httpbin.org/html")
        print(f"URL: {result.get('url')}")
        print(f"Content preview: {result.get('content', '')[:500]}...")
        
        # Example 2: Web scraping task
        print("\n📌 Example 2: Web scraping with AI")
        print("-" * 40)
        client.ask("""
Browse to https://news.ycombinator.com and:
1. Extract the top 5 story titles
2. Save them to a file called 'hn_top_stories.txt'
3. Include the points and comment count for each
""")
        
        # Example 3: API testing via browser
        print("\n📌 Example 3: Test a REST API")
        print("-" * 40)
        client.ask("""
Use the browser to:
1. Go to https://jsonplaceholder.typicode.com/posts/1
2. Extract the JSON response
3. Save it to 'api_response.json'
4. Then fetch posts 2-5 and save them all to 'all_posts.json'
""")
        
        # Example 4: Form interaction
        print("\n📌 Example 4: Form automation")
        print("-" * 40)
        client.ask("""
Go to https://httpbin.org/forms/post and:
1. Take a screenshot of the form
2. Describe what fields are available
3. Create a Python script that would fill out this form using requests
4. Save the script as 'form_filler.py'
""")
        
        # Show results
        print("\n📌 Results:")
        print("-" * 40)
        result = client.run_command("ls -la *.txt *.json *.py 2>/dev/null || echo 'Files created in workspace'")
        print(result)

    print("\n" + "=" * 60)
    print("✅ Browser automation completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
