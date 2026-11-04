# YouTube subtitles retrieved with youtube-transcript-api (2026-11-04)

**狀態：已解決。** 前一份紀錄 [YouTube subtitle retrieval failed (2026-11-04)](youtube-subtitle-retrieval-failed-20261104.md) 的失敗嘗試都沒有改動，這份只記錄後來成功的方法。

## 解法

使用者提出 Python 套件 **`youtube-transcript-api`**（PyPI）。它直接呼叫 YouTube 的內部字幕介面，不需要瀏覽器，也不需要編譯，所以不會碰到 Homebrew（Intel 版、不受支援）的問題。

- **測試影片**：`q8RPtjgXjSQ`（和前一份紀錄同一支）
- **結果**：成功，抓到 290 段英文自動字幕（auto-generated）。
- **環境**：系統的 Python 3.9.6，套件版本 1.2.4。前一份紀錄說 Python 3.9 只能裝到舊版 `yt-dlp`，但這個套件在 3.9 可以正常安裝與執行。
- **沒有繞過任何驗證**：沒有用代理、Cookie 或偽裝，YouTube 沒有擋這個請求。

## 做了什麼

| 項目 | 內容 |
|------|------|
| venv | 在 repo 內的 `.scratch/venv`（約 14 MB），`.scratch/` 已加入 `.gitignore`，不會被提交 |
| 腳本 | `tools/get_transcript.py`：輸入影片連結或 ID，優先用人工字幕，沒有才用自動字幕，輸出到 `.scratch/transcripts/<video_id>.txt` |
| 失敗分類 | 腳本把失敗分成 `NO_ENGLISH_CAPTIONS`、`BLOCKED`、`UNAVAILABLE`、`NETWORK`、`BROKEN`，不重試、不繞過，只回報 |
| 規則 | 失敗後的處理流程寫在 `CLAUDE.md` 的「Getting video captions」 |

## 過程中的觀察

- **先用暫存區測試，再搬到 repo**：一開始在 Claude Code 的 session 暫存區（`/private/tmp/...`）建 venv 驗證可行。那個位置在 repo 之外，重開機或換 session 後會消失，所以改放 repo 內的 `.scratch/`，再刪掉暫存區的版本。
- **遇到一次逾時**：腳本完成後第一次實際執行，連續兩次 `Operation timed out`。用 `curl` 測試，`example.com` 和 `pypi.org` 正常，只有 `youtube.com` 連不上。使用者切換網路環境後，同一個影片又能成功。原因沒有查清楚（可能是暫時的網路問題，也可能是對該連線的限流）。
- **因此新增了 `NETWORK` 類別**：原本腳本把逾時歸為 `BROKEN`（套件壞了），但升級套件解決不了網路問題，會誤導。現在逾時或連不上獨立成 `NETWORK`，處理方式是建議使用者檢查網路或 VPN 後再重試。
- **測試方式**：成功路徑用真實影片測；不存在的影片得到 `UNAVAILABLE`；不合法的輸入得到 `BAD_INPUT`；`NETWORK` 用模擬的連線錯誤測（沒有真的斷網）。

## 限制與風險

- 這個套件靠 YouTube 的內部介面，沒有官方保證，將來可能被擋或因 YouTube 改版而失效。
- 只驗證過一支影片（自動字幕）。人工字幕的路徑、沒有英文字幕的影片，都還沒有用真實影片測過。
- 自動字幕的人名與專有名詞可能有錯，Type 2 流程仍要標出可疑之處。
- 如果失敗，處理流程見 `CLAUDE.md`，原則是停止回報、給使用者選項，不繞過驗證。
