ABSTRACT
The ML-Based Code Quality RevieIr & Debugging Tool is an intelligent system that utilizes a
finetuned Large Language Model (LLM) along with traditional static analysis tools to evaluate code
quality, detect errors, and provide context-aware debugging suggestions. The LLM istrained on a curated
dataset of high-quality and erroneous code snippets, enabling it to classify code as "Good" or "Needs
Improvement" while offering optimized corrections. The system employs FastAPI for real-time
processing, allowing developers to submit entire projects for analysis. It integrates Supervised Learning
(Classification) with Rule-Based Error Checking, using pylint, flake8, and AST-based parsing to identify
syntax errors, logical flaws, and code smells. Additionally, the tool provides best practice
recommendations, helping developers write maintainable and efficient code. By combining ML-driven
insights with traditional static analysis, this tool enhances developer productivity and code reliability.

Introduction
Software development relies heavily on maintaining high-quality code that is efficient, readable, and free from
errors. Traditional static analysis tools like pylint and flake8 help detect basic issues, but they often lack
contextual understanding and fail to provide intelligent suggestions. To address this gap, our project introduces
an ML-Based Code RevieIr & Debugging Tool, which leverages Large Language Models (LLMs) and
Machine Learning (ML) techniques to enhance code quality assessment and automated debugging.
Our system integrates Supervised Learning (Classification) with Rule-Based Error Checking to evaluate
code, identify potential bugs, and suggest meaningful improvements. The LLM, trained on diverse high
quality and erroneous code samples, provides intelligent insights beyond conventional static analysis tools.
The project employs FastAPI for real-time processing, allowing users to submit entire projects for analysis,
making it scalable and efficient. By combining AI-driven analysis with traditional static code checkers, our
tool enhances developer productivity, promotes coding best practices, and ensures robust software quality.
To achieve seamless interaction and real-time processing, our tool is built using FastAPI, a high
performance Ib framework for handling API requests efficiently. FastAPI enables users to submit entire
projects for automated review, making the tool scalable and responsive. The LLM is sourced from
Hugging Face Transformers, an open-source library offering state-of-the-art pre-trained models for various
AI applications. By fine-tuning these models on structured datasets, I enhance their ability to understand and
assess code effectively.
By combining AI-driven analysis with traditional static code checkers, our tool enhances developer
productivity, promotes coding best practices, and ensures robust software quality. The integration of ML,
FastAPI, and Hugging Face Transformers creates an innovative, intelligent, and scalable solution for realtime code quality evaluation and debugging, reducing development time while improving overall software
reliability.

FastAPI
FastAPI is a modern, high-performance Ib framework designed for building APIs with Python. It is used in
our project to create a fast and scalable backend that processes user-submitted code and interacts with the LLM
for analysis. Its asynchronous nature ensures quick responses, making it ideal for handling large-scale code
reviews efficiently. Additionally, FastAPI's built-in support for automatic OpenAPI documentation
simplifies API management and integration, allowing seamless interactions betIen the frontend and backend
components of our system. The API serves as the communication layer betIen the user and the AI-poIred
analysis, enabling real-time feedback and debugging suggestions.

Review of Research Papers
[1]. Combining Large Language Models with Static Analyzers for Code Review Generation
Authors: Imen Jaoua, Oussama Ben Sghaier, Houari Sahraoui
Published: February 2025
Summary: This paper proposes a hybrid approach that integrates large language models (LLMs) with static
analyzers to enhance code review generation. The method incorporates knowledge at various stages of the LLM
pipeline, aiming to improve the relevance and completeness of review comments.
[2]. Evaluating Diverse Large Language Models for Automatic and General Bug Reproduction
Published: October 2024
Summary: This research evaluates various large language models for their effectiveness in automatically
reproducing software bugs, contributing to the understanding of LLM capabilities in debugging tasks.
[3] LLM-Based Code Review using GPT Models Stanford University (2022)
Explores the application of GPT-3 in automated code review, demonstrating how large language models can
analyze, suggest improvements, and detect security flaws in source code. The paper emphasizes that
finetuned transformer models significantly improve contextual understanding compared to traditional static
analysis tools, making them valuable for software quality assurance.
[4] FastAPI for AI-Driven Code Quality Assessment ACM Transactions on Software Engineering
(2022)
Examines the implementation of FastAPI as a backend for AI-poIred code analysis tools. The study discusses
how FastAPI's asynchronous processing and scalability improve the performance of machine learning models
analyzing large codebases in real time. The paper also highlights FastAPI’s built-in automatic documentation
(OpenAPI), which facilitates seamless API integration.

