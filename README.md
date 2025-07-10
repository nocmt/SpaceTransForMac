# SpaceTransForMac - macOS即时翻译工具

## 项目介绍

SpaceTransForMac是一个macOS平台下的即时翻译工具，通过连续按下三次空格键触发翻译功能，将选中的文本翻译并自动替换。

### 主要特点

- **简单触发**：连续按下三次空格键即可触发翻译
- **智能翻译**：自动检测语言，中英文互译
- **即时替换**：翻译结果自动替换选中文本
- **AI驱动**：使用先进的AI模型提供高质量翻译

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone https://github.com/nocmt/SpaceTransForMac.git
cd SpaceTransForMac
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

首次运行程序时，系统会自动提示你输入必要的配置信息：

- API密钥（必填）
- API地址（默认为SiliconFlow API）
- 模型名称（默认为DeepSeek-V3）

这些配置会保存在用户主目录下的`~/.spacetrans/config.json`文件中，你可以随时手动编辑该文件修改配置。

## 使用方法

### 方法一：使用启动脚本

```bash
python run.py
```

启动脚本会自动检查依赖并提示安装，也会检查配置文件是否正确。
首次运行时会提示你输入必要的配置信息。

### 方法二：直接运行主程序

```bash
python main.py
```

### 方法三：使用打包好的应用程序

如果你已经使用PyInstaller打包了应用，可以直接运行生成的`.app`文件：

```bash
open dist/SpaceTrans.app
```

### 打包应用

你可以使用启动脚本来打包应用：

```bash
python run.py
```

然后在提示时选择`y`进行打包。打包完成后，应用将位于`dist/SpaceTrans.app`目录。

**注意**：打包的应用程序不包含配置文件，这是为了保护你的API密钥等敏感信息。首次运行打包后的应用程序时，系统会自动在用户主目录下的`~/.spacetrans/`文件夹中创建新的配置文件，并提示你输入必要的配置信息。

2. 在任意文本输入框中选中需要翻译的文本

3. 连续按下三次空格键触发翻译

4. 选中的文本将被翻译结果自动替换

5. 按下`Esc`键退出程序

## 注意事项

- 本程序需要访问辅助功能权限才能监听键盘输入
- 首次运行时，macOS可能会提示允许访问权限
- 需要有效的API密钥才能使用翻译功能
- 连续空格的超时时间默认为0.5秒，可在代码中调整

## 自定义配置

你可以在用户主目录下的`~/.spacetrans/config.json`文件中修改以下参数来自定义程序行为：

```json
{
    "API_KEY": "你的API密钥",
    "API_HOST": "https://api.siliconflow.cn",
    "MODEL": "THUDM/GLM-4.1V-9B-Thinking",
    "SPACE_TIMEOUT": 0.5,
    "SPACE_TRIGGER_COUNT": 3,
    "TEMPERATURE": 0.3,
    "SYSTEM_PROMPT": "你是一个专业的翻译助手，请将用户输入的文本翻译成中文或英文（根据输入文本的语言自动判断）。只返回翻译结果，不要有任何解释或额外内容。"
}
```

- `API_KEY`：你的API密钥
- `API_HOST`：API服务域名
- `MODEL`：使用的AI模型
- `SPACE_TIMEOUT`：连续空格的超时时间（秒）
- `SPACE_TRIGGER_COUNT`：触发翻译的连续空格次数
- `TEMPERATURE`：翻译结果的随机性（0-1之间，越低越精确）
- `SYSTEM_PROMPT`：系统提示词，用于指导AI如何翻译

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交问题和改进建议！