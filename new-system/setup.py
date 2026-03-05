"""
ECS - 安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# 读取requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')
    requirements = [r.strip() for r in requirements if r.strip() and not r.startswith('#')]

setup(
    name="emergent-collaboration",
    version="2.0.0",
    description="多Agent无领导小组讨论真涌现系统 - SPAR循环架构",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ECS Team",
    author_email="ecs-team@example.com",
    url="https://github.com/your-org/emergent-collaboration",
    project_urls={
        "Bug Reports": "https://github.com/your-org/emergent-collaboration/issues",
        "Source": "https://github.com/your-org/emergent-collaboration",
        "Documentation": "https://github.com/your-org/emergent-collaboration/wiki",
    },
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "mypy>=1.7.0",
            "flake8>=6.0",
        ],
        "visualization": [
            "matplotlib>=3.8.0",
            "networkx>=3.0",
            "plotly>=5.14.0",
        ],
        "all": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "mypy>=1.7.0",
            "flake8>=6.0",
            "matplotlib>=3.8.0",
            "networkx>=3.0",
            "plotly>=5.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ecs=ecs.cli:main",
            "ecs-cli=ecs.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="multi-agent emergence collaboration ai llm anthropic openai",
    python_requires=">=3.11",
)
