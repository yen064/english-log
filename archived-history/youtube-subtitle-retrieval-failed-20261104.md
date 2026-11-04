# YouTube subtitle retrieval failed (2026-11-04)

**狀態:暫停。** 目前沒有找到一個「不需要手動操作、又不影響本機」的方式,可以自動取得 YouTube 影片的英文字幕。

## 背景

Type 2(影片課)需要影片的英文字幕。我(Claude)看不到影片,只能讀字幕文字,所以必須先取得逐字稿。

- **測試影片**:<https://www.youtube.com/watch?v=q8RPtjgXjSQ>(桑德斯×AOC 國會記者會,頻道加了中英字幕)
- **這支影片的字幕軌**:有一條 English (auto-generated)
- **使用者的限制**:不要太麻煩、盡量不影響本機、不要一直建議手動貼逐字稿

## 嘗試過程與結果

| # | 方式 | 結果 | 原因 |
|---|------|------|------|
| 1 | `brew install yt-dlp` | 失敗 | 見下方「Homebrew 失敗的原因」 |
| 2 | WebFetch 直接讀 YouTube 頁面 | 只拿到標題 | 字幕不在原始頁面裡,頁面內容只剩導覽列與頁尾 |
| 3 | `curl` + Python 讀頁面,再抓字幕網址 | 找得到字幕軌,但下載是空的 | 字幕網址回傳 HTTP 200、0 bytes(預設、vtt、srv3 三種格式都一樣) |
| 4 | 子代理 `isolation: "remote"` 執行 `yt-dlp` | 失敗 | 沒有真的在遠端執行;`yt-dlp` 被 YouTube 拒絕 |
| 5 | Claude in Chrome / 內建瀏覽器 | 沒有執行 | 見下方「瀏覽器方案」 |
| 6 | 第三方字幕網站與 API(經 WebFetch) | 7 個全部失敗 | 見下方表格 |
| 7 | 分析 Tactiq 的網頁腳本,直接呼叫它的後端 | 停止 | 後端需要 Firebase App Check token,屬於存取控制,不繞過 |

## 細節

### 1. Homebrew 失敗的原因

- 這台 Mac 是 Apple Silicon,但 Homebrew 是 **Intel 版**,裝在 `/usr/local`,透過 Rosetta 執行(`brew config`:`macOS: 26.1-x86_64`、`Rosetta 2: true`,內建 Ruby 為 x86_64)。
- Homebrew 已不再支援 Intel(Tier 3),不再提供預編譯套件,所以 `yt-dlp` 要連帶從原始碼編譯約 20 個相依套件(`llvm`、`rust`、`cmake`、`python` 等)。
- 實際的失敗訊息:`configure: error: C compiler cannot create executables`(編譯 `pkgconf-3.0.10` 時)。為什麼編譯器失敗,**沒有查清楚**。
- **更正**:一開始誤判成「Command Line Tools 版本太舊」。實際上 CLT 26.2 高於 Homebrew 7.0.x 的最低要求(26.0.0);訊息中的 27.0 只是建議更新,不是失敗原因。
- Homebrew 7.0.12 是 2026-11-04 執行 `brew install` 時自動更新的(上一版 7.0.11,2026-10-27)。

### 3. 字幕下載為什麼是空的

- 頁面裡的 `captionTracks` 可以讀到,字幕軌網址也可以組出來,但請求回傳空內容。
- **推測**:YouTube 現在要求只有真實瀏覽器播放影片時才會產生的來源驗證(proof-of-origin token)。這個原因是推測,沒有直接證實。
- 要繞過驗證就得偽裝成瀏覽器,不這樣做。

### 4. 「遠端」執行為什麼不是遠端

- 工具說明寫 `isolation: "remote"` 是在雲端環境執行,但**兩次都在使用者的本機執行**(第二次 Claude 先要求子代理確認所在環境,它確認是本機後就停止了)。
- 第一次在本機暫存區留下一個 22 MB 的 Python 虛擬環境,已刪除。
- 官方文件(<https://code.claude.com/docs/en/sub-agents.md>、<https://code.claude.com/docs/en/worktrees.md>)只記載 `isolation: worktree`,**沒有記載 `remote`**。
- 正規的雲端做法是 Claude Code on the web(`claude --cloud`),需要:claude.ai 帳號與合格方案、GitHub 連結(GitHub App 或 `/web-setup`)、先 push、網路存取設定。預設的 Trusted 網路等級允許 `pypi.org`,但**不含 `youtube.com`**。使用者評估後決定不走這條路(太麻煩)。參考:<https://code.claude.com/docs/en/claude-code-on-the-web.md>、<https://code.claude.com/docs/en/cloud-environments.md>。
- 子代理在本機實際跑 `yt-dlp` 的結果:能裝到的最新版是 2025.10.14(Python 3.9 的限制),執行時 YouTube 回應 `The page needs to be reloaded`,子代理判斷是 YouTube 對該版本客戶端的 SABR 串流強制,不是驗證碼或登入。更新的版本(例如 nightly)沒有試。

### 5. 瀏覽器方案(沒有執行)

- 這個 session 沒有內建瀏覽器的工具。
- Claude in Chrome:這台電腦沒有 Chrome(使用者用 Edge)。搜尋結果顯示 Claude Code 的 Chrome 整合文件列出 Edge,但 Help Center 的說法偏向只支援 Chrome,官方互相矛盾;沒有找到 macOS + Edge 的明確結果。
- 另外安裝 Chrome 的估計:app 本身約 0.4–1.2 GB,長期使用約 1–3 GB;這台 Mac 可用空間 133 GiB,空間不是問題。
- 使用者決定不裝 Chrome(太麻煩、希望最小影響本機)。

### 6. 第三方字幕網站與 API

| 站台 | 結果 |
|------|------|
| youtubetotranscript.com | HTTP 403 |
| yewtu.be(Invidious) | 瀏覽器驗證頁,要求圖片驗證碼 |
| inv.nadeko.net(Invidious) | HTTP 502 |
| pipedapi.kavin.rocks(Piped) | HTTP 526 |
| piped-api.garudalinux.org(Piped) | 網域不存在 |
| tactiq.io | 頁面可載入,但逐字稿是 JavaScript 執行後才產生,只拿到空殼 |
| kome.ai | HTTP 429 |

### 7. Tactiq 的後端

- 頁面腳本在載入後會 `POST …/transcript`(內容是影片網址與語言),後端回傳標題與字幕清單。
- 該請求必須帶標頭 `X-Firebase-AppCheck: <token>`。App Check 用來證明請求來自真正的 Tactiq 網頁,沒有瀏覽器就拿不到 token。
- 取得這個 token 等於繞過對方的存取控制,所以在這裡停止。

## 結論

- 兩個共同的阻礙:**YouTube 與第三方站台都會擋掉非瀏覽器的程式化請求**;**這台 Mac 的 Homebrew 是不受支援的 Intel 版**。
- 不需要使用者手動操作、也不繞過驗證的方式,目前都沒有成功。

## 尚未嘗試的方向

- 在本機用較新的 Python 安裝新版或 nightly 的 `yt-dlp`(會在本機安裝東西,且不保證成功)。
- 改用頁面上本來就有全文逐字稿的教材來源(例如 TED、BBC Learning English、VOA Learning English、附逐字稿的 Podcast)。
- 搜尋同一場內容的現成文字稿(官方紀錄、C-SPAN、新聞全文)。
- MCP 伺服器(第三方,需要在本機安裝與執行)。
- 先從不需要字幕的 Type 1 或 Type 3 開始。