Existing Systems and Tools
1. pylint & flake8 – Basic static analysis tools that check for syntax errors and style violations but lack
AI-based intelligent suggestions.
2. SonarQube – A rule-based code quality tool that detects bugs and security vulnerabilities but does not
provide AI-driven insights or debugging help.
3. GitHub CodeQL – Performssecurity analysis by querying code but does not offer real-time debugging
suggestions or ML-based improvements.
4. ESLint – A JavaScript linting tool that ensures code follows best practices but does not analyze deeper
logical errors.
5. DeepCode – Uses symbolic AI to detect issues but has limited contextual understanding compared to
LLM-poIred tools.

Problem Statement
Traditional static analysis tools like pylint and flake8 detect syntax errors but lack contextual understanding
and intelligent debugging capabilities, making it difficult for developers to maintain high-quality code.
Existing AI-poIred solutions provide suggestions but often require extensive fine-tuning and fail to offer
real-time, project-wide analysis. To overcome these limitations, our ML-Based Code RevieIr & Debugging
Tool leverages Large Language Models (LLMs) from Hugging Face, Machine Learning (ML) techniques, and
FastAPI for automated code quality assessment, intelligent error detection, and real-time debugging
suggestions. By combining rule-based checks with AI-driven insights, our tool enhances software quality,
boosts developer productivity, and ensures more efficient and maintainable code.

Objectives
• To design a model for rule-based error detection with AI-driven insights for more accurate and
context-aware debugging.
• To design a model for using Hugging Face Transformers for fine-tuned LLMs, enabling intelligent
code analysis and improvement suggestions.
• To implement FastAPI for real-time processing, allowing users to submit entire projects for efficient
and scalable code review.
• To design a model for the detection of syntax errors, logical bugs, and code inefficiencies beyond
traditional static analysis tools like pylint and flake8.
• To design a model to enhance developer productivity by providing instant feedback and optimization
suggestions for better code maintainability.

Functional Requirements
Code Submission & Processing – The system must allow users to submit code files or entire projects for
analysis.
ML-Based Code Quality Assessment – The system should evaluate the quality of code using an LLM model
from Hugging Face and provide structured feedback.
Automated Debugging & Suggestions – The system must detect syntax and logical errors and suggest
appropriate fixes.
Static Code Analysis Integration – Must integrate traditional tools like Pylint & Flake8 for additional rulebased checks.
Real-Time API Processing (FastAPI) – The system should process requests efficiently using FastAPI for
rapid responses.
User Interface (Optional) – A simple UI (CLI/Ib-based) for users to upload and review code reports.
Code Optimization Suggestions – The system should recommend performance improvements based on
best practices.


METHODOLOGY
The primary goal of this project is to build a machine learning-based system that can automatically review
code quality and assist in debugging. Traditional tools use rule-based methods; this tool learns patterns from
real code to provide intelligent, adaptable analysis. Datasets are gathered from public sources such as GitHub,
Project CodeNet, and ManySStuBs4J. These include both buggy and corrected code snippets, across multiple
programming languages. Data is cleaned and structured to form labeled examples for training and evaluation.
Code is parsed into tokens or abstract syntax trees (ASTs), and features like indentation, line length, variable
naming, and complexity are extracted. For deep learning applications, pre-trained code embeddings (e.g.,
CodeBERT, GraphCodeBERT) are used to represent code semantics.
Two machine learning models are developed for the system: a classification model to detect whether a code
snippet is buggy, and a regression model to rate the quality of the code based on readability, maintainability,
and adherence to standards. Traditional machine learning methods such as Random Forest and XGBoost are
benchmarked alongside transformer-based models that are fine-tuned on code datasets.
Upon detecting an issue, the system provides debugging support using one of two approaches: retrieval-based
methods that match buggy code with similar corrected samples, and generation-based methods that use
transformer models to suggest fixes. The models are evaluated using metrics such as Accuracy, F1-Score,
Precision, and Recall for bug classification, and BLEU/CodeBLEU scores for suggestion quality. Additional
human evaluation is conducted to assess developer satisfaction and the usefulness of the tool.

CONCLUSION
The ML-Based Code RevieIr & Debugging Tool is an advanced AI-driven solution designed to enhance
code quality by integrating Large Language Models (LLMs) with traditional static analysis techniques. Unlike
conventional tools that rely solely on predefined rules, this system leverages Hugging Face Transformers to
analyze code contextually, detecting syntax errors, logical flaws, performance bottlenecks, and security
vulnerabilities while providing intelligent, real-time suggestions for improvement. Built using FastAPI, the
tool ensures scalability, efficiency, and seamless processing of entire projects. By combining ML-based
classification with rule-based validation, it offers a more comprehensive and accurate review process, reducing
false positives and improving overall debugging efficiency. Developers can use the tool via a user-friendly
CLI/Ib UI, enabling automated analysis and enhancing productivity. The system also promotes coding best
practices, maintainability, and security, making it invaluable for individual developers and large teams alike.
Future improvements will focus on support for multiple programming languages, deeper fine-tuning of LLMs,
integration with DevOps workflows, and cloud-based deployment, positioning it as a cutting-edge, scalable,
and indispensable solution for modern software development.
