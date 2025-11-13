"""
WiseFido 医疗编码字典 Web API
提供 REST API 查询服务，基于现有的 dic_tools.py 实现
"""
import json
import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# ========== 依赖检查与自动安装 ==========
def check_and_install_dependencies():
    """检查并自动安装缺失的依赖"""
    required_packages = {
        'fastapi': 'fastapi>=0.109.0',
        'uvicorn': 'uvicorn>=0.27.0',  # 简化版本，避免 [standard] 在某些环境下的问题
        'pydantic': 'pydantic>=2.5.0'
    }
    
    missing_packages = []
    
    # 检查每个包
    for package_name, package_spec in required_packages.items():
        try:
            __import__(package_name)
        except ImportError:
            missing_packages.append(package_spec)
    
    # 如果有缺失的包，自动安装
    if missing_packages:
        print("\n" + "=" * 70)
        print("  ⚠️  检测到缺失的依赖包")
        print("=" * 70)
        print(f"\n缺失的包: {', '.join(missing_packages)}")
        print("\n[INFO] 正在自动安装（这可能需要 30-60 秒）...")
        print("[提示] 如果安装时间过长，可按 Ctrl+C 取消并手动安装\n")
        
        try:
            # 使用当前 Python 解释器安装，显示输出
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install"] + missing_packages,
                capture_output=False,
                text=True,
                check=True
            )
            print("\n[成功] ✅ 依赖包已安装完成！")
            print("\n[提示] 请重新运行脚本以加载新安装的依赖")
            print("=" * 70 + "\n")
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print("\n[失败] ❌ 自动安装失败")
            print("\n[手动安装方法]:")
            print(f"  {sys.executable} -m pip install -r requirements.txt")
            print("\n或单独安装:")
            for pkg in missing_packages:
                print(f"  {sys.executable} -m pip install {pkg}")
            print("\n" + "=" * 70 + "\n")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n[已取消] 用户中断安装")
            print("\n[手动安装方法]:")
            print(f"  {sys.executable} -m pip install -r requirements.txt")
            print("\n" + "=" * 70 + "\n")
            sys.exit(1)

# 执行依赖检查
check_and_install_dependencies()

# 导入依赖（检查通过后才会执行到这里）
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# 导入配置
from _config import DICTIONARY_FILE, VALID_CATEGORIES, VALID_STATUSES

