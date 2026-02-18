"""答案填充模块"""
from pathlib import Path
from typing import List, Dict
import yaml
import re

def fill_questionnaire(questions: List[Dict[str, str]], template_path: Path) -> Dict[str, str]:
    """根据模板填充问卷答案"""
    # 加载企业信息模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_data = yaml.safe_load(f)
    
    filled_data = {}
    
    for question in questions:
        q_text = question['question'].lower()
        answer = match_answer(q_text, template_data)
        
        if answer:
            filled_data[question['id']] = answer
    
    return filled_data

def match_answer(question: str, template_data: Dict) -> str:
    """智能匹配问题和答案"""
    # 关键词映射
    keyword_map = {
        'company name|公司名称|企业名称': 'company_name',
        'address|地址': 'company_address',
        'phone|电话|联系方式': 'company_phone',
        'email|邮箱': 'company_email',
        'website|网站': 'company_website',
        'established|成立时间|注册时间': 'established_date',
        'employee|员工|人数': 'employee_count',
        'business|业务范围|经营范围': 'business_scope',
        'iso.*cert|iso.*认证': 'iso_certified',
        'cert.*number|证书编号': 'iso_cert_number',
        'dpo|data protection officer|数据保护官': 'data_protection_officer',
        'gdpr|通用数据保护': 'gdpr_compliant',
        'retention|保留政策': 'data_retention_policy',
        'encryption|加密': 'encryption_method',
        'backup|备份': 'backup_frequency',
        'incident.*response|事件响应': 'incident_response_plan',
        'security.*training|安全培训': 'security_training_frequency',
        'cloud.*provider|云服务商': 'cloud_provider',
        'database|数据库': 'database_type',
        'authentication|认证方式': 'authentication_method',
        'access.*control|访问控制': 'access_control',
        'network.*security|网络安全': 'network_security',
        'vulnerability|漏洞扫描': 'vulnerability_scanning',
        'penetration.*test|渗透测试': 'penetration_testing',
        'security.*policy|安全策略': 'security_policy_exists',
        'data.*classification|数据分类': 'data_classification_policy',
        'third.*party.*audit|第三方审计': 'third_party_audit',
        'business.*continuity|业务连续性': 'business_continuity_plan',
        'disaster.*recovery|灾难恢复': 'disaster_recovery_plan',
    }
    
    # 匹配关键词
    for pattern, key in keyword_map.items():
        if re.search(pattern, question, re.IGNORECASE):
            value = template_data.get(key)
            if value is not None:
                # 处理布尔值
                if isinstance(value, bool):
                    return "是" if value else "否"
                return str(value)
    
    return ""