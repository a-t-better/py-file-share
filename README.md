# PyFileShare - 内网文件传输工具

一个高性能、可配置的 Python 内网文件传输工具，支持大文件传输、断点续传、加密传输等功能。

## 功能特性

- ✅ **大文件传输**：支持 GB 级文件传输，采用流式处理
- ✅ **断点续传**：中断后可继续传输，无需重新开始
- ✅ **加密传输**：支持 TLS/SSL 加密传输
- ✅ **多协议支持**：HTTP/HTTPS、TCP Socket
- ✅ **灵活配置**：YAML/JSON 配置文件支持
- ✅ **进度跟踪**：实时显示传输进度和速度
- ✅ **并发传输**：支持多并发下载和上传
- ✅ **身份验证**：支持 API Key 和基础认证
- ✅ **日志系统**：详细的日志记录和调试模式
- ✅ **CLI 工具**：方便的命令行界面

## 项目结构

```
py-file-share/
├── pyfileshare/              # 主包
│   ├── __init__.py
│   ├── config/              # 配置管理
│   │   ├── __init__.py
│   │   ├── config.py        # 配置类
│   │   └── defaults.py      # 默认配置
│   ├── server/              # 服务器实现
│   │   ├── __init__.py
│   │   ├── http_server.py   # HTTP 服务器
│   │   ├── tcp_server.py    # TCP Socket 服务器
│   │   └── handlers.py      # 请求处理器
│   ├── client/              # 客户端实现
│   │   ├── __init__.py
│   │   ├── http_client.py   # HTTP 客户端
│   │   ├── tcp_client.py    # TCP Socket 客户端
│   │   └── progress.py      # 进度跟踪
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── transfer.py      # 传输管理
│   │   ├── crypto.py        # 加密功能
│   │   ├── storage.py       # 存储管理
│   │   └── utils.py         # 工具函数
│   └── cli/                 # CLI 工具
│       ├── __init__.py
│       ├── cli.py           # CLI 入口
│       └── commands.py      # 命令实现
├── config/                  # 配置文件目录
│   ├── server.yaml          # 服务器配置
│   ├── client.yaml          # 客户端配置
│   └── defaults.yaml        # 默认配置
├── tests/                   # 测试
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_transfer.py
│   └── test_crypto.py
├── examples/                # 示例
│   ├── server_example.py
│   └── client_example.py
├── requirements.txt         # 依赖
├── setup.py                 # 安装脚本
└── README.md               # 本文件
```

## 安装

```bash
# 克隆项目
git clone https://github.com/a-t-better/py-file-share.git
cd py-file-share

# 安装依赖
pip install -r requirements.txt

# 安装本包
pip install -e .
```

## 快速开始

### 启动服务器

```bash
# 使用默认配置
pyfileshare server start

# 使用自定义配置
pyfileshare server start --config config/server.yaml
```

### 上传文件

```bash
# HTTP 上传
pyfileshare client upload -f /path/to/file -s http://localhost:8080

# TCP 上传
pyfileshare client upload -f /path/to/file -s localhost:9090 --protocol tcp
```

### 下载文件

```bash
# HTTP 下载
pyfileshare client download -r /remote/file -d /path/to/save -s http://localhost:8080

# TCP 下载
pyfileshare client download -r /remote/file -d /path/to/save -s localhost:9090 --protocol tcp
```

## 配置

### 服务器配置 (config/server.yaml)

```yaml
server:
  # HTTP 服务器配置
  http:
    enabled: true
    host: 0.0.0.0
    port: 8080
    ssl:
      enabled: false
      cert_path: /path/to/cert.pem
      key_path: /path/to/key.pem
  
  # TCP 服务器配置
  tcp:
    enabled: true
    host: 0.0.0.0
    port: 9090
    ssl: false
  
  # 存储配置
  storage:
    upload_dir: ./uploads
    max_file_size: 10GB
    cleanup_incomplete: true
    cleanup_timeout: 86400

# 身份验证
auth:
  enabled: true
  api_key: "your-secret-key"
  require_token: true

# 日志配置
logging:
  level: INFO
  file: logs/server.log
  max_size: 100MB
  backup_count: 10

# 传输配置
transfer:
  chunk_size: 4MB
  max_connections: 100
  timeout: 3600
  resume_enabled: true
```

### 客户端配置 (config/client.yaml)

```yaml
client:
  # 默认服务器地址
  default_server: http://localhost:8080
  
  # 传输配置
  transfer:
    chunk_size: 4MB
    max_workers: 4
    timeout: 3600
    retry_count: 3
  
  # 进度显示
  progress:
    show_progress: true
    refresh_rate: 1
    show_speed: true

# 日志配置
logging:
  level: INFO
  file: logs/client.log
```

## 使用示例

### Python API

```python
from pyfileshare.client import FileShareClient
from pyfileshare.config import ClientConfig

# 创建客户端
config = ClientConfig.from_yaml('config/client.yaml')
client = FileShareClient(config)

# 上传文件
result = client.upload(
    local_path='/path/to/large_file.zip',
    remote_path='/backups/large_file.zip',
    show_progress=True
)
print(f"Upload completed: {result}")

# 下载文件
result = client.download(
    remote_path='/backups/large_file.zip',
    local_path='/downloads/large_file.zip',
    show_progress=True
)
print(f"Download completed: {result}")
```

## 性能指标

- **传输速度**：取决于网络和磁盘性能
- **并发连接**：支持100+并发连接
- **内存占用**：恒定内存占用（流式处理）
- **大文件支持**：理论上支持无限大文件

## 安全特性

- TLS/SSL 加密传输
- API Key 身份验证
- 文件完整性验证 (MD5/SHA256)
- 请求签名验证
- 访问控制列表 (ACL)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- GitHub: [@a-t-better](https://github.com/a-t-better)
