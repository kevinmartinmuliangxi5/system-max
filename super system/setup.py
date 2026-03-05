from setuptools import setup, find_packages

setup(
    name="commander-system",
    version="23.0",
    packages=find_packages(where=".janus"),
    package_dir={"": ".janus"},
    py_modules=["dealer", "quick_check"],
    install_requires=[
        "pyperclip>=1.8.2",
        "colorama>=0.4.6",
        "requests"
    ],
    extras_require={
        "chinese": ["jieba>=0.42.1"],  # 可选：用于中文分词，提升中文记忆检索效果
        "full": ["jieba>=0.42.1"],  # 完整版：包含所有可选功能
    },
)