"""
快速测试脚本 - 诊断 API 问题
"""
import json
from pathlib import Path

# 测试1: 检查数据文件
print("=" * 70)
print("测试1: 检查数据文件")
print("=" * 70)

data_file = Path(__file__).parent / "coding_dictionary" / "coding_dictionary.json"
print(f"数据文件路径: {data_file}")
print(f"文件存在: {data_file.exists()}")

if data_file.exists():
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 数据加载成功")
        print(f"   词条数量: {len(data)}")
        print(f"   数据类型: {type(data)}")
        if data:
            print(f"   第一条数据: {json.dumps(data[0], ensure_ascii=False, indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
else:
    print("❌ 数据文件不存在")

# 测试2: 测试类型转换
print("\n" + "=" * 70)
print("测试2: 测试 Pydantic 模型转换")
print("=" * 70)

try:
    from pydantic import BaseModel, Field
    from typing import Optional, List, Dict, Any
    
    class CodingEntry(BaseModel):
        code: str = Field(..., description="编码值")
        system: str = Field(..., description="编码系统 URI")
        display: str = Field(..., description="英文名称")
        display_zh: str = Field(..., description="中文名称")
        id: Optional[str] = Field(None, description="词条唯一标识符")
        category: Optional[str] = Field(None, description="分类")
        status: Optional[str] = Field(None, description="状态")
        version: Optional[str] = Field(None, description="版本号")
        description: Optional[str] = Field(None, description="英文描述")
        description_zh: Optional[str] = Field(None, description="中文描述")
        synonyms: Optional[List[str]] = Field(None, description="英文同义词")
        synonyms_zh: Optional[List[str]] = Field(None, description="中文同义词")
        source_refs: Optional[List[Any]] = Field(None, description="来源参考")
        detection: Optional[Dict[str, Any]] = Field(None, description="检测能力信息")
    
    if data:
        # 尝试转换第一条数据
        test_entry = CodingEntry(**data[0])
        print(f"✅ 模型转换成功")
        print(f"   转换后类型: {type(test_entry)}")
        print(f"   code: {test_entry.code}")
        print(f"   display_zh: {test_entry.display_zh}")
        
        # 测试批量转换
        entries = [CodingEntry(**item) for item in data[:3]]
        print(f"✅ 批量转换成功 (前3条)")
        print(f"   列表类型: {type(entries)}")
        print(f"   列表长度: {len(entries)}")
        
except Exception as e:
    print(f"❌ 模型转换失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3: 测试配置导入
print("\n" + "=" * 70)
print("测试3: 测试配置导入")
print("=" * 70)

import sys
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

try:
    from _config import DICTIONARY_FILE, VALID_CATEGORIES, VALID_STATUSES
    print(f"✅ 配置导入成功")
    print(f"   DICTIONARY_FILE: {DICTIONARY_FILE}")
    print(f"   VALID_CATEGORIES: {VALID_CATEGORIES}")
except ImportError as e:
    print(f"⚠️  配置导入失败 (使用默认值): {e}")
    DICTIONARY_FILE = Path(__file__).parent / "coding_dictionary" / "coding_dictionary.json"
    VALID_CATEGORIES = ["观察类", "操作类", "干预类", "状态类", "实体类", "其他"]
    print(f"   使用默认 DICTIONARY_FILE: {DICTIONARY_FILE}")

print("\n" + "=" * 70)
print("诊断完成!")
print("=" * 70)
