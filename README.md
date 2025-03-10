# Quaser Mr.Q

Mr.Q 是個 AI智能助理，我們能透過 MR.Q 與 CNC加工機台互動，請他幫助你完成日常加工前準備、取得當前機台各項指標以及完成暖機作業等功能

# 技術展示

1. 自動解析腳本，完成各項作業流程
2. 使用 PyQT5 開發前端畫面
3. 使用 MVC 架構完成專案開發
4. 使用 Azure OPENAI, STT, TTS 等多項智能技術，完成全語音互動流程
5. 使用 RAG 技術，加入專業知識，使 GPT 能夠理解並依照指令回答我們所需要的內容

## Installation

#### 安裝包

.NET Framework 4.8 Developer Pack

[https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48)

Visual Studio 2019 Community

- 勾選 "使用C++的桌面開發"
- 勾選 "MSVC v142 - VS 2019 C++ ARM64 建置工具"
- 勾選 "Windows 10 SDK 10.0.16299.0"

Speech to Text

需額外安裝 [Visual Studio 2015、2017、2019 與 2022 的 Microsoft Visual C++ 可轉散發套件](https://learn.microsoft.com/zh-tw/cpp/windows/latest-supported-vc-redist?view=msvc-170&preserve-view=true)

#### 虛擬環境

Switch Win32

```plaintext
set CONDA_FORCE_32BIT=1 # switch win32
set CONDA_FORCE_32BIT=  # switch win64
```

Create ENV

```plaintext
conda create -n pyqt5-py38-32bit python=3.8
conda activate pyqt5-py38-32bit
```

Dependency

```plaintext
conda install pyqt // check the lib version is win32
conda install pandas // ...
pip install -r requirements.txt
```

## Execution

```Python
python main.py
```
