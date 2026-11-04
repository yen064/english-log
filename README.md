# english-log

我的英文練習日誌。透過和 Claude 的對話練習英文，並把每次練習的內容、修正、新單字整理下來，方便日後複習。

## 資料夾導覽

| 路徑 | 內容 |
|------|------|
| `sessions/` | 每次練習一個檔案，檔名為 `YYYY-MM-DD-topic.md` |
| `sessions.md` | 所有 session 的索引(日期、類型、主題、題數、連結) |
| `session-template.md` | session 檔的樣板（含目錄連結），新增 session 時照這個格式 |
| `archived-history/` | 遇到的問題與調查過程的記錄，一個問題一個檔案 |
| `tools/` | 輔助腳本。`get_transcript.py` 用來取得 YouTube 英文字幕（Type 2 使用） |
| `captions/` | Type 2 影片的完整逐字稿，檔名和對應的 session 檔一致 |
| `.scratch/` | 本機的 Python 虛擬環境與暫時下載的字幕，已設為 git 不追蹤，不會被提交（clone 後不存在，需要時再建立） |
| `vocabulary.md` | 累積的單字與片語(依字母排序，附來源連結) |
| `phrases.md` | 每次 session 的「今日片語」（每次 1 到 5 個，依字母排序，附來源連結） |
| `mistakes.md` | 反覆出現的錯誤，依類型分類(時態、冠詞、介系詞、用字等) |

## 四種練習方式

| Type | 名稱 | 誰主動 | 教材 | 簡單說明 |
|------|------|--------|------|----------|
| 1 | 自由對話 | 我 | 我和 Claude 的對話 | 我想聊什麼就聊什麼，或把已經有的對話貼過去，Claude 整理成 session |
| 2 | 影片課 | 我 | YouTube 影片 | 我貼影片連結，Claude 讀懂內容後以它為教材，發問並指導我 |
| 3 | 時事聊天 | Claude | 目前的時事 | Claude 挑一則真實的時事主題，主動跟我聊 |
| 4 | 延續 | 我 | 已完成的 Type 1、2、3 或 4 session | 我從已完成的 session 中挑一個，Claude 接著上次的題號繼續問，並記錄在原本的檔案裡 |

Type 2 的字幕用 `tools/get_transcript.py` 取得（靠 `youtube-transcript-api` 套件，裝在 `.scratch/venv`）。取得失敗時會停下來回報，並給我幾個選項，不會繞過 YouTube 的限制。解法見 [YouTube subtitles retrieved with youtube-transcript-api (2026-11-04)](archived-history/youtube-subtitles-solved-20261104.md)，之前失敗的過程見 [YouTube subtitle retrieval failed (2026-11-04)](archived-history/youtube-subtitle-retrieval-failed-20261104.md)。

每種類型的詳細流程與規則，以 [`CLAUDE.md`](CLAUDE.md) 為準。

## 使用方式

1. 和 Claude 練習英文對話。
2. 把對話貼到這個 repo 的 Claude Code session，請它建立一筆 session。
3. Claude 會自動產生 session 檔、更新單字表與常犯錯誤，並 commit。

## 複習建議

- 想複習單字：看 `vocabulary.md`。
- 想複習片語：看 `phrases.md`。
- 想知道自己常犯什麼錯：看 `mistakes.md`。
- 想回顧某次對話：先打開索引 [`sessions.md`](sessions.md)，用日期、類型或主題找到那一次，再點連結進入 `sessions/` 裡的完整記錄。

## 給 Claude 的規則

檔案格式、處理流程與各項規則都寫在 [`CLAUDE.md`](CLAUDE.md)，以該檔為準。
