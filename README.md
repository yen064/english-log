# english-log

我的英文練習日誌。透過和 Claude 的對話練習英文,並把每次練習的內容、修正、新單字整理下來,方便日後複習。

## 資料夾導覽

| 路徑 | 內容 |
|------|------|
| `sessions/` | 每次練習一個檔案,檔名為 `YYYY-MM-DD-topic.md` |
| `vocabulary.md` | 累積的單字與片語(依字母排序) |
| `mistakes.md` | 反覆出現的錯誤,依類型分類(時態、冠詞、介系詞、用字等) |

## 使用方式

1. 和 Claude 練習英文對話。
2. 把對話貼到這個 repo 的 Claude Code session,請它建立一筆 session。
3. Claude 會自動產生 session 檔、更新單字表與常犯錯誤,並 commit。

## 複習建議

- 想複習單字:看 `vocabulary.md`。
- 想知道自己常犯什麼錯:看 `mistakes.md`。
- 想回顧某次對話:到 `sessions/` 找對應日期。

## 給 Claude 的規則

檔案格式、處理流程與各項規則都寫在 [`CLAUDE.md`](CLAUDE.md),以該檔為準。
