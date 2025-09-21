# 发货助手 Android版 - 安装指南

## 🚀 快速开始

### 方法一：直接使用APK（推荐）

1. **下载APK**：从构建好的APK文件安装
2. **安装到手机**：
   - 开启"未知来源"应用安装权限
   - 安装APK文件
3. **准备数据文件**：将激活码文件复制到手机存储的 `ShippingApp` 文件夹

### 方法二：自己构建APK

#### 环境准备

1. **安装Python 3.8+**
2. **安装依赖**：
   ```bash
   pip install buildozer kivy[base] python-docx
   ```

3. **Android SDK（可选）**：
   - Buildozer可以自动下载SDK
   - 或手动安装Android Studio

#### 构建步骤

1. **进入目录**：
   ```bash
   cd sendGoods/android
   ```

2. **自动构建**：
   ```bash
   python build_apk.py
   ```
   
   或手动构建：
   ```bash
   buildozer android debug
   ```

3. **等待完成**（首次构建需要10-30分钟）

## 📱 手机端设置

### 1. 创建数据文件夹

在手机存储根目录创建 `ShippingApp` 文件夹：
```
/sdcard/ShippingApp/
├── sendGoodsMode.txt
├── code30day.txt
├── code90day.txt
├── code365day.txt
└── code1day.txt
```

### 2. 复制激活码文件

将PC端的以下文件复制到手机：
- `sendGoodsMode.txt` - 发货模板
- `code30day.txt` - 30天激活码
- `code90day.txt` - 90天激活码  
- `code365day.txt` - 365天激活码
- `code1day.txt` - 1天激活码

### 3. 文件格式

激活码文件格式（每行一个激活码）：
```
ABCD1234EFGH
IJKL5678MNOP
QRST9012UVWX
...
```

## 🔧 桌面测试

在PC上测试Android版本：

### Windows
```bash
# 方法1：使用批处理
双击 "测试运行.bat"

# 方法2：命令行
python run_test.py
```

### Linux/Mac
```bash
python3 run_test.py
```

## 📋 功能说明

| 按钮 | 功能 | 说明 |
|------|------|------|
| 发货 | 加载发货模板 | 从sendGoodsMode.txt加载 |
| 散装 | 批量激活码 | 显示30天+1天激活码 |
| 30天 | 30天激活码 | 随机选择一个30天码 |
| 90天 | 90天激活码 | 随机选择一个90天码 |
| 365天 | 365天激活码 | 随机选择一个365天码 |
| 导入文件 | 导入文档 | 支持TXT/DOCX格式 |
| 复制内容 | 复制到剪贴板 | 可粘贴到QQ等应用 |
| 清空 | 清除内容 | 清空编辑区 |

## ❓ 常见问题

### Q: APK安装失败？
A: 检查以下设置：
- 开启"未知来源"应用安装
- 关闭"Play保护机制"
- 确认Android版本5.0+

### Q: 激活码不显示？
A: 检查以下问题：
- 数据文件是否在正确位置
- 文件编码是否为UTF-8
- 应用是否有存储权限

### Q: 导入DOCX失败？
A: DOCX功能依赖python-docx库，如果APK中未包含该库，只能导入TXT文件

### Q: 复制功能不工作？
A: 检查应用权限设置，确保允许访问剪贴板

### Q: 构建APK失败？
A: 常见原因：
- 网络问题（buildozer需要下载依赖）
- 磁盘空间不足（需要5GB+）
- Android SDK配置问题

## 🛠️ 故障排除

### 构建问题
```bash
# 清理构建缓存
buildozer android clean

# 查看详细日志
buildozer android debug -v

# 更新buildozer
pip install --upgrade buildozer
```

### 运行时问题
```bash
# 查看Android日志
adb logcat | grep python

# 重新安装APK
adb install -r your_app.apk
```

## 📞 技术支持

如遇问题：
1. 查看本文档的常见问题
2. 检查Android设备兼容性
3. 确认数据文件格式正确
4. 查看应用权限设置

---

**提示**：首次使用建议先在PC上测试功能，确认无误后再构建APK。
