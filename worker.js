/**
 * 甜甜图标工具 - Cloudflare Worker 搜索代理
 * -------------------------------------------------
 * 作用：把前端对 itunes.apple.com 的搜索请求转到你自己的 Cloudflare
 *       节点转发，绕过国内网络对 Apple 接口的不稳定访问。
 *
 * 部署步骤（约 2 分钟）：
 * 1. 打开 https://dash.cloudflare.com → Workers 和 Pages → 创建应用程序
 * 2. 创建 Worker，把本文件全部内容粘贴进去 → 部署
 * 3. 在 Worker 详情页 → 设置 → 域和路由 → 添加路由：
 *    路由：apptb.qqqi.de5.net/api/*
 *    区域：选择你的域名
 * 4. 确认 DNS 记录 apptb.qqqi.de5.net 的"代理状态"是橙色云（已代理）
 *    （设置 → DNS → 记录 → 点击代理状态切换为"已代理"）
 *
 * 部署完成后前端会自动探测到 /api/search 并优先使用，无需改代码。
 * 验证：浏览器打开 https://apptb.qqqi.de5.net/api/search?term=wechat&limit=2
 * 能看到 JSON 即成功。
 */
export default {
  async fetch(request) {
    const url = new URL(request.url);

    // 仅代理 /api/search 路径，其余请求（页面静态资源）原样回源
    if (url.pathname === '/api/search' || url.pathname === '/api/search/') {
      const target = new URL('https://itunes.apple.com/search');
      url.searchParams.forEach((value, key) => target.searchParams.set(key, value));
      target.searchParams.delete('ping'); // 清理前端探测参数

      const resp = await fetch(target.toString(), {
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'TiantianIconTool/1.0'
        }
      });

      const headers = new Headers(resp.headers);
      headers.set('Access-Control-Allow-Origin', '*');
      headers.set('Cache-Control', 'no-store');
      return new Response(resp.body, { status: resp.status, headers });
    }

    return fetch(request);
  }
};
