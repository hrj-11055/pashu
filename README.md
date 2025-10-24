# 豆瓣书单爬虫 📚

一个功能强大的Python爬虫，用于爬取豆瓣书单中的所有书籍信息，并生成带封面的Excel文件。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## ✨ 功能特色

- 🚀 **批量爬取**：支持爬取书单中的所有书籍（已测试492本）
- 📊 **多格式输出**：支持CSV、JSON、Excel三种格式
- 🖼️ **封面下载**：自动下载并优化书籍封面图片
- 📋 **Excel集成**：在Excel中直接显示书籍封面
- 🔄 **智能分页**：自动处理多页书单
- ⚡ **错误处理**：完善的异常处理和重试机制
- 🎯 **数据完整**：包含书名、作者、出版社、评分、链接等完整信息

## 📦 安装依赖

### 1. 克隆项目
```bash
git clone https://github.com/hrj-11055/pashu.git
cd pashu
```

### 2. 创建虚拟环境
```bash
python3 -m venv douban_env
source douban_env/bin/activate  # Linux/Mac
# 或
douban_env\Scripts\activate  # Windows
```

### 3. 安装依赖包
```bash
pip install -r requirements.txt
```

## 🚀 快速开始

### 基础使用
```bash
# 运行增强版爬虫
python enhanced_douban_spider.py
```

### 自定义书单
修改脚本中的URL：
```python
doulist_url = "https://www.douban.com/doulist/45298673/?start=0&sort=seq&playable=0&sub_type="
```

## 📁 项目结构

```
pashu/
├── enhanced_douban_spider.py    # 增强版爬虫（推荐）
├── create_excel_simple.py       # Excel文件生成器
├── working_douban_spider.py     # 基础版爬虫
├── requirements.txt             # 依赖包列表
├── README.md                    # 项目说明
├── douban_books_all.csv         # 爬取结果（CSV）
├── douban_books_all.json        # 爬取结果（JSON）
├── douban_books_with_covers.xlsx # 完整数据Excel文件
├── douban_books_sample_with_covers.xlsx # 带封面示例Excel
└── book_covers/                 # 封面图片文件夹
    ├── cover_1_如何阅读一本书.jpg
    ├── cover_2_少有人走的路.jpg
    └── ...
```

## 📊 输出数据格式

### CSV格式
```csv
书名,作者,出版社,评分,封面链接,书籍链接
如何阅读一本书,[美] 莫提默·J. 艾德勒 / 查尔斯·范多伦,商务印书馆,8.3,https://img1.doubanio.com/...,https://book.douban.com/subject/1013208/
```

### JSON格式
```json
[
  {
    "书名": "如何阅读一本书",
    "作者": "[美] 莫提默·J. 艾德勒 / 查尔斯·范多伦",
    "出版社": "商务印书馆",
    "评分": "8.3",
    "封面链接": "https://img1.doubanio.com/...",
    "书籍链接": "https://book.douban.com/subject/1013208/"
  }
]
```

### Excel格式
- 包含所有书籍信息
- 支持封面图片显示
- 自动调整列宽和行高
- 可直接用Microsoft Excel打开

## 🎯 使用示例

### 爬取指定书单
```python
from enhanced_douban_spider import crawl_all_douban_books

# 目标书单URL
url = "https://www.douban.com/doulist/45298673/?start=0&sort=seq&playable=0&sub_type="

# 爬取书籍数据
books_data = crawl_all_douban_books(url, max_pages=20)

# 保存数据
import pandas as pd
df = pd.DataFrame(books_data)
df.to_csv('my_books.csv', index=False, encoding='utf-8-sig')
```

### 生成Excel文件
```python
from create_excel_simple import create_excel_from_data

# 从已爬取数据生成Excel
excel_file = create_excel_from_data()
print(f"Excel文件已生成: {excel_file}")
```

## 📈 性能统计

- **爬取速度**: 约25本书/页，2秒/页延时
- **成功率**: 99%+ 数据完整性
- **支持规模**: 已测试492本书籍
- **文件大小**: Excel文件约45KB，CSV文件约84KB

## ⚠️ 注意事项

1. **遵守网站规则**: 请遵守豆瓣网站的robots.txt规则和使用条款
2. **合理使用**: 程序已内置2秒延时，请勿修改为更短时间
3. **网络环境**: 确保网络连接稳定
4. **存储空间**: Excel文件可能较大，请确保有足够空间
5. **反爬虫**: 如遇到限制，可能需要调整请求头或使用代理

## 🔧 技术栈

- **Python 3.8+**
- **requests**: HTTP请求处理
- **BeautifulSoup**: HTML解析
- **pandas**: 数据处理
- **openpyxl**: Excel文件操作
- **Pillow**: 图片处理

## 📝 更新日志

### v1.0.0 (2024-10-25)
- ✨ 初始版本发布
- 🚀 支持基础爬取功能
- 📊 支持CSV和JSON输出

### v1.1.0 (2024-10-25)
- ✨ 添加Excel输出支持
- 🖼️ 实现封面图片下载
- 🔄 支持多页爬取

### v1.2.0 (2024-10-25)
- ✨ 在Excel中嵌入封面图片
- 🎯 优化错误处理机制
- 📈 提升爬取成功率

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢豆瓣网提供的数据源
- 感谢所有开源库的贡献者
- 感谢使用本项目的用户反馈

## 📞 联系方式

- 项目链接: [https://github.com/hrj-11055/pashu](https://github.com/hrj-11055/pashu)
- 问题反馈: [Issues](https://github.com/hrj-11055/pashu/issues)

---

⭐ 如果这个项目对您有帮助，请给它一个星标！