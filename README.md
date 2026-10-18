# Shadowrocket Stable Config

适用于 iPhone / Shadowrocket 的**稳定优先**分流配置：国内服务直连、AI / Spotify 走所选代理节点、AliDNS + DNSPod DoH、少量高确定性广告域名拦截。

> **安全取向**：不包含节点、机场订阅、密钥、账号；不使用远程广告黑名单、MITM、第三方响应脚本。无法保证去除 Spotify 免费版音频广告，也无法保证所有 App 100% 兼容。

## 快速使用

1. 在 Shadowrocket 中备份当前可用配置。
2. 导入 `config/shadowrocket.conf`，启用「配置」分流模式，继续使用原有节点。
3. 优先验证 **微信扫码点单 → Apple Music 账户 → ChatGPT → Spotify**。
4. 有异常立即恢复上一版，并通过 Shadowrocket 连接记录确认真实命中规则。

## 固定订阅 URL（GitHub Pages）

启用 GitHub Pages 后，长期稳定的订阅地址：

`https://eikooc7.github.io/shadowrocket-stable-config/shadowrocket.conf`

需要先在仓库 **Settings → Pages → Build and deployment → Source: GitHub Actions** 中启用 Pages，并确认 `Publish stable config` 工作流成功。

如果暂时不启用 Pages，也可使用 GitHub Raw 文件（取决于网络可访问性）：

`https://raw.githubusercontent.com/eikooc7/shadowrocket-stable-config/main/config/shadowrocket.conf`

**注意**：GitHub 上配置变更不代表手机端瞬间自动更新；请在 Shadowrocket 的配置订阅中启用它支持的定期更新/手动刷新。启用前，先确认你的网络能够访问此 URL。

## CI/CD 设计

- `Config CI`：每次 push/PR 静态检查规则格式、DNS、MITM 关闭、广告拦截白名单、关键域名匹配顺序，输出预览 artifact。
- `Publish stable config`：`main` 分支的正式配置通过测试后发布到 GitHub Pages（需要先启用 Pages）。
- `Review upstream ad-domain candidates`：每周检测 StevenBlack/hosts 中的少量候选域名，只将差异提交 PR 到**不生效**的 `rules/review-candidates.txt`；不自动加入正式拦截规则。
- Dependabot：每周提出 Actions 依赖更新 PR。

**自动检查 ≠ 无审查地自动扩大广告拦截范围。** 这是为了避免再次出现 Apple Music、银行或扫码点餐故障。规则要进入正式版，必须人工审查并经 CI 后合并 `main`。可在 GitHub 设置 `main` 分支保护规则，要求 `verify` CI 通过才允许合并。实际设备端验证仍然必要。

## 本地检查

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

`site/` 是生成产物，不需要提交到仓库。

## 故障回退

1. 立即在 Shadowrocket 切回已知可用配置。
2. 对 DNS 故障，可临时改用：
   `dns-server = system` / `fallback-dns-server = system`
3. 查看 Github commit 历史，必要时 Revert 最近的相关提交并重新部署 Pages。
4. 不建议在银行、支付或 Apple 账户域名上开启 HTTPS 解密。

## 项目首次上 GitHub

请在 `eikooc7` GitHub 账户下创建一个**公开的空仓库**，名为 `shadowrocket-stable-config`，**不要勾选自动生成 README**。在解压后的项目目录执行：

```bash
git init
git add .
git commit -m "feat: initialize stable Shadowrocket config and CI/CD"
git branch -M main
git remote add origin https://github.com/eikooc7/shadowrocket-stable-config.git
git push -u origin main
```

建议使用 GitHub Desktop 或 `gh auth login` / Git 凭据助手进行身份验证，**不要把 GitHub Token 写入仓库**。

## 特别说明

- 原配置中 `DOMAIN-SUFFIX,spotify.com,PROXY` 在 `DOMAIN,ads.spotify.com,REJECT` 之前，按顺序匹配会使后者不可达。仓库版调整为先精确 REJECT，再宽泛 PROXY。
- 静态模拟只检查已列出的常见域名；餐饮小程序使用的第三方实际域名无法全部预测。
- GitHub Pages 公共托管可能在某些网络条件下无法访问，无法对其可达性作保证。