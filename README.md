# 发货助手 Android版

基于Kivy框架开发的Android发货软件，移植自Windows版本。

## 功能特性

- ✅ 发货模板管理
- ✅ 散装激活码批量处理
- ✅ 30天/90天/365天激活码随机选择
- ✅ 文件导入功能（支持TXT/DOCX）
- ✅ 剪贴板操作
- ✅ 触摸友好的移动端界面
- ✅ 自动文本格式化

## 环境要求

### 开发环境
- Python 3.8+
- Kivy 2.0+
- Buildozer（用于打包APK）

### Android设备要求
- Android 5.0+ (API 21+)
- 存储权限（用于读取激活码文件）

## 安装依赖

```bash
# 安装Python依赖
pip install kivy[base] python-docx

# 安装Buildozer（用于打包APK）
pip install buildozer
```

## 开发测试

在桌面端测试运行：

```bash
cd android
python main.py
```

## 打包APK

1. 确保已安装Android SDK和NDK
2. 配置buildozer.spec文件中的路径
3. 执行打包命令：

```bash
cd android
buildozer android debug
```

生成的APK文件在 `bin/` 目录下。

## 文件结构

```
android/
├── main.py              # 主程序文件
├── shipping.kv          # Kivy界面布局文件
├── buildozer.spec       # 构建配置文件
├── README.md            # 说明文档
└── data/               # 数据文件目录（需要手动创建）
    ├── sendGoodsMode.txt    # 发货模板
    ├── code30day.txt        # 30天激活码
    ├── code90day.txt        # 90天激活码
    ├── code365day.txt       # 365天激活码
    └── code1day.txt         # 1天激活码
```

## 使用说明

### 首次使用

1. 安装APK到Android设备
2. 将激活码文件复制到设备存储的 `ShippingApp` 目录下：
   - `sendGoodsMode.txt` - 发货模板
   - `code30day.txt` - 30天激活码（每行一个）
   - `code90day.txt` - 90天激活码
   - `code365day.txt` - 365天激活码
   - `code1day.txt` - 1天激活码

### 主要功能

1. **发货**：加载默认发货模板
2. **散装**：批量显示30天和1天激活码
3. **30天/90天/365天**：随机选择对应天数的激活码
4. **导入文件**：从设备存储导入TXT或DOCX文件
5. **复制内容**：将当前内容复制到剪贴板
6. **清空**：清除当前内容

### 文件格式

激活码文件格式（每行一个激活码）：
```
ABCD1234EFGH
IJKL5678MNOP
QRST9012UVWX
```

## 权限说明

应用需要以下权限：
- **存储权限**：读取激活码文件和导入文档
- **网络权限**：未来版本可能需要（当前版本不使用）

## 故障排除

### 常见问题

1. **激活码不显示**
   - 检查激活码文件是否存在于正确目录
   - 确认文件编码为UTF-8
   - 检查文件权限

2. **导入DOCX失败**
   - 确认已安装python-docx库
   - 检查DOCX文件是否损坏

3. **复制功能不工作**
   - 检查剪贴板权限
   - 重启应用

### 调试模式

如果遇到问题，可以使用调试版本：

```bash
buildozer android debug
adb logcat | grep python
```

## 版本历史

- **v1.0** - 初始版本
  - 基本发货功能
  - 激活码管理
  - 文件导入
  - 剪贴板操作

## 技术支持

如有问题，请检查：
1. Android版本兼容性
2. 存储权限设置
3. 文件路径和格式
4. 应用日志信息
