import json
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class LogViewerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.generate_html().encode('utf-8'))
        elif parsed_path.path == '/api/logs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            logs = self.get_logs()
            self.wfile.write(json.dumps(logs, ensure_ascii=False).encode('utf-8'))
        elif parsed_path.path.startswith('/api/log/'):
            log_name = parsed_path.path.split('/')[-1]
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            log_data = self.get_log_content(log_name)
            self.wfile.write(json.dumps(log_data, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()
    
    def get_logs(self):
        logs_dir = Path("logs")
        if not logs_dir.exists():
            return []
        
        log_files = sorted(logs_dir.glob("run_*.json"), reverse=True)
        return [{"name": f.name, "path": str(f)} for f in log_files]
    
    def get_log_content(self, log_name):
        log_path = Path("logs") / log_name
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_html(self):
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoGen TaskForce - 日志查看器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .sidebar {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .sidebar h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .log-list {
            list-style: none;
        }
        
        .log-item {
            padding: 12px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            border-left: 4px solid #667eea;
        }
        
        .log-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        
        .log-item.active {
            background: #667eea;
            color: white;
        }
        
        .content {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            min-height: 400px;
        }
        
        .mission {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .step {
            margin: 25px 0;
            padding: 20px;
            border-radius: 8px;
            background: #f8f9fa;
            border-left: 4px solid #28a745;
        }
        
        .step-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            font-size: 1.2em;
            font-weight: bold;
            color: #495057;
        }
        
        .step-emoji {
            font-size: 1.5em;
            margin-right: 10px;
        }
        
        .step-time {
            font-size: 0.8em;
            color: #6c757d;
            margin-left: auto;
        }
        
        .step-output {
            background: white;
            padding: 15px;
            border-radius: 4px;
            white-space: pre-wrap;
            line-height: 1.6;
            color: #212529;
        }
        
        .planner { border-left-color: #007bff; }
        .redteam { border-left-color: #dc3545; }
        .commander { border-left-color: #ffc107; }
        .executor { border-left-color: #28a745; }
        .auditor { border-left-color: #6f42c1; }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: #6c757d;
        }
        
        .empty {
            text-align: center;
            padding: 50px;
            color: #6c757d;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 1.8em;
            }
            .content {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 AutoGen TaskForce - 日志查看器</h1>
        
        <div class="sidebar">
            <h2>📚 执行历史</h2>
            <ul class="log-list" id="logList">
                <li class="loading">加载中...</li>
            </ul>
        </div>
        
        <div class="content" id="content">
            <div class="empty">👈 请从左侧选择一个日志查看</div>
        </div>
    </div>
    
    <script>
        const agentEmojis = {
            'Planner': '📋',
            'RedTeam': '🔴',
            'Commander': '👨‍✈️',
            'Executor': '⚙️',
            'Auditor': '📊'
        };
        
        const agentClasses = {
            'Planner': 'planner',
            'RedTeam': 'redteam',
            'Commander': 'commander',
            'Executor': 'executor',
            'Auditor': 'auditor'
        };
        
        async function loadLogs() {
            try {
                const response = await fetch('/api/logs');
                const logs = await response.json();
                
                const logList = document.getElementById('logList');
                
                if (logs.length === 0) {
                    logList.innerHTML = '<li class="empty">暂无日志记录</li>';
                    return;
                }
                
                logList.innerHTML = logs.map(log => {
                    const timestamp = log.name.replace('run_', '').replace('.json', '');
                    const formatted = timestamp.replace(/_/g, ' ').replace(/^(\\d{4})(\\d{2})(\\d{2})/, '$1-$2-$3');
                    return `<li class="log-item" onclick="loadLog('${log.name}')">${formatted}</li>`;
                }).join('');
            } catch (error) {
                console.error('加载日志列表失败:', error);
                document.getElementById('logList').innerHTML = '<li class="empty">加载失败</li>';
            }
        }
        
        async function loadLog(logName) {
            try {
                const response = await fetch(`/api/log/${logName}`);
                const data = await response.json();
                
                const content = document.getElementById('content');
                
                let html = `
                    <h2>📁 ${logName}</h2>
                    <p><strong>⏰ 执行时间:</strong> ${new Date(data.timestamp).toLocaleString('zh-CN')}</p>
                    
                    <div class="mission">
                        <h3>🎯 任务目标</h3>
                        <p>${data.mission}</p>
                    </div>
                `;
                
                data.steps.forEach((step, index) => {
                    const emoji = agentEmojis[step.agent] || '🤖';
                    const className = agentClasses[step.agent] || '';
                    const time = step.timestamp ? new Date(step.timestamp).toLocaleTimeString('zh-CN') : '';
                    
                    html += `
                        <div class="step ${className}">
                            <div class="step-header">
                                <span class="step-emoji">${emoji}</span>
                                <span>步骤 ${index + 1}: ${step.agent}</span>
                                <span class="step-time">${time}</span>
                            </div>
                            <div class="step-output">${step.output}</div>
                        </div>
                    `;
                });
                
                content.innerHTML = html;
                
                // 高亮当前选中的日志
                document.querySelectorAll('.log-item').forEach(item => {
                    item.classList.remove('active');
                    if (item.textContent.includes(logName.replace('run_', '').replace('.json', '').replace(/_/g, ' '))) {
                        item.classList.add('active');
                    }
                });
                
            } catch (error) {
                console.error('加载日志内容失败:', error);
                document.getElementById('content').innerHTML = '<div class="empty">❌ 加载失败</div>';
            }
        }
        
        // 页面加载时获取日志列表
        loadLogs();
    </script>
</body>
</html>
"""

def main():
    port = 8082
    server_address = ('', port)
    httpd = HTTPServer(server_address, LogViewerHandler)
    print(f"\n🚀 日志查看器已启动!")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"💡 按 Ctrl+C 停止服务器\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        httpd.shutdown()

if __name__ == "__main__":
    main()
