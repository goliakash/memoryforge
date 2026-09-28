from setuptools import setup, find_packages

setup(
    name="ai-security-memory-agent",
    version="1.0.0",
    description="AI Security Operations & Compliance Memory Agent powered by Hindsight",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "httpx",
        "rich",
        "hindsight-client",
    ],
    entry_points={
        "console_scripts": [
            "secops-demo=demo.demo_story:run_full_demo",
        ],
    },
)
