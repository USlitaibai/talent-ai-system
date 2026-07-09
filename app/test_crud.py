from app.crud import save_resume


resume = {
    "name": "张伟",
    "school": "上海交通大学",
    "major": "计算机科学与技术",
    "research_direction": "人工智能、机器学习",
    "skills": [
        "Python",
        "PyTorch",
        "深度学习"
    ],
    "papers": "3篇"
}

save_resume(resume)

print("=" * 50)
print("CRUD测试完成")
print("=" * 50)