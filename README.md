
<h3 align="center">Similar Images</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/blackmonk13/similar_images.svg)](https://github.com/blackmonk13/similar_images/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/blackmonk13/similar_images.svg)](https://github.com/blackmonk13/similar_images/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="justify"> This is a Python-based application designed to identify and group similar images within a specified directory. It utilizes image hashing, specifically average hashing, to compare images efficiently. The tool offers the flexibility to scan directories at a single level or recursively, depending on the user's needs. The similarity threshold can be adjusted to control the sensitivity of the comparison process. The results are presented in a JSON format, making it easy to understand and process the grouped images further.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Contributing](#contributing)

## 🧐 About <a name = "about"></a>

The primary purpose of the project is to address the challenge of identifying and organizing similar images within large datasets. Manually comparing and categorizing images can be a laborious and impractical task, especially when dealing with a significant number of images. By employing image hashing techniques, the project aims to streamline this process, making it more efficient and accurate. The tool can be particularly useful for image deduplication, image organization, and content-based image retrieval tasks, offering a valuable solution for individuals and organizations working with extensive image collections.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

To get started with the Similarity Finder project, you need to have the following software installed on your local machine:

1. Git - [Download & Install Git](https://git-scm.com/downloads)
2. Python (version 3.6 or higher) - [Download & Install Python](https://www.python.org/downloads/)

### Installing

Here's a step-by-step guide to help you set up a development environment for the Similarity Finder project:

1. Clone the repository

```bash
git clone https://github.com/blackmonk13/similar_images.git
```

2. Navigate to the project directory

```bash
cd similar_images
```

3. Set up a Python virtual environment (optional but recommended)

```bash
python3 -m venv env
```

4. Activate the virtual environment

On Windows:

```bash
.\env\Scripts\activate
```

On macOS and Linux:

```bash
source env/bin/activate
```

5. Install the dependencies from the `requirements.txt` file

```bash
pip install -r requirements.txt
```

6. Run the project using the command mentioned in the [Usage](#usage) section.


## 🎈 Usage <a name="usage"></a>

To use the Similarity Finder, run the following command in your terminal:

```bash
python -m similar_images -t 1 -r -o json -f output.json path/to/your/image/directory
```

Replace path/to/your/image/directory with the path to the directory containing images you want to analyze. The -t flag sets the similarity threshold (default is 10), the -r flag enables or disables recursive directory scanning, the -o flag sets the output format (default is json), and the -f flag specifies the path to the output file.

The application will output a JSON or CSV file containing groups of similar images found in the specified directory.

## 🚀 Deployment <a name = "deployment"></a>

You can find the latest wheel (.whl) file in the release page. To deploy the project on a live system:

#### Unix-like systems (macOS, Linux)

Run the following command in your terminal:

```bash
curl -s https://api.github.com/repos/blackmonk13/similar_images/releases/latest | jq -r '.assets[] | select(.name | endswith(".whl")) | .browser_download_url' | xargs pip install
```

#### Windows

Open PowerShell and run the following command:

```powershell
(Invoke-WebRequest -Uri "https://api.github.com/repos/blackmonk13/similar_images/releases/latest" -UseBasicParsing | ConvertFrom-Json).assets | Where-Object { $_.name -like "*whl" } | ForEach-Object { pip install $_.browser_download_url }
```

This command will install the project and its dependencies, allowing you to run the `similar_images` command directly from your terminal or Command Prompt without any hassle.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Programming Language
- [Pillow](https://pillow.readthedocs.io/en/stable/) - Image Processing Library
- [imagehash](https://github.com/JohannesBuchner/imagehash) - Image Hashing Library
- [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor) - Concurrency Library for Python

## ✍️ Authors <a name = "authors"></a>

- [@blackmonk13](https://github.com/blackmonk13) - Idea & Initial work

See also the list of [contributors](https://github.com/blackmonk13/similar_images/contributors) who participated in this project.

## Contributing <a name="contributing"></a>

We welcome contributions from the community! If you'd like to contribute to Banner, please follow these steps:

1. Fork the repository and create a new branch for your changes.
4. Commit your changes and push them to your fork.
5. Open a pull request against the main branch of the original repository.

Please make sure that your contributions adhere to the project's coding style and guidelines.

Before submitting a pull request, please make sure that:

1. Your changes do not introduce any new bugs or regressions.
4. Your code is well-documented and easy to understand.