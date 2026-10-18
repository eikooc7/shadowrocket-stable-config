# Shadowrocket Stable Config

一个稳定优先、面向日常使用的 Shadowrocket 分流配置。支持 ChatGPT / Claude / Gemini 代理、国内 App 和支付直连、Apple Music 账户直连、AliDNS / DNSPod 加密 DNS，以及少量保守广告拦截规则。

**稳定优先原则：** 不下载第三方大型黑名单，不运行 MITM、证书解密或远程脚本，不上传节点、机场订阅或任何账号凭据。Spotify 免费版音频广告仍可能出现。

## Shadowrocket 订阅

推荐 GitHub Pages 固定订阅地址（需要先在 Settings → Pages → Build and deployment 中将 Source 设为 GitHub Actions）：

https://eikooc7.github.io/shadowrocket-stable-config/shadowrocket.conf

Pages 尚未部署时，可使用已提交的 GitHub Raw 文件：

https://raw.githubusercontent.com/eikooc7/shadowrocket-stable-config/main/config/shadowrocket.conf

**使用方法：** 在 Shadowrocket 备份当前可用配置，导入上述地址或 `config/shadowrocket.conf`，保持现有机场节点，切换「全局路由」为「配置」。优先实测微信扫码点单、Apple Music 账户、ChatGPT 对话、Spotify 音乐播放。手机端是否自动刷新取决于 Shadowrocket 的订阅更新设置；GitHub 发布不等于手机立即切换配置。

## CI/CD

- [Config CI](.github/workflows/ci.yml)：对推送与 PR 静态校验 95 条分流规则、16 项关键域名样本，以及 DNS、MITM、广告域名列表；生成预览 artifact。
- [Publish stable config](.github/workflows/pages.yml)：当正式配置更新到 main 后构建并发布 GitHub Pages；也可手动触发。
- [Review upstream ad-domain candidates](.github/workflows/monitor.yml)：每周检查少量上游广告域名，只创建**非生效**候选 PR，不直接更改正式配置。
- [Dependabot](.github/dependabot.yml)：定期提出 Actions 依赖版本更新。

没有任何静态测试可以完全模拟真实 iPhone 网络；支付、小程序、Apple Music 和 Spotify 音频广告都需要实测。任何误杀应回滚 Git commit，而不是继续扩大规则库。

## 本地测试

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

生成 `site/shadowrocket.conf` 和 `site/version.json`，用于发布。正式版源文件在 `config/shadowrocket.conf`。

## 安全发布与回退

建议启用 main 分支保护，并要求 CI 成功才能合并。对新的广告 REJECT 规则，必须人工审核对应域名是否与 Apple Music、微信小程序、银行支付、AI 登录共用基础设施。遇到正常 App 异常，请立即在 Shadowrocket 切回备份配置，查看连接日志后再修改规则。

技术说明：精准拒绝 `ads.spotify.com` 的规则放在 `spotify.com` 后缀代理规则之前，避免首次匹配导致广告域名未被拦截；这不保证拦截 Spotify 音频广告。

