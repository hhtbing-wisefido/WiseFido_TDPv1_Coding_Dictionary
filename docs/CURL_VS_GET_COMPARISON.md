# 🔍 详解：`curl` vs `GET` 命令的区别

## 📌 核心区别总结

| 命令 | 本质 | 环境 | 返回类型 | 推荐场景 |
|------|------|------|----------|----------|
| `curl` (PowerShell) | `Invoke-WebRequest` 别名 | ⚠️ 仅 PowerShell | PowerShell 对象 | PowerShell 脚本 |
| `curl.exe` | 真正的 curl 工具 | ✅ 所有平台 | 纯文本 | 通用 HTTP 测试 |
| `GET` | `Invoke-WebRequest` 别名 | ⚠️ 仅 PowerShell | PowerShell 对象 | PowerShell 脚本 |
| `Invoke-RestMethod` | PowerShell 原生 cmdlet | ⚠️ 仅 PowerShell | 自动解析对象 | ✅ **API 测试最佳** |

---

## 1️⃣ `curl` 在 PowerShell 中的混淆

### ⚠️ **重要：PowerShell 中的 `curl` 不是真正的 curl！**

在 PowerShell 中：
```powershell
curl http://localhost:8080/api/health
```

**实际执行的是：**
```powershell
Invoke-WebRequest -Uri "http://localhost:8080/api/health"
```

**验证：**
```powershell
Get-Alias curl

# 输出:
# CommandType     Name
# -----------     ----
# Alias           curl -> Invoke-WebRequest
```

### ✅ 如何使用真正的 curl

Windows 10 1803+ 自带真正的 curl.exe：

```powershell
# 方法 1: 显式调用 curl.exe
curl.exe http://localhost:8080/api/health

# 方法 2: 移除别名后使用
Remove-Item alias:curl
curl http://localhost:8080/api/health
```

---

## 2️⃣ 真正的 `curl.exe`

### 📦 什么是 curl？

**cURL** = **Client URL**
- 起源于 1997 年，作者 Daniel Stenberg
- 跨平台的命令行工具和库
- 支持 20+ 协议（HTTP、HTTPS、FTP、SMTP、LDAP 等）
- 在 Linux/macOS 中是标准工具
- Windows 10 1803+ 内置于 `C:\Windows\system32\curl.exe`

### 🎯 特点

#### ✅ 优点
- **通用性强**：文档、教程最多
- **跨平台**：Linux、macOS、Windows 一致
- **功能强大**：支持认证、代理、cookies、证书等
- **轻量快速**：纯命令行，无依赖

#### ⚠️ 缺点
- **返回纯文本**：需要手动解析 JSON
- **语法相对复杂**：参数多，需要记忆

### 📖 常用示例

```bash
# 基本 GET 请求（默认）
curl.exe http://localhost:8080/api/health

# 显示详细信息（包括响应头）
curl.exe -i http://localhost:8080/api/health

# 只显示响应头
curl.exe -I http://localhost:8080/api/health

# POST 请求发送 JSON
curl.exe -X POST http://localhost:8080/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"test","value":123}'

# 发送文件
curl.exe -X POST http://localhost:8080/upload \
  -F "file=@data.json"

# 下载文件
curl.exe -o output.json http://localhost:8080/api/export

# 跟随重定向
curl.exe -L http://localhost:8080/redirect

# 使用代理
curl.exe -x http://proxy:8080 http://localhost:8080/api/health

# 添加认证
curl.exe -u username:password http://localhost:8080/api/protected

# 忽略 SSL 证书验证（测试用）
curl.exe -k https://localhost:8443/api/health

# 静默模式（不显示进度）
curl.exe -s http://localhost:8080/api/health

# 保存 cookies
curl.exe -c cookies.txt http://localhost:8080/login

# 使用 cookies
curl.exe -b cookies.txt http://localhost:8080/api/user
```

---

## 3️⃣ PowerShell 的 `GET` 别名

### 📦 什么是 GET？

在 PowerShell 中，`GET` 是 `Invoke-WebRequest` 的**别名**：

```powershell
Get-Alias GET

# 输出:
# CommandType     Name
# -----------     ----
# Alias           GET -> Invoke-WebRequest
```

### 🎯 特点