# 创建 FastAPI 应用
app = FastAPI(
    title="WiseFido 医疗编码字典 API",
    description="提供医疗编码词条的查询、搜索、统计等服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS（允许跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 数据模型 ==========

class CodingEntry(BaseModel):
    """词条数据模型（兼容旧格式数据）"""
    # 核心字段
    code: str = Field(..., description="编码值")
    system: str = Field(..., description="编码系统 URI")
    display: str = Field(..., description="英文名称")
    display_zh: str = Field(..., description="中文名称")
    
    # 可选字段（旧数据可能没有）
    id: Optional[str] = Field(None, description="词条唯一标识符")
    category: Optional[str] = Field(None, description="分类")
    status: Optional[str] = Field(None, description="状态（active/deprecated/draft）")
    version: Optional[str] = Field(None, description="版本号")
    description: Optional[str] = Field(None, description="英文描述")
    description_zh: Optional[str] = Field(None, description="中文描述")
    synonyms: Optional[List[str]] = Field(None, description="英文同义词")
    synonyms_zh: Optional[List[str]] = Field(None, description="中文同义词")
    source_refs: Optional[List[Any]] = Field(None, description="来源参考")
    detection: Optional[Dict[str, Any]] = Field(None, description="检测能力信息")

class StatsResponse(BaseModel):
    """统计信息响应模型"""
    total: int = Field(..., description="总词条数")
    categories: Dict[str, int] = Field(..., description="分类分布")
    statuses: Dict[str, int] = Field(..., description="状态分布")
    systems: Dict[str, int] = Field(..., description="编码系统分布")
    detection_stats: Dict[str, int] = Field(..., description="检测能力统计")
    last_updated: str = Field(..., description="数据最后更新时间")

class SearchResult(BaseModel):
    """搜索结果模型"""
    total: int = Field(..., description="匹配结果总数")
    results: List[CodingEntry] = Field(..., description="词条列表")

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    total_entries: int
    timestamp: str

# ========== 辅助函数 ==========

def load_dictionary() -> List[Dict]:
    """加载词典数据"""
    try:
        with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("词典数据格式错误：根节点必须是数组")
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"词典文件不存在: {DICTIONARY_FILE}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"词典 JSON 解析失败: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载词典失败: {e}")

def get_system_category(system: str) -> str:
    """将 system URI 归类"""
    if not system:
        return "其他"
    if "snomed" in system.lower():
        return "SNOMED CT"
    elif system.startswith("internal://"):
        return "Internal"
    elif system.startswith("tdp://"):
        return "TDP"
    else:
        return "其他"

# ========== API 端点 ==========

@app.get("/", response_class=JSONResponse)
async def root():
    """根路径，返回 API 信息"""
    return {
        "name": "WiseFido 医疗编码字典 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "健康检查": "GET /api/health",
            "统计信息": "GET /api/stats",
            "查询所有词条": "GET /api/entries",
            "查询单个词条": "GET /api/entries/{entry_id}",
            "搜索词条": "GET /api/search?q={keyword}&field={field}",
            "按分类查询": "GET /api/categories/{category}",
        }
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    try:
        data = load_dictionary()
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            total_entries=len(data),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/stats", response_model=StatsResponse)
async def get_statistics():
    """获取词条统计信息"""
    data = load_dictionary()
    
    # 统计分类
    categories = {}
    statuses = {}
    systems = {}
    detection_stats = {"direct": 0, "indirect": 0, "not_detectable": 0, "未标注": 0}
    
    for item in data:
        # 分类统计
        category = item.get("category", "未知")
        categories[category] = categories.get(category, 0) + 1
        
        # 状态统计
        status = item.get("status", "未知")
        statuses[status] = statuses.get(status, 0) + 1
        
        # 编码系统统计
        system = item.get("system", "未知")
        system_cat = get_system_category(system)
        systems[system_cat] = systems.get(system_cat, 0) + 1
        
        # 检测能力统计
        detection = item.get("detection", {})
        if detection and isinstance(detection, dict):
            radar_info = detection.get("radar_60ghz", {})
            if isinstance(radar_info, dict):
                detectable = radar_info.get("detectable", "")
                if detectable in detection_stats:
                    detection_stats[detectable] += 1
                elif detectable:
                    detection_stats["未标注"] += 1
            else:
                detection_stats["未标注"] += 1
        else:
            detection_stats["未标注"] += 1
    
    # 获取文件最后修改时间
    try:
        mtime = Path(DICTIONARY_FILE).stat().st_mtime
        last_updated = datetime.fromtimestamp(mtime).isoformat()
    except:
        last_updated = "未知"
    
    return StatsResponse(
        total=len(data),
        categories=categories,
        statuses=statuses,
        systems=systems,
        detection_stats=detection_stats,
        last_updated=last_updated
    )

@app.get("/api/entries", response_model=SearchResult)
async def get_all_entries(
    skip: int = Query(0, ge=0, description="跳过前 N 条记录"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数量（最大1000）"),
    category: Optional[str] = Query(None, description="按分类过滤"),
    status: Optional[str] = Query(None, description="按状态过滤")
):
    """
    查询所有词条（支持分页和过滤）
    
    - **skip**: 跳过的记录数（用于分页）
    - **limit**: 返回的记录数（默认100，最大1000）
    - **category**: 可选，按分类过滤
    - **status**: 可选，按状态过滤
    """
    data = load_dictionary()
    
    # 过滤
    filtered = data
    if category:
        filtered = [item for item in filtered if item.get("category") == category]
    if status:
        filtered = [item for item in filtered if item.get("status") == status]
    
    # 分页
    paginated = filtered[skip:skip + limit]
    
    return SearchResult(
        total=len(filtered),
        results=paginated
    )

@app.get("/api/entries/{entry_id}", response_model=CodingEntry)
async def get_entry_by_id(entry_id: str):
    """
    根据 ID 查询单个词条
    
    - **entry_id**: 词条的唯一标识符（如 snomed:129006008）
    """
    data = load_dictionary()
    
    # 查找词条
    entry = next((item for item in data if item.get("id") == entry_id), None)
    
    if not entry:
        raise HTTPException(status_code=404, detail=f"未找到 ID 为 '{entry_id}' 的词条")
    
    return entry

@app.get("/api/search", response_model=SearchResult)
async def search_entries(
    q: str = Query(..., description="搜索关键词"),
    field: str = Query("all", description="搜索字段：id, code, display, display_zh, category, all"),
    skip: int = Query(0, ge=0, description="跳过前 N 条记录"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数量（最大1000）")
):
    """
    搜索词条
    
    - **q**: 搜索关键词（必填）
    - **field**: 搜索字段（id, code, display, display_zh, category, all）
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数
    """
    data = load_dictionary()
    keyword = q.lower()
    
    # 根据字段搜索
    results = []
    for item in data:
        if field == "all":
            # 全字段搜索
            searchable = " ".join([
                str(item.get("id", "")),
                str(item.get("code", "")),
                str(item.get("display", "")),
                str(item.get("display_zh", "")),
                str(item.get("category", "")),
                str(item.get("description", "")),
                str(item.get("description_zh", ""))
            ]).lower()
            if keyword in searchable:
                results.append(item)
        elif field == "id":
            if keyword in item.get("id", "").lower():
                results.append(item)
        elif field == "code":
            if keyword in item.get("code", "").lower():
                results.append(item)
        elif field == "display":
            if keyword in item.get("display", "").lower():
                results.append(item)
        elif field == "display_zh":
            if keyword in item.get("display_zh", ""):
                results.append(item)
        elif field == "category":
            if keyword in item.get("category", "").lower():
                results.append(item)
        else:
            raise HTTPException(status_code=400, detail=f"不支持的搜索字段: {field}")
    
    # 分页
    paginated = results[skip:skip + limit]
    
    return SearchResult(
        total=len(results),
        results=paginated
    )

@app.get("/api/categories", response_class=JSONResponse)
async def get_categories():
    """获取所有可用的分类列表"""
    data = load_dictionary()
    categories = {}
    
    for item in data:
        cat = item.get("category", "未知")
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "valid_categories": VALID_CATEGORIES,
        "actual_categories": [
            {"name": cat, "count": count}
            for cat, count in sorted(categories.items(), key=lambda x: -x[1])
        ]
    }

@app.get("/api/categories/{category}", response_model=SearchResult)
async def get_entries_by_category(
    category: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    按分类查询词条
    
    - **category**: 分类名称（如 posture_codes, motion_codes 等）
    """
    data = load_dictionary()
    
    # 过滤
    filtered = [item for item in data if item.get("category") == category]
    
    if not filtered:
        raise HTTPException(status_code=404, detail=f"分类 '{category}' 不存在或没有词条")
    
    # 分页
    paginated = filtered[skip:skip + limit]
    
    return SearchResult(
        total=len(filtered),
        results=paginated
    )

@app.get("/api/systems", response_class=JSONResponse)
async def get_systems():
    """获取所有编码系统列表"""
    data = load_dictionary()
    systems = {}
    
    for item in data:
        system = item.get("system", "未知")
        system_cat = get_system_category(system)
        if system_cat not in systems:
            systems[system_cat] = {"count": 0, "examples": []}
        systems[system_cat]["count"] += 1
        if len(systems[system_cat]["examples"]) < 3:
            systems[system_cat]["examples"].append(system)
    
    return {
        "systems": [
            {"name": name, "count": info["count"], "examples": info["examples"]}
            for name, info in sorted(systems.items(), key=lambda x: -x[1]["count"])
        ]
    }

# ========== 错误处理 ==========

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """自定义 HTTP 异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# ========== 启动配置 ==========

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("  🚀 WiseFido 医疗编码字典 API 服务启动中...")
    print("=" * 70)
    print("\n📋 服务信息:")
    print("  - API 文档: http://localhost:8080/docs")
    print("  - ReDoc 文档: http://localhost:8080/redoc")
    print("  - 健康检查: http://localhost:8080/api/health")
    print("  - 统计信息: http://localhost:8080/api/stats")
    print("\n" + "=" * 70 + "\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        reload=False,  # 生产环境关闭自动重载
        log_level="info"
    )