#### ✅ 优点
- **简洁**：只需 `GET http://url`
- **返回对象**：可访问 StatusCode、Headers、Content 等属性
- **易于处理**：PowerShell 原生对象

#### ⚠️ 缺点
- **仅 PowerShell**：在 Bash、CMD 中不可用
- **需要参数**：某些情况需加 `-UseBasicParsing`
- **不如专用命令**：API 测试应用 `Invoke-RestMethod`

### 📖 使用示例

```powershell
# 基本用法（可能需要 -UseBasicParsing）
GET http://localhost:8080/api/health -UseBasicParsing

# 访问响应属性
$response = GET http://localhost:8080/api/health -UseBasicParsing
$response.StatusCode          # 200
$response.StatusDescription   # OK
$response.Headers            # 响应头字典
$response.Content            # 响应体（字符串）

# 解析 JSON
$data = $response.Content | ConvertFrom-Json
$data.status                 # "healthy"

# POST 请求
$body = @{
    name = "test"
    value = 123
} | ConvertTo-Json

POST http://localhost:8080/api/data `
  -ContentType "application/json" `
  -Body $body `
  -UseBasicParsing
```

---

## 4️⃣ PowerShell 的 `Invoke-RestMethod` ⭐

### 📦 什么是 Invoke-RestMethod？

PowerShell 专门用于 **RESTful API** 的 cmdlet。

### 🎯 特点

#### ✅ 优点（⭐ 最推荐用于 API 测试）
- **自动解析 JSON**：无需 `ConvertFrom-Json`
- **返回对象**：直接访问属性
- **最简洁**：API 测试最方便
- **支持管道**：易于数据处理

#### ⚠️ 缺点
- **仅 PowerShell**：跨平台需要 PowerShell Core
- **无响应头**：默认只返回内容（可用 `-ResponseHeadersVariable` 获取）

### 📖 使用示例

```powershell
# 基本 GET 请求（自动解析 JSON）
$data = Invoke-RestMethod -Uri "http://localhost:8080/api/health"
$data.status                 # 直接访问！无需 ConvertFrom-Json

# 简写形式
$data = irm http://localhost:8080/api/health  # irm 是别名

# POST 请求
$body = @{
    name = "test"
    value = 123
}

Invoke-RestMethod -Uri "http://localhost:8080/api/data" `
  -Method POST `
  -ContentType "application/json" `
  -Body ($body | ConvertTo-Json)

# 获取响应头
Invoke-RestMethod -Uri "http://localhost:8080/api/health" `
  -ResponseHeadersVariable headers
$headers

# 分页查询示例
$result = Invoke-RestMethod -Uri "http://localhost:8080/api/entries?limit=10"
$result.total                # 总数
$result.results.Count        # 返回的数量
$result.results[0].display   # 第一条的名称

# 搜索并过滤
$results = Invoke-RestMethod -Uri "http://localhost:8080/api/search?q=walking"
$results.results | Where-Object { $_.system -like "*snomed*" } | 
  Select-Object display, display_zh
```

---

## 5️⃣ 实际对比演示

### 测试端点：`http://localhost:8080/api/health`

#### 方法 1: curl.exe（真正的 curl）
```powershell
curl.exe http://localhost:8080/api/health
```
**输出（纯文本）：**
```json
{"status":"healthy","version":"1.0.0","total_entries":79,"timestamp":"2025-11-13T17:00:00.000000"}
```

#### 方法 2: Invoke-WebRequest（或别名 curl/GET）
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8080/api/health" -UseBasicParsing
$response.StatusCode  # 200
$response.Content     # JSON 字符串
```
**输出（需要手动解析）：**
```powershell
StatusCode        : 200
StatusDescription : OK
Content           : {"status":"healthy",...}
```

#### 方法 3: Invoke-RestMethod ⭐（推荐）
```powershell
$data = Invoke-RestMethod -Uri "http://localhost:8080/api/health"
$data.status          # "healthy"
$data.total_entries   # 79
```
**输出（自动解析为对象）：**
```
status         : healthy
version        : 1.0.0
total_entries  : 79
timestamp      : 2025-11-13T17:00:00.000000
```

---

## 6️⃣ 选择指南

### 🎯 使用场景推荐

| 场景 | 推荐命令 | 原因 |
|------|----------|------|
| **跨平台脚本** | `curl.exe` 或 `curl` (非 PS) | 通用性最强 |
| **Linux/Mac 环境** | `curl` | 系统自带 |
| **Windows CMD** | `curl.exe` | CMD 无其他选择 |
| **PowerShell 脚本** | `Invoke-RestMethod` | 最方便，自动解析 |
| **需要响应头** | `Invoke-WebRequest` | 完整响应信息 |
| **快速测试 API** | `Invoke-RestMethod` | 最快速 |
| **调试 HTTP** | `curl.exe -v` | 详细输出 |
| **下载文件** | `curl.exe -o` 或 `Invoke-WebRequest -OutFile` | 都支持 |
| **复杂认证** | `curl.exe` | 选项最丰富 |

---

## 7️⃣ 快速参考

### curl.exe 常用参数
```bash
-X, --request <method>    # 指定 HTTP 方法（GET, POST, PUT, DELETE）
-H, --header <header>     # 添加请求头
-d, --data <data>         # 发送数据（POST）
-i, --include            # 包含响应头
-I, --head               # 只显示响应头
-o, --output <file>      # 保存到文件
-s, --silent             # 静默模式
-v, --verbose            # 详细模式
-u, --user <user:pass>   # 认证
-x, --proxy <proxy>      # 使用代理
-k, --insecure           # 忽略 SSL 验证
-L, --location           # 跟随重定向
```

### Invoke-RestMethod 常用参数
```powershell
-Uri <string>                    # 目标 URL
-Method <WebRequestMethod>       # HTTP 方法（Get, Post, Put, Delete）
-Headers <hashtable>             # 请求头
-Body <object>                   # 请求体
-ContentType <string>            # Content-Type
-ResponseHeadersVariable <var>   # 保存响应头到变量
-OutFile <path>                  # 保存到文件
-MaximumRedirection <int>        # 最大重定向次数
-Credential <PSCredential>       # 认证凭据
-Proxy <Uri>                     # 代理
```

---

## 8️⃣ 常见问题

### Q1: PowerShell 中 `curl` 报错怎么办？
```powershell
curl : 无法分析响应内容，因为 Internet Explorer 引擎不可用...
```

**解决方案：**
```powershell
# 方案 1: 加 -UseBasicParsing
curl -UseBasicParsing http://localhost:8080/api/health

# 方案 2: 使用真正的 curl.exe
curl.exe http://localhost:8080/api/health

# 方案 3: 使用 Invoke-RestMethod（推荐）
Invoke-RestMethod http://localhost:8080/api/health
```

### Q2: 如何在 PowerShell 中禁用 curl 别名？
```powershell
# 临时移除（当前会话）
Remove-Item alias:curl

# 永久配置（添加到 $PROFILE）
if (Test-Path alias:curl) { Remove-Item alias:curl }
```

### Q3: 如何美化 JSON 输出？

**curl.exe:**
```bash
curl.exe http://localhost:8080/api/health | jq .
# 或在 PowerShell 中
curl.exe http://localhost:8080/api/health | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Invoke-RestMethod:**
```powershell
Invoke-RestMethod http://localhost:8080/api/health | ConvertTo-Json -Depth 10
```

---

## 9️⃣ 总结建议

### ✅ 最佳实践

1. **在你的 WiseFido 项目中：**
   ```powershell
   # 推荐：使用 Invoke-RestMethod
   Invoke-RestMethod http://localhost:8080/api/health
   Invoke-RestMethod http://localhost:8080/api/stats
   Invoke-RestMethod "http://localhost:8080/api/search?q=walking"
   ```

2. **在文档中提供跨平台命令：**
   ```bash
   # Linux/Mac/Windows（通用）
   curl http://localhost:8080/api/health
   
   # PowerShell（推荐）
   Invoke-RestMethod http://localhost:8080/api/health
   ```

3. **在 CI/CD 脚本中：**
   ```bash
   # 使用 curl（最通用）
   curl -f http://localhost:8080/api/health || exit 1
   ```

---

## 🎓 学习资源

- **curl 官方文档**: https://curl.se/docs/
- **PowerShell 文档**: https://docs.microsoft.com/powershell/
- **HTTP 协议**: https://developer.mozilla.org/docs/Web/HTTP

---

**最后建议**：在你的项目中，为了测试 API，使用 `Invoke-RestMethod` 是最方便的！ 🚀
